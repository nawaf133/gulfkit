import re

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")

COUNTRIES = {
    "SA": ("966", r"5\d{8}", "السعودية"),
    "AE": ("971", r"5[024568]\d{7}", "الإمارات"),
    "KW": ("965", r"[569]\d{7}", "الكويت"),
    "QA": ("974", r"[3567]\d{7}", "قطر"),
    "BH": ("973", r"[36]\d{7}", "البحرين"),
    "OM": ("968", r"[79]\d{7}", "عمان"),
}

IBAN_LENGTHS = {"SA": 24, "AE": 23, "KW": 30, "QA": 29, "BH": 22, "OM": 23}


def normalize_digits(text):
    return str(text).translate(_DIGITS)


def saudi_id(value):
    v = normalize_digits(value).strip()
    if not re.fullmatch(r"\d{10}", v):
        return False, "لازم يكون 10 أرقام"
    if v[0] not in "12":
        return False, "لازم يبدأ بـ 1 (مواطن) أو 2 (مقيم)"
    total = 0
    for i, ch in enumerate(v):
        n = int(ch)
        if i % 2 == 0:
            n *= 2
            total += n // 10 + n % 10
        else:
            total += n
    if total % 10:
        return False, "رقم التحقق غلط"
    return True, "هوية وطنية" if v[0] == "1" else "إقامة"


def _match_international(s):
    for code, (prefix, pattern, _) in COUNTRIES.items():
        if s.startswith(prefix) and re.fullmatch(pattern, s[len(prefix):]):
            return code
    return None


def phone(value, default="SA"):
    if default not in COUNTRIES:
        return False, "الدولة غير مدعومة: " + default
    s = re.sub(r"[\s\-().]", "", normalize_digits(value))
    intl = False
    if s.startswith("+"):
        s, intl = s[1:], True
    elif s.startswith("00"):
        s, intl = s[2:], True

    if not s.isdigit():
        return False, "الرقم فيه حروف أو رموز غلط"

    code = None
    if intl or not s.startswith("0"):
        code = _match_international(s)
    if code is None and not intl:
        prefix, pattern, _ = COUNTRIES[default]
        local = s[1:] if s.startswith("0") else s
        if re.fullmatch(pattern, local):
            s, code = prefix + local, default
    if code is None:
        return False, "الرقم ما يطابق صيغة جوال خليجي"
    prefix, _, name = COUNTRIES[code]
    return True, "+{} ({})".format(s, name)


def iban(value):
    s = re.sub(r"\s", "", str(value)).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{11,30}", s):
        return False, "الصيغة غلط"
    cc = s[:2]
    expected = IBAN_LENGTHS.get(cc)
    if expected and len(s) != expected:
        return False, "الطول لازم يكون {} للدولة {}".format(expected, cc)
    moved = s[4:] + s[:4]
    digits = "".join(str(int(c, 36)) for c in moved)
    if int(digits) % 97 != 1:
        return False, "رقم التحقق غلط"
    grouped = " ".join(s[i:i + 4] for i in range(0, len(s), 4))
    return True, grouped
