import os
import streamlit as st
from groq import Groq

# Set page title and layout
st.set_page_config(page_title="AI Content Assistant", page_icon="📝", layout="centered")

st.title("📝 AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags in seconds using Groq.")

# Retrieve Groq API Key from Streamlit Secrets or Environment Variables
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.warning("⚠️ GROQ_API_KEY is missing! Please configure it in your Streamlit Secrets or environment variables.")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=api_key)

# User Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)

    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Social Media Post", "Blog Intro", "Product Announcement", "Newsletter Snippet", "Educational Tip"]
        )
        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Threads"]
        )
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual & Friendly", "Persuasive", "Witty & Fun", "Informative", "Inspirational"]
        )

    with col2:
        topic = st.text_input("Topic / Main Idea", placeholder="e.g., Launching a new remote work software tool")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Tech entrepreneurs and freelancers")

    submitted = st.form_submit_button("🚀 Generate Content", use_container_width=True)

# Process Generation
if submitted:
    if not topic.strip():
        st.error("Please enter a topic before generating content.")
    else:
        # Prompt definition
        system_prompt = (
            "You are an expert social media manager and digital content writer. "
            "Your output must be engaging, formatted cleanly, and directly tailored to the target platform and audience."
        )
        
        user_prompt = f"""
Please generate a complete post based on these requirements:
- Content Type: {content_type}
- Platform: {platform}
- Topic: {topic}
- Target Audience: {target_audience if target_audience else 'General Audience'}
- Tone: {tone}

Formatting Requirements:
1. Main Post Body / Caption (include call-to-action where applicable)
2. A separate list of 5-8 relevant hashtags at the bottom.
"""

        with st.spinner("Generating content..."):
            try:
                # API Call using a high-performance free-tier Groq model
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                generated_content = response.choices[0].message.content

                st.subheader("📌 Generated Result")
                st.markdown(generated_content)

                # Download Option
                st.download_button(
                    label="📥 Download Content as Text File",
                    data=generated_content,
                    file_name="generated_content.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred while calling the Groq API: {e}")
