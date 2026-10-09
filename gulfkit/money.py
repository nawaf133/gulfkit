from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from .validators import normalize_digits

CURRENCIES = {
    "SAR": ("ر.س", 2),
    "AED": ("د.إ", 2),
    "KWD": ("د.ك", 3),
    "QAR": ("ر.ق", 2),
    "BHD": ("د.ب", 3),
    "OMR": ("ر.ع", 3),
}

COUNTRY_CURRENCY = {
    "SA": "SAR", "AE": "AED", "KW": "KWD",
    "QA": "QAR", "BH": "BHD", "OM": "OMR",
}

VAT_RATES = {"SA": Decimal("15"), "AE": Decimal("5"), "BH": Decimal("10"), "OM": Decimal("5")}

_ARABIC_OUT = str.maketrans("0123456789,.", "٠١٢٣٤٥٦٧٨٩٬٫")


def _decimal(value):
    text = normalize_digits(value).replace(",", "").replace("٬", "").replace("٫", ".")
    try:
        return Decimal(text.strip())
    except InvalidOperation:
        raise ValueError("المبلغ غلط: " + str(value))


def fmt(amount, currency="SAR", arabic_digits=False):
    if currency not in CURRENCIES:
        raise ValueError("عملة غير مدعومة: " + currency)
    symbol, places = CURRENCIES[currency]
    quant = Decimal(1).scaleb(-places)
    value = _decimal(amount).quantize(quant, ROUND_HALF_UP)
    text = "{:,.{}f}".format(value, places)
    if arabic_digits:
        text = text.translate(_ARABIC_OUT)
    return "{} {}".format(text, symbol)


def vat(amount, country="SA", rate=None, inclusive=False):
    if country not in COUNTRY_CURRENCY:
        raise ValueError("دولة غير مدعومة: " + country)
    if rate is None:
        if country not in VAT_RATES:
            raise ValueError("ما فيه ضريبة قيمة مضافة مسجلة لهذي الدولة، حدد النسبة بـ --rate")
        pct = VAT_RATES[country]
    else:
        pct = _decimal(rate)
    base = _decimal(amount)
    factor = pct / Decimal(100)
    if inclusive:
        net = base / (1 + factor)
        total = base
    else:
        net = base
        total = base * (1 + factor)
    return net, total - net, total
