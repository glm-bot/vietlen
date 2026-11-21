#!/usr/bin/env python3
"""vietlen — bộ lệnh dòng lệnh tiếng Việt: đọc tên là hiểu nó làm gì.

Chỉ dùng thư viện chuẩn của Python (3.9+). Gồm các lệnh:
    dem          đếm dòng, từ, ký tự của file
    tim          tìm file/thư mục theo tên
    kich-thuoc   xem dung lượng thư mục theo loại file
    ngay         hôm nay là thứ mấy, còn bao nhiêu ngày đến mốc
    tim-dong     in các dòng chứa từ khóa, kèm số dòng
    so-sanh      so sánh hai file theo nội dung (SHA-256)
    luu          sao lưu file, tên kèm dấu thời gian
    don-dep      tìm rác trong thư mục (__pycache__, .DS_Store, *.pyc...), --xoa để dọn thật
    doi-ten      đổi tên hàng loạt theo cặp --cu/--moi, mặc định chỉ xem trước

Ví dụ:
    python vietlen.py dem ghi-chu.txt
    python vietlen.py tim bao-cao --trong ~/Documents
    python vietlen.py kich-thuoc ~/Downloads
    python vietlen.py ngay --den 2027-02-06
    python vietlen.py tim-dong quan-trong ghi-chu.txt
    python vietlen.py so-sanh ban-goc.txt ban-sua.txt
    python vietlen.py luu ghi-chu.txt --vao ~/sao-luu
    python vietlen.py don-dep ~/Projects --xoa
    python vietlen.py doi-ten ~/Pictures --cu IMG --moi anh --thuc-su
"""
import argparse
import datetime
import hashlib
import shutil
import sys
from pathlib import Path

THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]

THU_MUC_RAC = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
TEN_RAC = {".DS_Store", "Thumbs.db", "desktop.ini"}
DUOI_RAC = {".pyc", ".pyo", ".tmp", ".swp"}


def la_rac(p: Path) -> bool:
    """Nhận diện mục rác: thư mục cache, file hệ điều hành bỏ đi, file tạm."""
    if p.is_dir():
        return p.name in THU_MUC_RAC
    if p.name in TEN_RAC or p.name.endswith("~"):
        return True
    return p.suffix in DUOI_RAC


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


def cmd_tim_dong(args) -> None:
    """In các dòng trong file chứa từ khóa, kèm số thứ tự dòng."""
    p = Path(args.file).expanduser()
    if not p.is_file():
        raise SystemExit(f"tim-dong: không tìm thấy file '{args.file}'")
    tu_khoa = args.tu_khoa.lower()
    hits = 0
    for i, dong in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if tu_khoa in dong.lower():
            print(f"{i}: {dong}")
            hits += 1
    print(f"\ntìm thấy {hits} dòng chứa '{args.tu_khoa}' trong {p.name}")


def cmd_so_sanh(args) -> None:
    """So sánh hai file: giống hệt hay khác nhau (theo SHA-256)."""
    p1, p2 = Path(args.file1).expanduser(), Path(args.file2).expanduser()
    for p in (p1, p2):
        if not p.is_file():
            raise SystemExit(f"so-sanh: không tìm thấy file '{p}'")
    h1 = hashlib.sha256(p1.read_bytes()).hexdigest()
    h2 = hashlib.sha256(p2.read_bytes()).hexdigest()
    if h1 == h2:
        print(f"GIỐNG HỆT: {p1.name} và {p2.name} cùng nội dung ({doc_dung_luong(p1.stat().st_size)})")
    else:
        print("KHÁC NHAU:")
        print(f"  {p1.name}: {doc_dung_luong(p1.stat().st_size)} — sha256 {h1[:12]}...")
        print(f"  {p2.name}: {doc_dung_luong(p2.stat().st_size)} — sha256 {h2[:12]}...")


def cmd_luu(args) -> None:
    """Sao lưu file vào thư mục đích, tên file kèm dấu thời gian."""
    muc_dich = Path(args.vao).expanduser().resolve() if args.vao else Path.cwd() / "ban-sao-luu"
    muc_dich.mkdir(parents=True, exist_ok=True)
    thoi_gian = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    da_luu = 0
    for ten in args.file:
        p = Path(ten).expanduser()
        if not p.is_file():
            print(f"luu: không tìm thấy file '{ten}'", file=sys.stderr)
            continue
        moi = muc_dich / f"{p.stem}_{thoi_gian}{p.suffix}"
        shutil.copy2(p, moi)
        print(f"đã lưu {p.name} -> {moi}")
        da_luu += 1
    print(f"\n({da_luu} file đã được sao lưu lúc {thoi_gian})")


