"""WCAG 2.1 relative-luminance contrast check for the Umbral v1.0 tokens.

Phase 0 verification only. The generated matrix in Phase 1 will live in
tokens/build/contrast.json and be produced from tokens/src/, not from these
hard-coded values (which are transcribed from the live products' tokens.css).
"""

TOKENS = {
    "laboratorio": {
        "ink": "#16191C", "base": "#F2F3F1", "panel": "#FAFAF8",
        "border": "#DDE0DC", "gridline": "#E6E8E4", "baseline": "#C4C9C4",
        "muted": "#6E756F", "caption": "#9AA19B",
        "signal": "#128273", "model": "#5A63D8", "alert": "#C8503F",
    },
    "instrumento": {
        "ink": "#EDF1F4", "base": "#101418", "panel": "#171C22",
        "border": "#2A3138", "gridline": "#232A31", "baseline": "#3A434C",
        "muted": "#8B95A0", "caption": "#5C6670",
        "signal": "#5FD4C4", "model": "#8B93F8", "alert": "#E26A5A",
    },
}

# role -> what threshold actually applies to it
TEXT_ROLES = ["ink", "muted", "caption", "signal", "model", "alert"]
GRAPHIC_ROLES = ["signal", "model", "alert", "baseline", "border", "gridline"]
BACKGROUNDS = ["base", "panel"]


def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.2126 * srgb_to_linear(r)
            + 0.7152 * srgb_to_linear(g)
            + 0.0722 * srgb_to_linear(b))


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def report():
    for mode, t in TOKENS.items():
        print(f"\n{'=' * 74}\nmodo {mode}\n{'=' * 74}")
        print(f"{'pair':<28} {'ratio':>7}  {'AA text':>8} {'graphic':>8}")
        print("-" * 74)
        seen = set()
        for bg in BACKGROUNDS:
            for role in TEXT_ROLES + GRAPHIC_ROLES:
                if role == bg or (role, bg) in seen:
                    continue
                seen.add((role, bg))
                r = ratio(t[role], t[bg])
                is_text = role in TEXT_ROLES
                is_graphic = role in GRAPHIC_ROLES
                text_v = ("PASS" if r >= 4.5 else "FAIL") if is_text else "  — "
                graph_v = ("PASS" if r >= 3.0 else "FAIL") if is_graphic else "  — "
                flag = "  <<<" if (is_text and r < 4.5) or (is_graphic and r < 3.0) else ""
                print(f"{role + ' on ' + bg:<28} {r:>7.2f}  {text_v:>8} {graph_v:>8}{flag}")


def check_candidate(label, fg, mode):
    t = TOKENS[mode]
    rb, rp = ratio(fg, t["base"]), ratio(fg, t["panel"])
    ok = "OK " if min(rb, rp) >= 4.5 else "no "
    print(f"  {ok}{label:<22} {fg}  vs base {rb:5.2f}  vs panel {rp:5.2f}")


if __name__ == "__main__":
    report()
