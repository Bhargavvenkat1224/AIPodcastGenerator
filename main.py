import os
import uuid
import streamlit as st
from dotenv import load_dotenv
import requests
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found in .env")
    st.stop()
if not ELEVENLABS_API_KEY:
    st.error("ELEVENLABS_API_KEY not found in .env")
    st.stop()

# Clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Streamlit UI
st.set_page_config(page_title="Text → Podcast", layout="centered")
st.title("Text to Podcast Generator")
st.caption("Turn any article, blog, or notes into a natural-sounding podcast in seconds!")

# Input methods
tab1, tab2 = st.tabs(["Type/Paste Text", "Upload .txt File"])

with tab1:
    text_input = st.text_area("Paste your text here:", height=300, placeholder="e.g. A blog post, news article, notes...")
with tab2:
    uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])

generate_btn = st.button("Generate Podcast", type="primary", use_container_width=True)

if generate_btn:
    # Get text
    if uploaded_file:
        text = uploaded_file.read().decode("utf-8", errors="ignore")
    elif text_input and text_input.strip():
        text = text_input
    else:
        st.warning("Please provide some text!")
        st.stop()

    if not text.strip():
        st.error("Text is empty!")
        st.stop()

    with st.spinner("Step 1/2: Summarizing with GPT-4.1-mini..."):
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a friendly podcast host. Summarize the given text into a natural, engaging spoken script (max 1800 characters). Make it conversational and warm, like you're talking directly to the listener. Do NOT include quotes, timestamps, or metadata."},
                    {"role": "user", "content": f"Summarize this into a podcast script:\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            script = response.choices[0].message.content.strip()
            st.success("Summary created!")
            st.text_area("Podcast Script Preview:", script, height=150)

        except Exception as e:
            st.error(f"OpenAI Error: {e}")
            st.stop()

    with st.spinner("Step 2/2: Generating voice with ElevenLabs..."):
        try:
            url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL/stream"

            headers = {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }

            payload = {
                "text": script,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.8,
                    "style": 0.6,
                    "use_speaker_boost": True
                }
            }

            response = requests.post(url, json=payload, headers=headers, stream=True)

            if response.status_code != 200:
                st.error(f"ElevenLabs Error: {response.status_code}\n{response.text}")
                st.stop()

            # Save audio
            os.makedirs("podcasts", exist_ok=True)
            filename = f"podcasts/podcast_{uuid.uuid4().hex[:8]}.mp3"
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            audio_bytes = open(filename, "rb").read()

            st.success("Podcast generated successfully!")
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="Download Podcast MP3",
                data=audio_bytes,
                file_name="my_podcast.mp3",
                mime="audio/mp3"
            )

            # Optional: Show script again
            with st.expander("View full spoken script"):
                st.write(script)

        except Exception as e:
            st.error(f"Audio generation failed: {e}")