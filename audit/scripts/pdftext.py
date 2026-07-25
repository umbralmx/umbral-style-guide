"""Minimal PDF text extractor: decodes subset-font hex strings via ToUnicode CMaps.

Enough to read the Umbral brand book without poppler installed.
"""
import re
import sys
import zlib

data = open(sys.argv[1], "rb").read()

# ── map object number -> raw bytes ────────────────────────────────────────
objs = {}
for m in re.finditer(rb"(\d+)\s+(\d+)\s+obj\b", data):
    num = int(m.group(1))
    start = m.end()
    end = data.find(b"endobj", start)
    objs[num] = data[start:end]


def stream_of(body):
    m = re.search(rb"stream\r?\n", body)
    if not m:
        return None
    e = body.find(b"endstream", m.end())
    raw = body[m.end():e]
    if b"FlateDecode" in body[:m.start()]:
        try:
            return zlib.decompress(raw)
        except Exception:
            return None
    return raw


# ── build ToUnicode maps, keyed by the font resource they belong to ───────
def parse_cmap(b):
    cmap = {}
    for m in re.finditer(rb"beginbfchar(.*?)endbfchar", b, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", m.group(1)):
            cmap[int(src, 16)] = "".join(
                chr(int(dst[i:i + 4], 16)) for i in range(0, len(dst), 4))
    for m in re.finditer(rb"beginbfrange(.*?)endbfrange", b, re.S):
        for lo, hi, dst in re.findall(
                rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", m.group(1)):
            lo_i, hi_i, d = int(lo, 16), int(hi, 16), int(dst, 16)
            for k in range(lo_i, hi_i + 1):
                cmap[k] = chr(d + k - lo_i)
    return cmap


# font name (/F4) -> cmap, resolved per page resource dict
tounicode_by_obj = {}
for num, body in objs.items():
    if b"beginbfchar" in body or b"beginbfrange" in body:
        s = stream_of(body)
        if s:
            tounicode_by_obj[num] = parse_cmap(s)
    else:
        s = stream_of(body)
        if s and (b"beginbfchar" in s or b"beginbfrange" in s):
            tounicode_by_obj[num] = parse_cmap(s)

# font object -> ToUnicode object
font_to_cmap = {}
for num, body in objs.items():
    if b"/Font" in body or b"/BaseFont" in body:
        m = re.search(rb"/ToUnicode\s+(\d+)\s+\d+\s+R", body)
        if m:
            font_to_cmap[num] = tounicode_by_obj.get(int(m.group(1)), {})

# resource name (/F4) -> font object, gathered from every /Font << >> dict
name_to_cmap = {}
for num, body in objs.items():
    for fm in re.finditer(rb"/Font\s*<<(.*?)>>", body, re.S):
        for nm, fo in re.findall(rb"/(\w+)\s+(\d+)\s+\d+\s+R", fm.group(1)):
            cm = font_to_cmap.get(int(fo))
            if cm:
                name_to_cmap.setdefault(nm.decode(), {}).update(cm)

# merged fallback: every glyph mapping we found
merged = {}
for cm in tounicode_by_obj.values():
    merged.update(cm)


def decode_hex(h, cmap):
    out = []
    # subset fonts here use 1-byte codes
    for i in range(0, len(h), 2):
        code = int(h[i:i + 2], 16)
        out.append(cmap.get(code, merged.get(code, "")))
    return "".join(out)


# ── walk content streams in order, emitting text ──────────────────────────
pages = []
for num in sorted(objs):
    body = objs[num]
    s = stream_of(body)
    if not s or b"Tj" not in s:
        continue
    cur = {}
    buf = []
    last_td = 0
    for m in re.finditer(
            rb"/(\w+)\s+[\d.]+\s+Tf|<([0-9A-Fa-f]+)>\s*Tj|"
            rb"([-\d.]+)\s+[-\d.]+\s+Td|\bTm\b|\bET\b", s):
        if m.group(1):
            cur = name_to_cmap.get(m.group(1).decode(), merged)
        elif m.group(2):
            buf.append(decode_hex(m.group(2).decode(), cur))
        elif m.group(3):
            if float(m.group(3)) == 0:
                buf.append(" ")
    if buf:
        pages.append("".join(buf))

text = "\n\n=== page break ===\n\n".join(pages)
if len(sys.argv) > 2:
    kw = sys.argv[2].lower()
    for m in re.finditer(re.escape(kw), text.lower()):
        print(text[max(0, m.start() - 500):m.start() + 900])
        print("\n" + "~" * 70 + "\n")
else:
    print(text)
