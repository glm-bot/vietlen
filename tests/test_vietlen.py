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


class TestTimDong(unittest.TestCase):
    def test_tim_dong(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "nhat-ky.txt"
            f.write_text("hom nay nang dep\nhom mai mua\nhom qua gio\n", encoding="utf-8")
            out = chay(["tim-dong", "hom", str(f)])
            self.assertIn("1: hom nay nang dep", out)
            self.assertIn("2: hom mai mua", out)
            self.assertIn("3: hom qua gio", out)
            self.assertIn("tìm thấy 3 dòng", out)

    def test_tim_dong_khong_khop(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.txt"
            f.write_text("khong co gi\n", encoding="utf-8")
            out = chay(["tim-dong", "blabla", str(f)])
            self.assertIn("tìm thấy 0 dòng", out)

    def test_tim_dong_khong_phan_biet_hoa_thuong(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.txt"
            f.write_text("Quan Trong Lam\n", encoding="utf-8")
            out = chay(["tim-dong", "QUAN", str(f)])
            self.assertIn("Quan Trong Lam", out)


class TestSoSanh(unittest.TestCase):
    def test_giong_het(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.txt"
            b = Path(tmp) / "b.txt"
            a.write_text("noi dung giong nhau\n", encoding="utf-8")
            b.write_text("noi dung giong nhau\n", encoding="utf-8")
            out = chay(["so-sanh", str(a), str(b)])
            self.assertIn("GIỐNG HỆT", out)

    def test_khac_nhau(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.txt"
            b = Path(tmp) / "b.txt"
            a.write_text("ban goc\n", encoding="utf-8")
            b.write_text("ban da sua\n", encoding="utf-8")
            out = chay(["so-sanh", str(a), str(b)])
            self.assertIn("KHÁC NHAU", out)


class TestLuu(unittest.TestCase):
    def test_luu_tao_ban_sao(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "quan-trong.txt"
            f.write_text("du lieu quy gia\n", encoding="utf-8")
            out = chay(["luu", str(f), "--vao", str(Path(tmp) / "kho-sao-luu")])
            ban_sao = list((Path(tmp) / "kho-sao-luu").iterdir())
            self.assertEqual(len(ban_sao), 1)
            self.assertEqual(ban_sao[0].read_text(encoding="utf-8"), "du lieu quy gia\n")
            self.assertIn("đã lưu quan-trong.txt", out)
            self.assertIn(".txt", ban_sao[0].name)


class TestDonDep(unittest.TestCase):
    def test_tim_rac_chua_xoa(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "__pycache__").mkdir()
            (Path(tmp) / "__pycache__" / "mod.pyc").write_bytes(b"x")
            (Path(tmp) / ".DS_Store").write_bytes(b"y")
            (Path(tmp) / "giu-lai.txt").write_text("giu", encoding="utf-8")
            out = chay(["don-dep", tmp])
            self.assertIn("3 mục rác", out)
            self.assertIn("--xoa", out)
            self.assertTrue((Path(tmp) / "__pycache__").exists())

    def test_xoa_that(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "__pycache__").mkdir()
            (Path(tmp) / "__pycache__" / "mod.pyc").write_bytes(b"x")
            (Path(tmp) / ".DS_Store").write_bytes(b"y")
            (Path(tmp) / "giu-lai.txt").write_text("giu", encoding="utf-8")
            out = chay(["don-dep", tmp, "--xoa"])
            self.assertIn("đã dọn", out)
            self.assertFalse((Path(tmp) / "__pycache__").exists())
            self.assertFalse((Path(tmp) / ".DS_Store").exists())
            self.assertTrue((Path(tmp) / "giu-lai.txt").exists())

    def test_thu_muc_sach(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = chay(["don-dep", tmp])
            self.assertIn("sạch bong", out)

    def test_file_tam_duoi_khac(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "draf.tmp").write_bytes(b"x")
            (Path(tmp) / "sao.backup~").write_bytes(b"y")
            (Path(tmp) / "quan-trong.txt").write_text("giu", encoding="utf-8")
            out = chay(["don-dep", tmp])
            self.assertIn("2 mục rác", out)


class TestDoiTen(unittest.TestCase):
    def test_xem_truoc_mac_dinh(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "anh-IMG-1.jpg").write_bytes(b"x")
            (Path(tmp) / "anh-IMG-2.jpg").write_bytes(b"y")
            out = chay(["doi-ten", tmp, "--cu", "IMG", "--moi", "ca"])
            self.assertIn("anh-IMG-1.jpg -> anh-ca-1.jpg", out)
            self.assertIn("--thuc-su", out)
            self.assertTrue((Path(tmp) / "anh-IMG-1.jpg").exists())

    def test_doi_that(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "anh-IMG-1.jpg").write_bytes(b"x")
            (Path(tmp) / "anh-IMG-2.jpg").write_bytes(b"y")
            out = chay(["doi-ten", tmp, "--cu", "IMG", "--moi", "ca", "--thuc-su"])
            self.assertIn("đã đổi tên 2 file", out)
            self.assertTrue((Path(tmp) / "anh-ca-1.jpg").exists())
            self.assertFalse((Path(tmp) / "anh-IMG-1.jpg").exists())

    def test_ne_trung_ten_da_co(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.txt").write_text("cu", encoding="utf-8")
            (Path(tmp) / "b.txt").write_text("moi", encoding="utf-8")
            out = chay(["doi-ten", tmp, "--cu", "b", "--moi", "a", "--thuc-su"])
            self.assertIn("né sang", out)
            self.assertTrue((Path(tmp) / "a.txt").exists())
            self.assertEqual((Path(tmp) / "a.txt").read_text(encoding="utf-8"), "cu")
            self.assertTrue((Path(tmp) / "a_1.txt").exists())

    def test_khong_co_file_khop(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "x.txt").write_text("x", encoding="utf-8")
            out = chay(["doi-ten", tmp, "--cu", "zzz", "--moi", "y"])
            self.assertIn("không có file nào chứa", out)


if __name__ == "__main__":
    unittest.main()
