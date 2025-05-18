import streamlit as st
from groq import Groq
import re
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

st.set_page_config(page_title="AI Ad Script Generator", layout="centered")

st.title("🎬 AI Ad Video Script Generator")
st.markdown("Generate high-converting ad scripts for products or services using Groq's DeepSeek model.")

# Inputs
script_type = st.radio("What are you promoting?", ["Product", "Lead-Gen/Offer"], horizontal=True)
tone = st.selectbox("Choose the tone of the script:", ["Casual", "Urgent", "Friendly", "Authoritative", "Luxurious"])
ad_length = st.slider("Desired Ad Length (seconds)", 15, 60, 30, step=5)

product_or_offer = st.text_area("Describe your product or offer", height=100)
target_audience = st.text_input("Who is the target audience?")

generate = st.button("Generate Script")

if generate:
    st.markdown("🚀 **Generating your script using DeepSeek...**")

    structure = "Hook → Problem → Solution → Social Proof → Call to Action" if script_type == "Product" else \
                "Pain Point → Who Qualifies → Urgency → Proof/Trust Signal → Call to Action"

    system_prompt = f"""
You are a world-class video ad scriptwriter. Write a {ad_length}-second script for a {script_type.lower()}.
Use the structure: {structure}.
Tone: {tone}.
Audience: {target_audience}.
Make the script engaging, emotionally compelling, and optimized for conversions.
Each section should be labeled clearly.
    """.strip()

    # API Call
    try:
        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": product_or_offer}
            ]
        )
        raw_output = completion.choices[0].message.content
        cleaned_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL).strip()

        st.subheader("🎥 Your Generated Ad Script:")
        st.markdown(cleaned_output)

    except Exception as e:
        st.error(f"❌ Failed to generate script: {e}")
