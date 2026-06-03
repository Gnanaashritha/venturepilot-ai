from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from prompts import MASTER_PROMPT

load_dotenv()

# ---------------------------
# OPENROUTER CLIENT
# ---------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="VenturePilot AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------
# SIDEBAR
# ---------------------------

with st.sidebar:
    st.title("🚀 VenturePilot AI")

    st.markdown("---")

    st.markdown("### Navigation")

    st.write("📊 Dashboard")
    st.write("🚀 New Analysis")
    st.write("📄 Reports")
    st.write("⚔️ Competitors")
    st.write("⚙️ Settings")

# ---------------------------
# PDF FUNCTION
# ---------------------------

def create_pdf(report_text):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    for line in report_text.split("\n"):
        if line.strip():
            content.append(
                Paragraph(line, styles["BodyText"])
            )

    doc.build(content)

    buffer.seek(0)

    return buffer

# ---------------------------
# HEADER
# ---------------------------

st.title("🚀 VenturePilot AI")

st.markdown(
    """
    Turn startup ideas into actionable business insights.

    Analyze market opportunities, competitors, risks,
    revenue models, and startup readiness instantly.
    """
)

st.markdown("---")

# ---------------------------
# METRICS SECTION
# ---------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Startup Score",
        value="--"
    )

with col2:
    st.metric(
        label="Market Demand",
        value="--"
    )

with col3:
    st.metric(
        label="Risk Level",
        value="--"
    )

with col4:
    st.metric(
        label="Revenue Potential",
        value="--"
    )

st.markdown("---")

# ---------------------------
# INPUT FORM
# ---------------------------

st.subheader("🚀 New Startup Analysis")

idea = st.text_input(
    "Startup Idea"
)

audience = st.text_input(
    "Target Audience"
)

problem = st.text_area(
    "Problem Being Solved",
    height=150
)

# ---------------------------
# ANALYSIS
# ---------------------------

if st.button("🚀 Analyze Startup"):

    prompt = MASTER_PROMPT.format(
        idea=idea,
        audience=audience,
        problem=problem
    )

    with st.spinner(
        "Analyzing startup idea..."
    ):

        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        report = response.choices[0].message.content

        st.markdown("---")

        st.subheader("📊 Analysis Report")

        st.markdown(report)

        pdf_file = create_pdf(report)

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="startup_report.pdf",
            mime="application/pdf"
        )