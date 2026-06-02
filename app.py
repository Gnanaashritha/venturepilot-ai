from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from prompts import MASTER_PROMPT

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

st.set_page_config(
    page_title="VenturePilot AI",
    page_icon="🚀",
    layout="wide"
)

def create_pdf(report_text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    for line in report_text.split("\n"):
        if line.strip():
            content.append(Paragraph(line, styles["BodyText"]))

    doc.build(content)

    buffer.seek(0)
    return buffer


st.title("🚀 VenturePilot AI")

st.markdown("""
Validate startup ideas using AI-powered market analysis,
risk assessment, and MVP recommendations.
""")

idea = st.text_input("Startup Idea")
audience = st.text_input("Target Audience")
problem = st.text_area("Problem Being Solved")

if st.button("🚀 Analyze Startup"):

    prompt = MASTER_PROMPT.format(
        idea=idea,
        audience=audience,
        problem=problem
    )

    with st.spinner("Analyzing startup idea..."):

        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        report = response.choices[0].message.content

        st.markdown(report)

        pdf_file = create_pdf(report)

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="startup_report.pdf",
            mime="application/pdf"
        )