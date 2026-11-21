#!/usr/bin/env python3
"""vietlen — bộ lệnh dòng lệnh tiếng Việt: đọc tên là hiểu nó làm gì.

Chỉ dùng thư viện chuẩn của Python (3.8+). Gồm các lệnh:
    dem          đếm dòng, từ, ký tự của file
    tim          tìm file/thư mục theo tên
    kich-thuoc   xem dung lượng thư mục theo loại file
    ngay         hôm nay là thứ mấy, còn bao nhiêu ngày đến mốc

Ví dụ:
    python vietlen.py dem ghi-chu.txt
    python vietlen.py tim bao-cao --trong ~/Documents
    python vietlen.py kich-thuoc ~/Downloads
    python vietlen.py ngay --den 2027-02-06
"""
import argparse
import datetime
import sys
from pathlib import Path

THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def doc_dung_luong(n: int) -> str:
    f = float(n)
    for don_vi in ("B", "KB", "MB", "GB", "TB"):
        if f < 1024 or don_vi == "TB":
            return f"{f:.0f} {don_vi}" if don_vi == "B" else f"{f:.1f} {don_vi}"
        f /= 1024
    return f"{f:.1f} TB"


def cmd_dem(args) -> None:
    """Đếm dòng, từ, ký tự của một hoặc nhiều file."""
    tong_dong = tong_tu = tong_ky_tu = da_dem = 0
    for ten in args.file:
        p = Path(ten).expanduser()
        if not p.is_file():
            print(f"dem: không tìm thấy file '{ten}'", file=sys.stderr)
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        so_dong = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
        so_tu = len(text.split())
        so_ky_tu = len(text)
        print(f"{p.name}: {so_dong} dòng, {so_tu} từ, {so_ky_tu} ký tự")
        tong_dong += so_dong
        tong_tu += so_tu
        tong_ky_tu += so_ky_tu
        da_dem += 1
    if da_dem > 1:
        print(f"tổng cộng ({da_dem} file): {tong_dong} dòng, {tong_tu} từ, {tong_ky_tu} ký tự")


def cmd_tim(args) -> None:
    """Tìm file/thư mục theo tên, không phân biệt hoa thường."""
    if args.trong:
        root = Path(args.trong).expanduser().resolve()
        if not root.is_dir():
            raise SystemExit(f"tim: không tìm thấy thư mục '{args.trong}'")
    else:
        root = Path.cwd()
    ket_qua = []
    for p in sorted(root.rglob("*")):
        if args.ten.lower() in p.name.lower():
            ket_qua.append(p)
            if len(ket_qua) >= args.gioi_han:
                break
    for p in ket_qua:
        print(p)
    dau_cong = "+" if len(ket_qua) >= args.gioi_han else ""
    print(f"\ntìm thấy {len(ket_qua)}{dau_cong} kết quả khớp '{args.ten}' trong {root}")


def cmd_kich_thuoc(args) -> None:
    """Xem dung lượng thư mục, nhóm theo loại file."""
    root = Path(args.thu_muc).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"kich-thuoc: không tìm thấy thư mục '{args.thu_muc}'")
    thong_ke: dict = {}
    for p in root.rglob("*"):
        if p.is_file():
            loai = p.suffix.lower() if p.suffix else "(không đuôi)"
            so_luong, dung_luong = thong_ke.get(loai, (0, 0))
            thong_ke[loai] = (so_luong + 1, dung_luong + p.stat().st_size)
    if not thong_ke:
        print(f"{root}: không có file nào")
        return
    print(f"Dung lượng trong {root} (theo loại file):")
    for loai, (so_luong, dung_luong) in sorted(thong_ke.items(), key=lambda kv: -kv[1][1]):
        print(f"  {loai:<14} {so_luong:>5} file   {doc_dung_luong(dung_luong):>10}")
    tong_file = sum(sl for sl, _ in thong_ke.values())
    tong_dung_luong = sum(dl for _, dl in thong_ke.values())
    print(f"  {'TỔNG':<14} {tong_file:>5} file   {doc_dung_luong(tong_dung_luong):>10}")


def cmd_ngay(args) -> None:
    """Hôm nay thứ mấy, còn bao nhiêu ngày đến một mốc."""
    hom_nay = datetime.date.today()
    if not args.den:
        print(f"Hôm nay là {THU[hom_nay.weekday()]}, {hom_nay.strftime('%d/%m/%Y')}")
        return
    try:
        moc = datetime.date.fromisoformat(args.den)
    except ValueError:
        raise SystemExit(f"ngay: ngày '{args.den}' không hợp lệ (dạng chuẩn: 2027-02-06)")
    con_lai = (moc - hom_nay).days
    if con_lai > 0:
        print(f"Còn {con_lai} ngày nữa đến {moc.strftime('%d/%m/%Y')}")
    elif con_lai == 0:
        print("Ngày đó chính là hôm nay!")
    else:
        print(f"Ngày {moc.strftime('%d/%m/%Y')} đã qua {abs(con_lai)} ngày")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="vietlen",
        description="Bộ lệnh dòng lệnh tiếng Việt — đọc tên là hiểu nó làm gì.",
    )
    sub = p.add_subparsers(dest="lenh", required=True)

    q = sub.add_parser("dem", help="đếm dòng, từ, ký tự của file")
    q.add_argument("file", nargs="+", help="file cần đếm")
    q.set_defaults(func=cmd_dem)

    t = sub.add_parser("tim", help="tìm file/thư mục theo tên")
    t.add_argument("ten", help="đoạn tên cần tìm (không phân biệt hoa thường)")
    t.add_argument("--trong", help="thư mục để tìm (mặc định: thư mục hiện tại)")
    t.add_argument("--gioi-han", type=int, default=50, help="giới hạn số kết quả (mặc định: 50)")
    t.set_defaults(func=cmd_tim)

    k = sub.add_parser("kich-thuoc", help="xem dung lượng thư mục theo loại file")
    k.add_argument("thu_muc", help="thư mục cần xem")
    k.set_defaults(func=cmd_kich_thuoc)

    n = sub.add_parser("ngay", help="hôm nay thứ mấy, còn bao nhiêu ngày đến mốc")
    n.add_argument("--den", help="ngày cần đếm ngược tới (dạng 2027-02-06)")
    n.set_defaults(func=cmd_ngay)

    args = p.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
