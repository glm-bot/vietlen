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

Ví dụ kết quả:

```
$ python vietlen.py ngay --den 2027-02-06
Còn 77 ngày nữa đến 06/02/2027
```

## Cách dùng

Cần Python 3.8 trở lên. Không cần cài thêm gì:

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

## Lộ trình

- [x] v0.1.0 — 4 lệnh đầu tiên: `dem`, `tim`, `kich-thuoc`, `ngay`
- [ ] Thêm lệnh `don-dep`, `doi-ten`, `luu` (sao lưu)
- [ ] Đóng gói lên PyPI để cài bằng `pip install vietlen`

## Giấy phép

MIT — xem [LICENSE](LICENSE).
