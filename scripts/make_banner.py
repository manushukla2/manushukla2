def make_banner(output_path="banner.svg"):
    text = "Hi, I'm Manu Shukla"
    sub  = "AI Software Engineer,"

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="860" height="100" style="background:#0d1117">

  <!-- Main title typing effect -->
  <text x="430" y="45" text-anchor="middle"
        font-family="Courier New,monospace" font-size="28" fill="#39d353"
        opacity="0">
    {text}
    <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="0.2s" fill="freeze"/>
  </text>

  <!-- Cursor blink on title -->
  <text x="620" y="45" font-family="Courier New,monospace" font-size="28" fill="#39d353">
    <animate attributeName="opacity" values="1;0;1" dur="0.8s" begin="0s" repeatCount="3"/>
  </text>

  <!-- Subtitle fade in -->
  <text x="430" y="75" text-anchor="middle"
        font-family="Courier New,monospace" font-size="14" fill="#58a6ff"
        opacity="0">
    {sub}
    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1s" fill="freeze"/>
  </text>

</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    make_banner()
