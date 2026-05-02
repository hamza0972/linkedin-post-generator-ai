import os
import gradio as gr
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)


def generate_post(topic, tone, audience):
    try:
        prompt = f"""
Write a high-quality LinkedIn post.

Topic: {topic}
Tone: {tone}
Audience: {audience}

Rules:
- Strong hook
- Short paragraphs
- Emojis
- Bullet points if needed
- End with a question
- Add 4–6 hashtags
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


def app(topic, tone, audience):
    if not topic:
        return "⚠️ Please enter a topic"
    return generate_post(topic, tone, audience)


demo = gr.Interface(
    fn=app,
    inputs=[
        gr.Textbox(label="📌 Topic"),
        gr.Dropdown(
            ["Professional", "Casual", "Motivational", "Storytelling"],
            label="🎭 Tone",
            value="Professional"
        ),
        gr.Textbox(label="🎯 Audience")
    ],
    outputs=gr.Textbox(
        label="📝 LinkedIn Post",
        lines=22
    ),
    title="💼 LinkedIn Post Generator",
    description="Generate professional LinkedIn posts using Groq AI 🚀"
)

demo.launch()
