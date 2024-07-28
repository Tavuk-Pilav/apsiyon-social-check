import os
import re
import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def get_blacklist():
    url = "https://api.github.com/repos/ooguz/turkce-kufur-karaliste/contents/karaliste.txt"
    response = requests.get(url)
    if response.status_code == 200:
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        blacklist = content.split('\n')
        return [word.strip() for word in blacklist if word.strip()]
    else:
        raise Exception("GitHub'dan veri çekilemedi.")

def check_content(text):
    blacklist = get_blacklist()
    pattern = r'\b(' + '|'.join(re.escape(word) for word in blacklist) + r')\b'
    if re.search(pattern, text, re.IGNORECASE):
        return "Uygunsuz"
    else:
        return "Uygun"

def analyze_sentiment(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Verilen metni analiz et ve şu kategorilerden birine yerleştir: Uygun, Uygunsuz, Saldırgan, Kötümser, Kinayeli. Eğer 'Uygun' değilse, neden olduğuna dair kısa, tek cümlelik bir açıklama yap."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def analyze_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Bu görüntüyü analiz et ve uygunluğunu değerlendir. Şu kategorilerden birine yerleştir: Uygun, Uygunsuz, Saldırgan, Kötümser, Kinayeli. Eğer 'Uygun' değilse, neden olduğuna dair kısa, tek cümlelik bir açıklama yap."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def analyze_text(text):
    blacklist_result = check_content(text)
    if blacklist_result == "Uygun":
        sentiment_analysis = analyze_sentiment(text)
        sentiment_parts = sentiment_analysis.split('.')
        sentiment_category = sentiment_parts[0].strip()
        if sentiment_category == "Uygun":
            return "Metin onaylandı.", sentiment_category, ""
        else:
            feedback = sentiment_parts[1].strip() if len(sentiment_parts) > 1 else ""
            return f"Metin onaylanmadı.", sentiment_category, feedback
    else:
        return "Metin kara liste kontrolünden geçemedi.", "Uygunsuz", "Kara listedeki kelime kullanımı"

def analyze_image_content(image_path):
    image_analysis = analyze_image(image_path)
    image_parts = image_analysis.split('.')
    image_category = image_parts[0].strip()
    if image_category == "Uygun":
        return "Görsel onaylandı.", image_category, ""
    else:
        feedback = image_parts[1].strip() if len(image_parts) > 1 else ""
        return f"Görsel onaylanmadı.", image_category, feedback

if __name__ == "__main__":
    text_result, text_category, text_feedback = analyze_text("Apartman o kadar başarılı ki neredeyse hiçbir şey doğru gitmiyor")
    print(f"Sonuç: {text_result}")
    print(f"Kategori: {text_category}")
    print(f"Geri Bildirim: {text_feedback}")

    image_result, image_category, image_feedback = analyze_image_content("/home/enes/Desktop/Hackathon/Apsiyon_hackathon/social/check/image/27908_6.jpg")
    print(f"Sonuç: {image_result}")
    print(f"Kategori: {image_category}")
    print(f"Geri Bildirim: {image_feedback}")