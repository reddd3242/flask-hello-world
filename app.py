from flask import Flask, request, send_file
import pytesseract
from PIL import Image
from gtts import gTTS
import openai
import os

# 🚫 API key'i koda gömmek yok! Environment'tan alınmalı:
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def hello():
    return "✅ Server aktif! /upload için POST, /audio için GET kullan."

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    file.save("question.jpg")

    text = pytesseract.image_to_string(Image.open("question.jpg"))
    print("OCR:", text)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    answer = response['choices'][0]['message']['content']
    print("Yanıt:", answer)

    tts = gTTS(answer, lang="tr")
    tts.save("response.mp3")

    return "✅ Cevap hazır."

@app.route('/audio')
def get_audio():
    return send_file("response.mp3", mimetype="audio/mpeg")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
