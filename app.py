import gradio as gr
from generate import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="STEM Scholarship Assistant") as demo:
    gr.Markdown("# 🎓 STEM Scholarship Assistant")
    gr.Markdown(
        "Ask about undergraduate STEM scholarships, eligibility, award amounts, "
        "and funding. Answers are grounded in real documents with sources cited."
    )

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What is the Goldwater Scholarship award amount?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
