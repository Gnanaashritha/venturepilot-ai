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

    st.markdown(response.choices[0].message.content)