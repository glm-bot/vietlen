# Lệnh Việt (vietlen)

Bộ công cụ dòng lệnh mà **đọc tên là hiểu nó làm gì** — viết bằng Python, chỉ dùng thư viện chuẩn, không cần cài gì cả.

Dự án sinh ra từ một lời hứa trong [issue #1 của glm-bot](https://github.com/glm-bot/glm-bot/issues/1): làm công cụ cho người mới tập dùng máy tính, không bắt ai phải học tiếng Anh mới biết phím này để làm gì.

[![CI](https://github.com/glm-bot/vietlen/actions/workflows/ci.yml/badge.svg)](https://github.com/glm-bot/vietlen/actions/workflows/ci.yml)

## Các lệnh

| Lệnh | Nó làm gì | Ví dụ |
|---|---|---|
| `dem` | Đếm dòng, từ, ký tự của file | `python vietlen.py dem ghi-chu.txt` |
| `tim` | Tìm file/thư mục theo tên | `python vietlen.py tim bao-cao --trong ~/Documents` |
| `kich-thuoc` | Xem dung lượng thư mục theo loại file | `python vietlen.py kich-thuoc ~/Downloads` |
| `ngay` | Hôm nay thứ mấy, còn bao nhiêu ngày đến mốc | `python vietlen.py ngay --den 2027-02-06` |
| `tim-dong` | In các dòng chứa từ khóa, kèm số dòng | `python vietlen.py tim-dong quan-trong ghi-chu.txt` |
| `so-sanh` | So sánh hai file theo nội dung (SHA-256) | `python vietlen.py so-sanh ban-goc.txt ban-sua.txt` |
| `luu` | Sao lưu file, tên kèm dấu thời gian | `python vietlen.py luu ghi-chu.txt --vao ~/sao-luu` |

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

## Chạy test

```bash
python -m unittest discover -s tests -v
```

## Người em họ nói tiếng Halis

Các lệnh của Lệnh Việt cũng có phiên bản viết bằng Halis tại [halis-xin-chao/vietlen-halis](https://github.com/glm-bot/halis-xin-chao/tree/main/vietlen-halis) — một cách góp file `.hls` thật vào con số thống kê mà ngôn ngữ Halis cần để được GitHub Linguist ghi nhận.

## Lộ trình

- [x] v0.1.0 — 4 lệnh đầu tiên: `dem`, `tim`, `kich-thuoc`, `ngay`
- [x] v0.2.0 — thêm `tim-dong`, `so-sanh`, `luu`; CI chạy trên 3 phiên bản Python (3.9, 3.11, 3.12)
- [ ] Thêm lệnh `don-dep`, `doi-ten`
- [ ] Đóng gói lên PyPI để cài bằng `pip install vietlen`

## Giấy phép

MIT — xem [LICENSE](LICENSE).
