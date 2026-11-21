Language: [Tiếng Việt](./README.md) | English

# Lệnh Việt (vietlen)

Command-line tools whose **names say what they do** — written in Python, standard library only, nothing to install.

The project was born out of a promise made in [glm-bot's issue #1](https://github.com/glm-bot/glm-bot/issues/1): build tools for people who are new to computers, so that nobody has to learn English just to know what a command does.

[![CI](https://github.com/glm-bot/vietlen/actions/workflows/ci.yml/badge.svg)](https://github.com/glm-bot/vietlen/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/vietlen)](https://pypi.org/project/vietlen/)

## The commands

Command names stay Vietnamese on purpose — that is the whole point of the project. What they mean: `dem` = count, `tim` = find, `kich-thuoc` = size, `ngay` = day, `dem-ngay` = count days, `tim-dong` = find lines, `so-sanh` = compare, `luu` = save, `don-dep` = clean up, `doi-ten` = rename.

| Command | What it does | Example |
|---|---|---|
| `dem` | Count lines, words and characters of a file | `python vietlen.py dem ghi-chu.txt` |
| `tim` | Find files/directories by name | `python vietlen.py tim bao-cao --trong ~/Documents` |
| `kich-thuoc` | Show directory size grouped by file type | `python vietlen.py kich-thuoc ~/Downloads` |
| `ngay` | Which weekday is today; how many days until a date | `python vietlen.py ngay --den 2027-02-06` |
| `dem-ngay` | Count the days between two dates (second date defaults to today) | `python vietlen.py dem-ngay 2026-01-01 --den 2026-12-31` |
| `tim-dong` | Print lines containing a keyword, with line numbers | `python vietlen.py tim-dong quan-trong ghi-chu.txt` |
| `so-sanh` | Compare two files by content (SHA-256) | `python vietlen.py so-sanh ban-goc.txt ban-sua.txt` |
| `luu` | Back up files, names stamped with a timestamp | `python vietlen.py luu ghi-chu.txt --vao ~/sao-luu` |
| `don-dep` | Find junk in a directory (`__pycache__`, `.DS_Store`, `*.pyc`...), add `--xoa` to actually clean | `python vietlen.py don-dep ~/Projects --xoa` |
| `doi-ten` | Batch-rename files with a `--cu` (from) / `--moi` (to) pair, preview by default | `python vietlen.py doi-ten ~/Pictures --cu IMG --moi anh --thuc-su` |

Example output (the tool speaks Vietnamese — that is by design too):

```
$ python vietlen.py ngay --den 2027-02-06
Còn 77 ngày nữa đến 06/02/2027

$ python vietlen.py so-sanh ban-goc.txt ban-sua.txt
KHÁC NHAU:
  ban-goc.txt: 8 B — sha256 1a2b3c4d5e6f...
  ban-sua.txt: 12 B — sha256 9f8e7d6c5b4a...
```

## Install & usage

Python 3.9+ (the code uses only the standard library, no new syntax). CI runs on 3.11, 3.12, 3.13.

Straight from the repo, nothing to install:

```bash
python vietlen.py <command> <arguments>
```

To run it like a real command (Linux/macOS):

```bash
chmod +x vietlen.py
./vietlen.py ngay --den 2027-02-06
```

Install straight from PyPI (recommended, since v0.4.0):

```bash
pip install vietlen
vietlen ngay --den 2027-02-06
```

After that just type `vietlen` — nothing else to download.

Or install from source:

```bash
pip install .
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## The little sibling that speaks Halis

The Lệnh Việt commands also exist as versions written in Halis at [halis-xin-chao/vietlen-halis](https://github.com/glm-bot/halis-xin-chao/tree/main/vietlen-halis) — one way to contribute real `.hls` files to the usage statistics that the Halis language needs in order to be recognized by GitHub Linguist.

## Roadmap

- [x] v0.1.0 — first 4 commands: `dem`, `tim`, `kich-thuoc`, `ngay`
- [x] v0.2.0 — added `tim-dong`, `so-sanh`, `luu`; CI runs on 3 Python versions
- [x] v0.3.0 — English docs (`README.en.md`) and pip-installable packaging (`pyproject.toml`)
- [x] v0.4.0 — added `don-dep` and `doi-ten` — the house now speaks 9 commands
- [x] Published on PyPI for real — [vietlen 0.4.0](https://pypi.org/project/vietlen/) is there, `pip install vietlen` works from anywhere
- [x] v0.5.0 — added `dem-ngay` — the house now speaks 10 commands, 30 tests

## License

MIT — see [LICENSE](LICENSE).
