"""Test cho vietlen — chạy bằng: python -m unittest discover -s tests -v"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import vietlen


def chay(argv):
    """Chạy lệnh vietlen, trả về nội dung stdout."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        vietlen.main(argv)
    return buf.getvalue()


class TestDem(unittest.TestCase):
    def test_dem_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "ghi-chu.txt"
            f.write_text("xin chao vietnam\nhai ba muoi\n", encoding="utf-8")
            out = chay(["dem", str(f)])
            self.assertIn("2 dòng", out)
            self.assertIn("6 từ", out)
            self.assertIn("29 ký tự", out)

    def test_dem_nhieu_file_co_tong(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.txt"
            b = Path(tmp) / "b.txt"
            a.write_text("mot hai ba\n", encoding="utf-8")
            b.write_text("bon nam sau\n", encoding="utf-8")
            out = chay(["dem", str(a), str(b)])
            self.assertIn("tổng cộng (2 file)", out)

    def test_dem_file_khong_ton_tai(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = chay(["dem", str(Path(tmp) / "khong-co.txt")])
            self.assertEqual(out.strip(), "")


class TestTim(unittest.TestCase):
    def test_tim_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "bao-cao-quy-1.txt").write_text("x", encoding="utf-8")
            (Path(tmp) / "anh-nho.jpg").write_text("y", encoding="utf-8")
            out = chay(["tim", "bao-cao", "--trong", tmp])
            self.assertIn("bao-cao-quy-1.txt", out)
            self.assertIn("tìm thấy 1", out)

    def test_tim_khong_phan_biet_hoa_thuong(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "BaoCao.txt").write_text("x", encoding="utf-8")
            out = chay(["tim", "baocao", "--trong", tmp])
            self.assertIn("BaoCao.txt", out)


class TestKichThuoc(unittest.TestCase):
    def test_kich_thuoc_theo_loai(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("12345", encoding="utf-8")
            (Path(tmp) / "b.txt").write_text("1234567", encoding="utf-8")
            (Path(tmp) / "c.jpg").write_bytes(b"0123456789")
            out = chay(["kich-thuoc", tmp])
            self.assertIn(".txt", out)
            self.assertIn(".jpg", out)
            self.assertIn("TỔNG", out)
            self.assertIn("3 file", out)

    def test_thu_muc_khong_co_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = chay(["kich-thuoc", tmp])
            self.assertIn("không có file nào", out)


class TestNgay(unittest.TestCase):
    def test_hom_nay(self):
        out = chay(["ngay"])
        self.assertIn("Hôm nay là", out)
        self.assertIn(str(date.today().year), out)

    def test_den_ngay_tuong_lai(self):
        moc = date.today() + timedelta(days=10)
        out = chay(["ngay", "--den", moc.isoformat()])
        self.assertIn("Còn 10 ngày", out)

    def test_den_ngay_da_qua(self):
        moc = date.today() - timedelta(days=3)
        out = chay(["ngay", "--den", moc.isoformat()])
        self.assertIn("đã qua 3 ngày", out)

    def test_den_ngay_khong_hop_le(self):
        with self.assertRaises(SystemExit):
            chay(["ngay", "--den", "31/02/2027"])


if __name__ == "__main__":
    unittest.main()