def cmd_don_dep(args) -> None:
    """Tìm rác trong thư mục. Với --xoa thì dọn thật, không thì chỉ liệt kê."""
    root = Path(args.thu_muc).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"don-dep: không tìm thấy thư mục '{args.thu_muc}'")
    rac = [p for p in sorted(root.rglob("*")) if la_rac(p)]
    if not rac:
        print(f"{root}: sạch bong, không có rác nào")
        return
    for p in rac:
        print(f"  {p}{'/' if p.is_dir() else ''}")
    dung_luong = sum(p.stat().st_size for p in rac if p.is_file())
    print(f"\ntìm thấy {len(rac)} mục rác, {doc_dung_luong(dung_luong)}")
    if not args.xoa:
        print("chạy lại với --xoa để dọn thật")
        return
    da_xoa = 0
    for p in rac:
        if not p.exists():
            continue  # đã bị dọn theo thư mục cha
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            da_xoa += 1
        except OSError as loi:
            print(f"don-dep: không xóa được {p} ({loi})", file=sys.stderr)
    print(f"đã dọn {da_xoa} mục — thư mục giờ sạch hơn")


def cmd_doi_ten(args) -> None:
    """Đổi tên hàng loạt: thay --cu bằng --moi trong tên file. Mặc định chỉ xem trước."""
    root = Path(args.thu_muc).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"doi-ten: không tìm thấy thư mục '{args.thu_muc}'")
    cap_doi = []
    for p in sorted(root.iterdir()):
        if not p.is_file() or args.cu not in p.name:
            continue
        ten_moi = p.name.replace(args.cu, args.moi)
        if ten_moi != p.name:
            cap_doi.append((p, root / ten_moi))
    if not cap_doi:
        print(f"{root}: không có file nào chứa '{args.cu}' trong tên")
        return
    for cu, moi in cap_doi:
        print(f"  {cu.name} -> {moi.name}")
    print(f"\n{len(cap_doi)} file sẽ được đổi tên")
    if not args.thuc_su:
        print("chạy lại với --thuc-su để đổi thật")
        return
    da_doi = 0
    for cu, moi in cap_doi:
        if moi.exists():
            i = 1
            while moi.with_name(f"{moi.stem}_{i}{moi.suffix}").exists():
                i += 1
            moi = moi.with_name(f"{moi.stem}_{i}{moi.suffix}")
            print(f"  (tên đã có, né sang {moi.name})")
        cu.rename(moi)
        da_doi += 1
    print(f"đã đổi tên {da_doi} file")


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

    t2 = sub.add_parser("tim-dong", help="in các dòng chứa từ khóa, kèm số dòng")
    t2.add_argument("tu_khoa", help="từ khóa cần tìm (không phân biệt hoa thường)")
    t2.add_argument("file", help="file cần tìm trong đó")
    t2.set_defaults(func=cmd_tim_dong)

    s = sub.add_parser("so-sanh", help="so sánh hai file theo nội dung (SHA-256)")
    s.add_argument("file1")
    s.add_argument("file2")
    s.set_defaults(func=cmd_so_sanh)

    l = sub.add_parser("luu", help="sao lưu file, tên kèm dấu thời gian")
    l.add_argument("file", nargs="+", help="file cần sao lưu")
    l.add_argument("--vao", help="thư mục đích (mặc định: ban-sao-luu/)")
    l.set_defaults(func=cmd_luu)

    d2 = sub.add_parser("don-dep", help="tìm rác trong thư mục, --xoa để dọn thật")
    d2.add_argument("thu_muc", help="thư mục cần dọn")
    d2.add_argument("--xoa", action="store_true", help="xóa thật (mặc định chỉ liệt kê)")
    d2.set_defaults(func=cmd_don_dep)

    n2 = sub.add_parser("doi-ten", help="đổi tên hàng loạt theo cặp --cu/--moi")
    n2.add_argument("thu_muc", help="thư mục chứa file cần đổi tên")
    n2.add_argument("--cu", required=True, help="đoạn tên cần thay trong tên file")
    n2.add_argument("--moi", default="", help="đoạn tên thay vào (mặc định: xóa hẳn)")
    n2.add_argument("--thuc-su", action="store_true", help="đổi thật (mặc định chỉ xem trước)")
    n2.set_defaults(func=cmd_doi_ten)

    args = p.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
