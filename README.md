# gulfkit

A small command-line tool for developers working in Saudi Arabia and the Gulf. It bundles the things you end up rewriting in every regional project: ID, phone and IBAN validation, Hijri dates, currency formatting, VAT, and an RTL project starter. No dependencies, just Python.

![python](https://img.shields.io/badge/python-3.8%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

## Install

```bash
git clone https://github.com/nawaf133/gulfkit.git
cd gulfkit
pip install .
```

Requires Python 3.8 or newer.

```bash
gulfkit --version
```

## Commands

| Command | What it does |
|---------|--------------|
| `new`   | Create an RTL Arabic starter project (`web` or `flask` template) |
| `id`    | Validate a Saudi national ID or iqama number |
| `phone` | Validate a mobile number (SA, AE, KW, QA, BH, OM) |
| `iban`  | Validate an IBAN |
| `hijri` | Convert between Hijri and Gregorian dates |
| `money` | Format an amount in a Gulf currency |
| `vat`   | Calculate VAT |

Output messages are in Arabic.

## Usage

### New project

```bash
gulfkit new my-site
gulfkit new my-api -t flask
```

```
تم إنشاء المشروع my-site (web):
  my-site/index.html
  my-site/style.css
  my-site/script.js
```

The starter ships with `dir="rtl"`, the Tajawal font, and small helpers for SAR formatting and Umm al-Qura dates through the browser's `Intl` API.

### National ID / iqama

```bash
gulfkit id 1087654321
```

```
✔ هوية وطنية
```

An invalid number returns the reason:

```
✘ رقم التحقق غلط
```

This checks the format and the checksum only. It does not tell you whether the ID is actually registered to anyone.

### Phone numbers

Accepts the formats people actually type: `05xxxxxxxx`, `+9665xxxxxxxx`, `00966...`, and Arabic-Indic digits.

```bash
gulfkit phone 0501234567
gulfkit phone +971501234567
gulfkit phone 50012345 -c KW
```

```
✔ +966501234567 (السعودية)
✔ +971501234567 (الإمارات)
```

### IBAN

```bash
gulfkit iban "SA03 8000 0000 6080 1016 7519"
```

```
✔ SA03 8000 0000 6080 1016 7519
```

### Hijri dates

```bash
gulfkit hijri                          # today
gulfkit hijri 2026-10-09               # Gregorian to Hijri
gulfkit hijri 1447-09-01 --from-hijri  # Hijri to Gregorian
```

```
الجمعة 26 ربيع الثاني 1448هـ الموافق 9 أكتوبر 2026م
```

The conversion uses the tabular Islamic calendar, so it can be off by a day compared to the official Umm al-Qura calendar, especially around Ramadan and the Eids. Don't use it for anything official.

### Money

```bash
gulfkit money 1234.5
gulfkit money 1234.5 -c KWD
gulfkit money 1234.5 --ar-digits
```

```
1,234.50 ر.س
1,234.500 د.ك
١٬٢٣٤٫٥٠ ر.س
```

### VAT

```bash
gulfkit vat 100
gulfkit vat 115 --inclusive
gulfkit vat 200 -c AE
gulfkit vat 100 -c QA --rate 3
```

```
الصافي:   100.00 ر.س
الضريبة:  15.00 ر.س
الإجمالي: 115.00 ر.س
```

Default rates: Saudi Arabia 15%, UAE 5%, Bahrain 10%, Oman 5%. Kuwait and Qatar have no default, pass one with `--rate`. Rates change, so check them before relying on the output.

## Use as a library

```python
from datetime import date
from gulfkit import validators, hijri, money

validators.saudi_id("1087654321")   # (True, 'هوية وطنية')
validators.phone("0501234567")      # (True, '+966501234567 (السعودية)')
validators.iban("SA0380000000608010167519")

hijri.describe(date.today())
money.fmt("1999.9", "SAR")
```

## Exit codes

The validation commands exit with `0` when the input is valid and `1` when it isn't, so they work in scripts:

```bash
if gulfkit id "$ID" > /dev/null; then
  echo "valid"
fi
```

## Notes

- If Arabic text shows up reversed or disconnected, use a terminal with bidi support (Windows Terminal, iTerm2, GNOME Terminal).
- For anything official, go to the relevant authority (Absher, ZATCA, your bank).

## Tests

```bash
pip install pytest
pytest
```

## Contributing

Bug reports and pull requests are welcome. If you add a feature, add a test with it.

Ideas I haven't built yet: numbers to Arabic words ("one hundred and twenty-five riyals"), commercial registration and VAT number validation, more starter templates (FastAPI, Next.js).

## License

MIT
