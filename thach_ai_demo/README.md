# Thach AI - Portfolio Chatbot (Python + Flask)

Bản demo dựa trên yêu cầu **Fullstack / AI ChatBot: thêm chatbot vào portfolio để trả lời về chủ nhân**, và lấy GitHub nhatanhng làm nguồn thông tin tham khảo. Đây là **ứng dụng mới**, không phải bản sao của repository GitHub.

## Tính năng
- Giao diện chat web phong cách tối, hỗ trợ điện thoại.
- Demo offline: tự trả lời một số câu hỏi về GitHub mà không cần API key.
- AI thật: kết nối Gemini API bằng key riêng, hỗ trợ lịch sử hội thoại ngắn.
- Lưu lịch sử chat trên trình duyệt (localStorage), tạo chat mới.
- Không cần microphone hoặc voice.

## Chạy Windows (PowerShell / CMD)
1. Cài Python 3.10+; mở terminal tại thư mục dự án.
2. `python -m pip install -r requirements.txt`
3. `copy .env.example .env` (trên Windows); với macOS/Linux: `cp .env.example .env`.
4. Muốn chat tự do: mở `.env` và đặt `GEMINI_API_KEY=KEY_MOI_CUA_BAN`.
5. `python app.py`
6. Mở http://127.0.0.1:5000

**Không có API key:** vẫn chạy giao diện + chatbot hỏi đáp từ các quy tắc demo. Không phải mô hình ngôn ngữ đầy đủ.

**Có API key:** sử dụng Gemini model chỉ định qua `GEMINI_MODEL` (phải là model API key được phép sử dụng). API có hạn mức và đôi khi tính phí tùy tài khoản. Nếu nhận lỗi 404/quota, thử model khả dụng khác trong Google AI Studio.

## Cá nhân hóa
Sửa `knowledge.txt` để đưa thông tin thật của bạn vào. Tên Nguyễn Nhật Anh ở dữ liệu mẫu là tên ghi trong repo `nhatanhng/intro`; không mặc định đây là tên của người cài đặt ứng dụng.

## Bảo mật
- Không chia sẻ hoặc commit file `.env` lên GitHub (đã có `.gitignore`).
- Nếu từng đăng API key lên chat hoặc nơi công khai, hãy **thu hồi và tạo key mới**.
- Bản mẫu chạy localhost, không có đăng nhập hoặc giới hạn request; bổ sung bảo vệ trước khi triển khai công khai.
