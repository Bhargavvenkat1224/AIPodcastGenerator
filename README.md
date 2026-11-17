#  AI Podcast Generator
An AI Agent that takes input text, summarizes it, and generates podcast audio.

Turn any article, blog, or notes into a natural-sounding podcast in seconds using GPT-4.1-mini and ElevenLabs!

---

## Features

- Summarizes text into a conversational, podcast-style script
- Generates audio using ElevenLabs Text-to-Speech API
- Supports text input or uploading `.txt` files
- Downloadable MP3 podcast files
- Streamlit web interface for easy use

---

## Requirements

- Python 3.10+
- `.env` file with your API keys:
  - `OPENAI_API_KEY=your_openai_api_key`
  - `ELEVENLABS_API_KEY=your_elevenlabs_api_key`
 
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage 

- 1. Run the app : 
```bash
streamlit run main.py
```
- 2. Enter text or upload a .txt file
- 3. Click Generate Podcast
- 4. Listen or download your podcast

## Folder Structure
```
├── podcasts/          # Generated audio files
├── main.py            # Streamlit app
├── .env               # API keys 
└──  requirements.txt
```

## Future Works 

- Add multilingual support: generate audio in languages like Telugu, Hindi, and other regional languages.

- Improve voice customization and style options.

- Support batch processing of multiple files at once.

- Add more AI agent features like emotion-based narration or storytelling style.


---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.



