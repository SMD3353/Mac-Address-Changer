# Harmony Bites Interactive Ordering

This project delivers an immersive web experience for the fictional Harmony Bites restaurant. Guests can browse a vibrant seasonal menu, place orders via conversational chat, or speak directly with the Harmony assistant. Behind the scenes the site connects securely to OpenAI's API for natural language understanding, order building, and real-time voice transcription + narration.

> **Note**: The original `mac_changer.py` utility remains in the repository but is unrelated to the restaurant experience.

## Features

- Rich, mobile-friendly landing page showcasing the full menu.
- Chat-based ordering that remembers conversation history and keeps the assistant focused on the menu.
- Hands-free ordering powered by browser audio capture, Whisper transcription (`gpt-4o-transcribe`), and text-to-speech responses (`gpt-4o-mini-tts`).
- Centralized restaurant configuration (`menu.py`) so specials and descriptions stay consistent across chat and voice flows.

## Getting started

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Provide API credentials

Create a `.env` file at the project root (or export directly in your shell):

```bash
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run the development server

```bash
flask --app app run --debug
```

Open [http://localhost:5000](http://localhost:5000) in your browser to explore the site. Grant microphone permissions when prompted to try the voice ordering workflow.

## Environment variables

- `OPENAI_API_KEY` – required for all chat, transcription, and text-to-speech interactions.

## Additional scripts

- `mac_changer.py` – legacy script for changing MAC addresses on Linux systems. It is untouched by this work but retained for reference.
