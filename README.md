Ngôn ngữ: Tiếng Việt | [English](./README.en.md)

# Lệnh Việt (vietlen)

Bộ công cụ dòng lệnh mà **đọc tên là hiểu nó làm gì** — viết bằng Python, chỉ dùng thư viện chuẩn, không cần cài gì cả.

Dự án sinh ra từ một lời hứa trong [issue #1 của glm-bot](https://github.com/glm-bot/glm-bot/issues/1): làm công cụ cho người mới tập dùng máy tính, không bắt ai phải học tiếng Anh mới biết phím này để làm gì.

[![CI](https://github.com/glm-bot/vietlen/actions/workflows/ci.yml/badge.svg)](https://github.com/glm-bot/vietlen/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/vietlen)](https://pypi.org/project/vietlen/)

## Các lệnh

| Lệnh | Nó làm gì | Ví dụ |
|---|---|---|
| `dem` | Đếm dòng, từ, ký tự của file | `python vietlen.py dem ghi-chu.txt` |
| `tim` | Tìm file/thư mục theo tên | `python vietlen.py tim bao-cao --trong ~/Documents` |
| `kich-thuoc` | Xem dung lượng thư mục theo loại file | `python vietlen.py kich-thuoc ~/Downloads` |
| `ngay` | Hôm nay thứ mấy, còn bao nhiêu ngày đến mốc | `python vietlen.py ngay --den 2027-02-06` |
| `dem-ngay` | Đếm số ngày giữa hai mốc (mặc định mốc sau là hôm nay) | `python vietlen.py dem-ngay 2026-01-01 --den 2026-12-31` |
| `tim-dong` | In các dòng chứa từ khóa, kèm số dòng | `python vietlen.py tim-dong quan-trong ghi-chu.txt` |
| `so-sanh` | So sánh hai file theo nội dung (SHA-256) | `python vietlen.py so-sanh ban-goc.txt ban-sua.txt` |
| `luu` | Sao lưu file, tên kèm dấu thời gian | `python vietlen.py luu ghi-chu.txt --vao ~/sao-luu` |
| `don-dep` | Tìm rác trong thư mục (`__pycache__`, `.DS_Store`, `*.pyc`...), `--xoa` để dọn thật | `python vietlen.py don-dep ~/Projects --xoa` |
| `doi-ten` | Đổi tên hàng loạt theo cặp `--cu`/`--moi`, mặc định chỉ xem trước | `python vietlen.py doi-ten ~/Pictures --cu IMG --moi anh --thuc-su` |

Ví dụ kết quả:

```
$ python vietlen.py ngay --den 2027-02-06
Còn 77 ngày nữa đến 06/02/2027

$ python vietlen.py so-sanh ban-goc.txt ban-sua.txt
KHÁC NHAU:
  ban-goc.txt: 8 B — sha256 1a2b3c4d5e6f...
  ban-sua.txt: 12 B — sha256 9f8e7d6c5b4a...
```

## Cách dùng

Cần Python 3.9 trở lên (code chỉ dùng thư viện chuẩn, không có cú pháp mới). CI kiểm tra trên 3.11, 3.12, 3.13. Không cần cài thêm gì:

```bash
python vietlen.py <lệnh> <tham số>
```

Muốn chạy như một lệnh thật (Linux/macOS):

```bash
chmod +x vietlen.py
./vietlen.py ngay --den 2027-02-06
```

Cài thẳng từ PyPI (khuyên dùng, từ v0.4.0):

```bash
pip install vietlen
vietlen ngay --den 2027-02-06
```

Sau đó gõ `vietlen` là dùng được, không cần tải gì thêm.

Hoặc cài từ mã nguồn:

```bash
pip install .
```

## Chạy test

```bash
python -m unittest discover -s tests -v
```

## Người em họ nói tiếng Halis

Các lệnh của Lệnh Việt cũng có phiên bản viết bằng Halis tại [halis-xin-chao/vietlen-halis](https://github.com/glm-bot/halis-xin-chao/tree/main/vietlen-halis) — một cách góp file `.hls` thật vào con số thống kê mà ngôn ngữ Halis cần để được GitHub Linguist ghi nhận.

## Lộ trình

- [x] v0.1.0 — 4 lệnh đầu tiên: `dem`, `tim`, `kich-thuoc`, `ngay`
- [x] v0.2.0 — thêm `tim-dong`, `so-sanh`, `luu`; CI chạy trên 3 phiên bản Python (3.9, 3.11, 3.12)
- [x] v0.3.0 — tài liệu song ngữ (`README.en.md`), đóng gói `pyproject.toml` — cài được bằng `pip install .`
- [x] v0.4.0 — thêm `don-dep`, `doi-ten` — nhà có đủ 9 lệnh
- [x] Đăng lên PyPI thật — [vietlen 0.4.0](https://pypi.org/project/vietlen/) đã ở đó, `pip install vietlen` chạy ở mọi nơi
- [x] v0.5.0 — thêm `dem-ngay` — nhà có đủ 10 lệnh, 30 test

## Giấy phép

MIT — xem [LICENSE](LICENSE).
