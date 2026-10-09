def make_info_card(output_path="info-card.svg"):
    lines = [
        ("", "manushukla2@github", "#39d353"),
        ("", "-" * 32, "#555"),
        ("Role", "Software Engineer (AI/ML)", "#58a6ff"),
        ("Agentic", "LangGraph · CrewAI · AutoGen", "#58a6ff"),
        ("Harness", "LangChain · LlamaIndex · Haystack", "#58a6ff"),
        ("Graphs", "LangGraph · DAG · State Machines", "#58a6ff"),
        ("LLMs", "Qwen3 · LLaMA 70B · NLLB-200", "#58a6ff"),
        ("Infra", "vLLM · QLoRA · Prompt Eng.", "#58a6ff"),
        ("ML/DL", "TensorFlow · Keras · UNet · VLMs", "#58a6ff"),
        ("Vector", "Pinecone · ChromaDB · FAISS", "#58a6ff"),
        ("Stack", "Python · FastAPI · Next.js · Docker", "#58a6ff"),
        ("System", "Multi-Tenant · RBAC · Azure · CI/CD", "#58a6ff"),
        ("Cloud", "Azure A100 · AWS · Nginx · Keycloak", "#58a6ff"),
        ("", "", ""),
        ("Projects", "dealsense · API-Forge · Nimbus", "#f0883e"),
        ("", "", ""),
        ("Contact", "github.com/manushukla2", "#39d353"),
    ]

    font_size = 13
    line_height = 22
    padding = 20
    svg_w = 490
    svg_h = padding * 2 + len(lines) * line_height + 10

    elements = []
    for i, (key, val, color) in enumerate(lines):
        y = padding + i * line_height + font_size
        delay = i * 0.08
        g_id = f"l{i}"

        content = ""
        if key == "":
            content = f'<text x="{padding}" y="0" font-family="Courier New,monospace" font-size="{font_size}" fill="{color}">{val}</text>'
        else:
            content = (
                f'<text x="{padding}" y="0" font-family="Courier New,monospace" font-size="{font_size}">'
                f'<tspan fill="#e0e0e0">{key.ljust(10)}</tspan>'
                f'<tspan fill="#555">: </tspan>'
                f'<tspan fill="{color}">{val}</tspan>'
                f'</text>'
            )

        elements.append(
            f'<g id="{g_id}" transform="translate(0,{y})" opacity="0">'
            f'{content}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0,{y+8}" to="0,{y}" dur="0.3s" begin="{delay:.2f}s" fill="freeze"/>'
            f'</g>'
        )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" style="background:#0d1117">
{''.join(elements)}
</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    make_info_card()
