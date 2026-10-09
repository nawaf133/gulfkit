import argparse
import sys
from datetime import date, datetime

from . import __version__, hijri, money, scaffold, validators


def _ok(msg):
    print("✔ " + msg)
    return 0


def _bad(msg):
    print("✘ " + msg)
    return 1


def cmd_new(args):
    try:
        files = scaffold.create(args.name, args.template, args.force)
    except ValueError as e:
        return _bad(str(e))
    print("تم إنشاء المشروع {} ({}):".format(args.name, args.template))
    for f in files:
        print("  " + f)
    return 0


def cmd_id(args):
    ok, info = validators.saudi_id(args.number)
    return _ok(info) if ok else _bad(info)


def cmd_phone(args):
    ok, info = validators.phone(args.number, args.country.upper())
    return _ok(info) if ok else _bad(info)


def cmd_iban(args):
    ok, info = validators.iban(args.value)
    return _ok(info) if ok else _bad(info)


def cmd_hijri(args):
    try:
        if args.from_hijri:
            if not args.value:
                return _bad("اكتب التاريخ الهجري بصيغة 1447-09-01")
            y, m, d = (int(p) for p in validators.normalize_digits(args.value).split("-"))
            g = hijri.to_gregorian(y, m, d)
        elif args.value:
            text = validators.normalize_digits(args.value)
            g = datetime.strptime(text, "%Y-%m-%d").date()
        else:
            g = date.today()
    except ValueError:
        return _bad("صيغة التاريخ غلط، استخدم YYYY-MM-DD")
    print(hijri.describe(g))
    return 0


def cmd_money(args):
    try:
        print(money.fmt(args.amount, args.currency.upper(), args.ar_digits))
    except ValueError as e:
        return _bad(str(e))
    return 0


def cmd_vat(args):
    country = args.country.upper()
    try:
        net, tax, total = money.vat(args.amount, country, args.rate, args.inclusive)
        cur = money.COUNTRY_CURRENCY[country]
        print("الصافي:   " + money.fmt(net, cur))
        print("الضريبة:  " + money.fmt(tax, cur))
        print("الإجمالي: " + money.fmt(total, cur))
    except ValueError as e:
        return _bad(str(e))
    return 0


def build_parser():
    p = argparse.ArgumentParser(
        prog="gulfkit",
        description="أدوات سريعة لمطوري السعودية والخليج",
    )
    p.add_argument("-v", "--version", action="version", version="gulfkit " + __version__)
    sub = p.add_subparsers(dest="command")

    s = sub.add_parser("new", help="ينشئ مشروع جاهز بإعدادات عربية RTL")
    s.add_argument("name")
    s.add_argument("-t", "--template", choices=sorted(scaffold.TEMPLATES), default="web")
    s.add_argument("--force", action="store_true")
    s.set_defaults(func=cmd_new)

    s = sub.add_parser("id", help="تحقق من رقم الهوية الوطنية أو الإقامة")
    s.add_argument("number")
    s.set_defaults(func=cmd_id)

    s = sub.add_parser("phone", help="تحقق من رقم جوال خليجي")
    s.add_argument("number")
    s.add_argument("-c", "--country", default="SA")
    s.set_defaults(func=cmd_phone)

    s = sub.add_parser("iban", help="تحقق من رقم الآيبان")
    s.add_argument("value")
    s.set_defaults(func=cmd_iban)

    s = sub.add_parser("hijri", help="تحويل بين الهجري والميلادي")
    s.add_argument("value", nargs="?")
    s.add_argument("--from-hijri", action="store_true", help="المدخل تاريخ هجري")
    s.set_defaults(func=cmd_hijri)

    s = sub.add_parser("money", help="تنسيق المبالغ بعملات الخليج")
    s.add_argument("amount")
    s.add_argument("-c", "--currency", default="SAR")
    s.add_argument("--ar-digits", action="store_true", help="أرقام عربية ٠١٢٣")
    s.set_defaults(func=cmd_money)

    s = sub.add_parser("vat", help="حساب ضريبة القيمة المضافة")
    s.add_argument("amount")
    s.add_argument("-c", "--country", default="SA")
    s.add_argument("--rate", help="نسبة مخصصة بالمئة")
    s.add_argument("--inclusive", action="store_true", help="المبلغ شامل الضريبة")
    s.set_defaults(func=cmd_vat)

    return p


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    return args.func(args)
