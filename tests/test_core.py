from datetime import date, timedelta

import pytest

from gulfkit import hijri, money, scaffold, validators


def make_id(prefix):
    for c in range(10):
        if validators.saudi_id(prefix + str(c))[0]:
            return prefix + str(c)


def test_saudi_id_valid_and_invalid():
    good = make_id("108765432")
    assert validators.saudi_id(good)[0]
    assert validators.saudi_id(good)[1] == "هوية وطنية"
    bad = good[:-1] + str((int(good[-1]) + 1) % 10)
    assert not validators.saudi_id(bad)[0]


def test_iqama_and_bad_prefix():
    good = make_id("212345678")
    assert validators.saudi_id(good) == (True, "إقامة")
    assert not validators.saudi_id("3000000000")[0]
    assert not validators.saudi_id("123")[0]


@pytest.mark.parametrize("value", [
    "0501234567", "+966501234567", "00966501234567",
    "966501234567", "٠٥٠١٢٣٤٥٦٧", "050 123 4567",
])
def test_saudi_phone_formats(value):
    ok, info = validators.phone(value)
    assert ok
    assert info.startswith("+966501234567")


@pytest.mark.parametrize("value", ["0401234567", "05012345", "abc", "+9665012"])
def test_phone_invalid(value):
    assert not validators.phone(value)[0]


def test_other_gulf_numbers():
    assert validators.phone("+971501234567")[0]
    assert validators.phone("+96550012345")[0]
    assert validators.phone("50012345", "KW")[0]


def test_iban():
    ok, info = validators.iban("SA03 8000 0000 6080 1016 7519")
    assert ok
    assert info == "SA03 8000 0000 6080 1016 7519"
    assert not validators.iban("SA0380000000608010167518")[0]
    assert not validators.iban("SA03800000006080101675")[0]


def test_hijri_roundtrip():
    d = date(2000, 1, 1)
    while d < date(2040, 1, 1):
        assert hijri.to_gregorian(*hijri.to_hijri(d)) == d
        d += timedelta(days=13)


def test_hijri_known_date():
    g = hijri.to_gregorian(1445, 9, 1)
    assert abs((g - date(2024, 3, 11)).days) <= 1


def test_money_format():
    assert money.fmt("1234.5") == "1,234.50 ر.س"
    assert money.fmt("1234.5", "KWD") == "1,234.500 د.ك"
    assert money.fmt("12", arabic_digits=True) == "١٢٫٠٠ ر.س"
    with pytest.raises(ValueError):
        money.fmt("abc")


def test_vat():
    net, tax, total = money.vat("100", "SA")
    assert (str(net), str(tax), str(total)) == ("100", "15.00", "115.00")
    net, tax, total = money.vat("115", "SA", inclusive=True)
    assert round(net, 2) == 100
    with pytest.raises(ValueError):
        money.vat("100", "KW")


def test_scaffold(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    files = scaffold.create("demo", "flask")
    assert any(f.endswith("app.py") for f in files)
    assert 'title="demo"' in (tmp_path / "demo" / "app.py").read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        scaffold.create("demo", "flask")
    with pytest.raises(ValueError):
        scaffold.create("اسم عربي")
