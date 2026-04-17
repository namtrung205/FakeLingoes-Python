# Hướng dẫn chạy FakeLingoes trên Ubuntu WSL

Để chạy và test ứng dụng trên môi trường Ubuntu WSL, bạn hãy thực hiện theo các bước sau:

### 1. Truy cập vào thư mục dự án từ WSL
Mở terminal Ubuntu của bạn và di chuyển đến thư mục chứa code (WSL ánh xạ ổ `D:` vào `/mnt/d/`):
```bash
cd "/mnt/d/Work/Private/Python App/FakeLingoes-Python"
```

### 2. Cài đặt môi trường và thư viện hệ thống
Tôi đã chuẩn bị script `setup_linux.sh` để cài đặt Tesseract, thư viện âm thanh và các thư viện hỗ trợ giao diện (GUI).
```bash
# Cấp quyền thực thi
chmod +x scripts/setup_linux.sh

# Chạy script cài đặt (Nhập mật khẩu sudo của Ubuntu khi được hỏi)
./scripts/setup_linux.sh
```

### 3. Kích hoạt môi trường và chạy app
```bash
# Kích hoạt môi trường ảo (venv) vừa tạo
source venv_linux/bin/activate

# Chạy ứng dụng
python3 src/fake_lingoes/main.py
```

### Lưu ý cho WSL:
- **Hiển thị GUI**: Nếu bạn dùng Windows 11, cửa sổ app sẽ tự hiện ra (WSLg). Nếu dùng Windows 10 bản cũ, bạn có thể cần cài thêm [VcXsrv](https://sourceforge.net/projects/vcxsrv/) trên Windows.
- **Tính năng OCR**: Script setup đã cài `tesseract-ocr` thông qua `apt`, ứng dụng sẽ tự nhận diện lệnh `tesseract` để hoạt động.
- **Âm thanh**: Nếu gặp lỗi âm thanh, hãy thử cài thêm: `sudo apt install libasound2`.
