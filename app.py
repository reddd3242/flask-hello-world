from flask import Flask, request, send_file
import pytesseract
from PIL import Image
from gtts import gTTS
import openai
import os

# API key gizli ortam değişkeninden alınmalı
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

# Ana rota testi için
@app.route('/')
def hello():
    return "✅ Server aktif! /upload için POST, /audio için GET kullan."

# Görsel yükleme ve yanıt üretme
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "❌ Görsel bulunamadı.", 400

    file = request.files['image']
    file.save("question.jpg")

    try:
        text = pytesseract.image_to_string(Image.open("question.jpg"))
        print("🧠 OCR Sonucu:", text)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        answer = response['choices'][0]['message']['content']
        print("🗨️ GPT Yanıtı:", answer)

        tts = gTTS(answer, lang="tr")
        tts.save("response.mp3")

        return "✅ Cevap hazır. /audio ile ses dosyasını çekebilirsin."
    
    except Exception as e:
        print("⚠️ Hata:", e)
        return "❌ Bir hata oluştu.", 500

# Ses dosyasını gönderme
@app.route('/audio')
def get_audio():
    if not os.path.exists("response.mp3"):
        return "❌ Ses dosyası bulunamadı. Önce /upload kullan.", 404

    return send_file("response.mp3", mimetype="audio/mpeg")

# Uygulama çalıştırma
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
