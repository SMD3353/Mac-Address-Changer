import base64
import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

from menu import MENU, RESTAURANT_DETAILS, format_menu_for_prompt

app = Flask(__name__)

load_dotenv()

_client: OpenAI | None = None


def get_openai_client() -> OpenAI:
    """Return an OpenAI client if the API key is available."""
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable is missing. "
                "Set it before using the chat or voice endpoints."
            )
        _client = OpenAI(api_key=api_key)
    return _client


SYSTEM_PROMPT = """
You are Harmony, the helpful ordering assistant for {name}. Guide guests through the
menu, answer questions about ingredients, and help them build complete orders.
Always mention current specials when relevant, offer suggestions for sides or
pairings, and confirm the full order before finishing. Prices are listed in USD.

Respond in a friendly, conversational tone. If a request cannot be fulfilled,
politely explain why and suggest alternatives when possible.

Menu:
{menu}
""".strip()


def build_message_history(history: List[Dict[str, Any]], user_message: str | None = None) -> List[Dict[str, Any]]:
    """Prepare the message payload for the OpenAI Responses API."""
    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT.format(
                        name=RESTAURANT_DETAILS["name"],
                        menu=format_menu_for_prompt(MENU),
                    ),
                }
            ],
        }
    ]

    for entry in history:
        role = entry.get("role")
        text = entry.get("content", "")
        if role in {"user", "assistant"} and text:
            messages.append({"role": role, "content": [{"type": "text", "text": text}]})

    if user_message:
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_message,
                    }
                ],
            }
        )

    return messages


@app.route("/")
def index():
    return render_template("index.html", restaurant=RESTAURANT_DETAILS)


@app.route("/api/menu")
def api_menu():
    return jsonify(MENU)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    history = payload.get("history") or []

    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        client = get_openai_client()
        messages = build_message_history(history, message)
        response = client.responses.create(
            model="gpt-4o-mini",
            input=messages,
        )
        reply_text = response.output_text
    except Exception as exc:  # pragma: no cover - defensive programming
        return jsonify({"error": str(exc)}), 500

    return jsonify({"reply": reply_text})


@app.route("/api/voice", methods=["POST"])
def api_voice():
    audio_file = request.files.get("audio")
    history_raw = request.form.get("history")
    try:
        history = json.loads(history_raw) if history_raw else []
    except json.JSONDecodeError:
        history = []

    if audio_file is None:
        return jsonify({"error": "Audio input is required."}), 400

    try:
        client = get_openai_client()
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file,
        )
        transcript_text = transcription.text.strip()

        if not transcript_text:
            return jsonify({"error": "We could not understand that audio. Please try again."}), 400

        messages = build_message_history(history, transcript_text)
        chat_response = client.responses.create(
            model="gpt-4o-mini",
            input=messages,
        )
        reply_text = chat_response.output_text

        tts_response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=reply_text,
        )
        audio_base64 = base64.b64encode(tts_response.read()).decode("utf-8")
    except Exception as exc:  # pragma: no cover - defensive programming
        return jsonify({"error": str(exc)}), 500

    return jsonify(
        {
            "transcript": transcript_text,
            "reply": reply_text,
            "audio": f"data:audio/mp3;base64,{audio_base64}",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
