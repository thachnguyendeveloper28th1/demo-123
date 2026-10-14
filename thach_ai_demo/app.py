import os
import re
import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.json.ensure_ascii = False

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, 'knowledge.txt'), encoding='utf-8') as f:
    KNOWLEDGE = f.read()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '').strip()
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash').strip()


def demo_answer(message):
    q = message.casefold()
    if any(s in q for s in ('xin chào', 'hello', 'hi ', 'chào')):
        return 'Xin chào! Mình là trợ lý portfolio của Nguyễn Nhật Anh. Bạn có thể hỏi về GitHub, dự án hoặc cách liên hệ.'
    if any(s in q for s in ('tên', 'ai vậy', 'chủ nhân', 'giới thiệu', 'bạn là ai')):
        return 'Theo repository intro, chủ nhân profile GitHub nhatanhng tên là Nguyễn Nhật Anh. Mình là chatbot thử nghiệm giới thiệu portfolio này.'
    if any(s in q for s in ('github', 'liên kết', 'link', 'trang cá nhân')):
        return 'GitHub: https://github.com/nhatanhng . Các repository công khai được liệt kê trong file knowledge.txt.'
    if any(s in q for s in ('dự án', 'project', 'repo', 'đã làm', 'công nghệ', 'backend', 'frontend')):
        return ('Một số repository: ricedata-fe (dùng mẫu React + Vite), ricedata-be (có app.py và models.py), '
                'USTHOpenDotaClient, androiddev2023, pp2023 và intro. Xem https://github.com/nhatanhng')
    if any(s in q for s in ('liên hệ', 'email', 'điện thoại', 'contact')):
        return 'Thông tin liên hệ chưa được xác minh trong dữ liệu mẫu. Bạn có thể thêm email công khai của mình vào knowledge.txt.'
    return ('Hiện đang chạy chế độ Demo (không cần API key). Mình chỉ trả lời các câu hỏi cơ bản về portfolio. '
            'Để chat thông minh về mọi chủ đề, hãy thêm GEMINI_API_KEY vào file .env và chạy lại ứng dụng.')


def ai_answer(message, history):
    system_text = ('Bạn là trợ lý AI bằng tiếng Việt, thân thiện, ngắn gọn. Nếu người dùng hỏi về chủ nhân '
                   'portfolio, hãy chỉ dùng thông tin đã kiểm chứng trong phần DỮ LIỆU và nói rõ điều chưa biết; '
                   'không tự suy đoán đời tư. Với câu hỏi kiến thức chung, trả lời bình thường. '
                   'DỮ LIỆU PORTFOLIO:\n' + KNOWLEDGE)
    contents = []
    for m in history[-12:]:
        if not isinstance(m, dict):
            continue
        role, text = m.get('role'), m.get('text')
        if role in ('user', 'model') and isinstance(text, str) and text.strip():
            contents.append({'role': role, 'parts': [{'text': text[:4000]}]})
    contents.append({'role': 'user', 'parts': [{'text': message}]})
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent'
    resp = requests.post(url, headers={'x-goog-api-key': GEMINI_API_KEY}, json={
        'systemInstruction': {'parts': [{'text': system_text}]},
        'contents': contents,
        'generationConfig': {'temperature': 0.65, 'maxOutputTokens': 1000}
    }, timeout=45)
    if not resp.ok:
        try:
            detail = resp.json().get('error', {}).get('message', 'API không phản hồi thành công')
        except ValueError:
            detail = 'API không phản hồi thành công'
        raise RuntimeError(f'Gemini API HTTP {resp.status_code}: {detail[:250]}')
    data = resp.json()
    chunks = [part.get('text', '') for c in data.get('candidates', [])
              for part in c.get('content', {}).get('parts', []) if 'text' in part]
    if not chunks:
        raise RuntimeError('API không trả về nội dung văn bản. Vui lòng thử lại.')
    return ''.join(chunks)


@app.get('/')
def home():
    return render_template('index.html', mode='Gemini API' if GEMINI_API_KEY else 'Demo offline')


@app.post('/api/chat')
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    history = data.get('history', [])
    if not isinstance(message, str) or not message.strip():
        return jsonify(error='Hãy nhập câu hỏi.'), 400
    if len(message) > 4000 or not isinstance(history, list):
        return jsonify(error='Tin nhắn quá dài hoặc lịch sử không hợp lệ.'), 400
    try:
        answer = ai_answer(message.strip(), history) if GEMINI_API_KEY else demo_answer(message.strip())
        return jsonify(answer=answer, mode='gemini' if GEMINI_API_KEY else 'demo')
    except requests.RequestException:
        return jsonify(error='Không kết nối được Gemini API. Kiểm tra mạng và thử lại.'), 502
    except RuntimeError as e:
        return jsonify(error=str(e)), 502


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
