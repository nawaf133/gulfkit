from datetime import date

HIJRI_MONTHS = [
    "محرم", "صفر", "ربيع الأول", "ربيع الثاني", "جمادى الأولى", "جمادى الآخرة",
    "رجب", "شعبان", "رمضان", "شوال", "ذو القعدة", "ذو الحجة",
]

GREG_MONTHS = [
    "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
    "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر",
]

WEEKDAYS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]


def _to_jd(y, m, d):
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def _from_jd(jd):
    l = jd + 68569
    n = (4 * l) // 146097
    l -= (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    d = l - (2447 * j) // 80
    l = j // 11
    m = j + 2 - 12 * l
    y = 100 * (n - 49) + i + l
    return y, m, d


def to_hijri(g):
    l = _to_jd(g.year, g.month, g.day) - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    return y, m, d


def to_gregorian(y, m, d):
    if not (1 <= m <= 12 and 1 <= d <= 30 and y > 0):
        raise ValueError("تاريخ هجري غير صحيح")
    jd = (11 * y + 3) // 30 + 354 * y + 30 * m - (m - 1) // 2 + d + 1948440 - 385
    return date(*_from_jd(jd))


def describe(g):
    hy, hm, hd = to_hijri(g)
    return "{} {} {} {}هـ الموافق {} {} {}م".format(
        WEEKDAYS[g.weekday()], hd, HIJRI_MONTHS[hm - 1], hy,
        g.day, GREG_MONTHS[g.month - 1], g.year,
    )
