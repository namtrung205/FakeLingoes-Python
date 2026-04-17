# FakeLingoes 🚀

[![Build and Package](https://github.com/namtrung205/FakeLingoes-Python/actions/workflows/build.yml/badge.svg)](https://github.com/namtrung205/FakeLingoes-Python/actions/workflows/build.yml)

**FakeLingoes** là một công cụ từ điển và dịch thuật đa nền tảng (Windows & Linux) mạnh mẽ, hỗ trợ dịch nhanh qua chụp ảnh màn hình (OCR), dịch văn bản và phát âm (TTS).

---

## ✨ Tính năng chính

- 🌍 **Đa nền tảng**: Hỗ trợ đầy đủ trên Windows và Linux (Ubuntu/WSL).
- 📸 **Dịch chụp màn hình (OCR)**: Chụp một vùng màn hình để nhận diện chữ và dịch ngay lập tức (hỗ trợ Tesseract Offline và SpaceOCR Online).
- 🔊 **Phát âm (TTS)**: Hỗ trợ giọng đọc Google (Online) và Espeak (Offline).
- 📋 **Dịch tự động từ Clipboard**: Lắng nghe thay đổi clipboard để dịch nhanh khi bạn copy văn bản.
- 📥 **Tra từ điển Offline**: Tích hợp bộ từ điển Anh-Việt có sẵn.
- 🎨 **Giao diện hiện đại**: Hỗ trợ Dark Mode, cửa sổ không viền, luôn hiển thị trên cùng (Stay on Top) và ẩn xuống Tray (System Tray).

---

## 🚀 Hướng dẫn cài đặt & Sử dụng

### Dành cho người dùng (Download)
Bạn có thể tải bản cài đặt mới nhất tại mục [Releases](https://github.com/namtrung205/FakeLingoes-Python/releases):
- **Windows**: Tải file `.exe` và chạy để cài đặt.
- **Ubuntu/Linux**: Tải file `.deb` và cài đặt lệnh:
  ```bash
  sudo apt install ./fakelingoes_0.0.x_amd64.deb
  ```

### Dành cho Lập trình viên (Chạy từ source)

#### Trên Windows:
1. Chạy `setup.bat` để tạo môi trường ảo và cài đặt thư viện.
2. Kích hoạt venv: `venv_win\Scripts\activate`
3. Chạy app: `python src/fake_lingoes/main.py`

#### Trên Linux:
1. Chạy script setup: `./scripts/setup_linux.sh`
2. Kích hoạt venv: `source venv_linux/bin/activate`
3. Chạy app: `python3 src/fake_lingoes/main.py`

---

## 🛠 Hướng dẫn Đóng gói (Build)

Dự án sử dụng **PyInstaller** để đóng gói thành file thực thi duy nhất.

### 1. Build thủ công

#### Trên Windows (Tạo file cài đặt .exe):
- Bạn cần cài đặt [Inno Setup](https://jrsoftware.org/isdl.php).
- Chạy lệnh build:
  ```bash
  pyinstaller FakeLingoes.spec
  ```
- Sau đó dùng Inno Setup mở file `Installer/installer.iss` để đóng gói bản setup.

#### Trên Linux (Tạo file cài đặt .deb):
- Đảm bảo đã chạy `scripts/setup_linux.sh`.
- Chạy script build chuyên dụng:
  ```bash
  ./scripts/build_deb.sh
  ```
- File `.deb` sẽ được tạo trong thư mục `Installer/`.

### 2. Tự động hóa với GitHub Actions
Dự án đã cấu hình sẵn quy trình **CI/CD** tự động hoàn toàn:
- Mỗi khi bạn push code hoặc đánh tag `v*` lên GitHub, hệ thống sẽ tự động build cả bản Windows (.exe) và Linux (.deb).
- Nếu push tag, file sẽ được tự động đẩy lên mục **Releases**.
- *Lưu ý*: Nhớ bật quyền `Read and write permissions` trong `Settings -> Actions -> General` của repository.

---

## ⌨️ Phím tắt mặc định

| Tính năng | Phím tắt |
| :--- | :--- |
| Dịch vùng chọn (Offline) | `Alt + W` |
| Dịch vùng chọn (Online API) | `Alt + I` |
| Hiện/Ẩn ứng dụng | `Alt + S` |
| Luôn ở trên cùng (Stay on Top) | `Alt + A` |
| Chế độ thu nhỏ/mở rộng | `Alt + Z` |
| Thoát ứng dụng | `Shift + Ctrl + Q` |

---

## 🤝 Đóng góp
Mọi ý đóng góp hoặc báo lỗi vui lòng mở **Issue** trên repository. Chúc bạn có trải nghiệm tốt với FakeLingoes!
