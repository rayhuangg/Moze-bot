from datetime import datetime

import utils

from utils import generate_moze_urls
import urllib.parse

def test_generate_moze_urls_identical_amount():
    # 測試金額是否相同且正確
    moze3_url, moze_url = generate_moze_urls("午餐", 200, "麥當勞")
    decoded_moze3_url = urllib.parse.unquote(moze3_url)
    decoded_moze_url = urllib.parse.unquote(moze_url)

    assert "amount=200" in decoded_moze3_url
    assert "amount=200" in decoded_moze_url
    assert "subcategory=午餐" in decoded_moze3_url
    assert "store=麥當勞" in decoded_moze3_url

def test_generate_moze_urls_with_note():
    # 測試備註功能
    _, moze_url = generate_moze_urls("採購", 500, note="買衛生紙")
    assert "note=買衛生紙" in urllib.parse.unquote(moze_url)

def test_generate_moze_urls_custom_datetime():
    # 測試自訂日期時間
    moze3_url, _ = generate_moze_urls("早餐", 100, date="2024.01.01", time="08:00")
    assert "date=2024.01.01" in moze3_url
    assert "time=08%3A00" in moze3_url

def test_generate_moze_urls_no_store():
    # 測試未提供店家名稱
    moze3_url, _ = generate_moze_urls("點心", 50)
    assert "store=" not in moze3_url


def test_generate_moze_urls_uses_taipei_timezone_defaults(monkeypatch):
    fixed_now = datetime(2026, 5, 19, 22, 20, tzinfo=utils.TAIPEI_TZ)

    monkeypatch.setattr(utils, "get_taipei_now", lambda: fixed_now)

    moze3_url, _ = generate_moze_urls("早餐", 100)

    assert "date=2026.05.19" in moze3_url
    assert "time=22%3A20" in moze3_url
