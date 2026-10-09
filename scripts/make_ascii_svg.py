from PIL import Image
import math

RAMP = " .`:-=+*cs#%@"

def image_to_ascii_svg(
    image_path="source-prepped.png",
    output_path="avi-ascii.svg",
    cols=100,
    font_size=7,
    line_height=1.2,
):
    img = Image.open(image_path).convert("L")
    aspect = img.height / img.width
    rows = int(cols * aspect * 0.45)
    img = img.resize((cols, rows))
    pixels = list(img.getdata())

    lines = []
    for r in range(rows):
        row_chars = ""
        for c in range(cols):
            brightness = pixels[r * cols + c]
            idx = int(brightness / 255 * (len(RAMP) - 1))
            row_chars += RAMP[idx]
        lines.append(row_chars)

    char_w = font_size * 0.6
    svg_w = int(cols * char_w) + 20
    svg_h = int(rows * font_size * line_height) + 20

    anims = []
    texts = []
    total_dur = rows * 0.045

    for i, line in enumerate(lines):
        delay = i * 0.045
        clip_id = f"cl{i}"
        y = 10 + int(i * font_size * line_height) + font_size

        anims.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="{y - font_size}" width="0" height="{int(font_size * line_height) + 2}">'
            f'<animate attributeName="width" from="0" to="{svg_w}" dur="0.3s" begin="{delay:.3f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        texts.append(
            f'<text x="10" y="{y}" clip-path="url(#{clip_id})" '
            f'font-family="Courier New,monospace" font-size="{font_size}" fill="#a0a0a0">'
            f'{line.replace("&","&amp;").replace("<","&lt;")}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" style="background:#0d1117">
<defs>{''.join(anims)}</defs>
{''.join(texts)}
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    image_to_ascii_svg()
