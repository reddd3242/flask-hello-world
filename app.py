from flask import Flask, request, send_file
import pytesseract
from PIL import Image
from gtts import gTTS
import openai
import os

openai.api_key = os.environ.get("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")

app = Flask(__name__)

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
