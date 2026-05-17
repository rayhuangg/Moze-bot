from utils import generate_moze_urls
import urllib.parse

def test_generate_moze_urls_identical_amount():
    # 測試金額是否相同且正確
    moze3_url, moze_url = generate_moze_urls("午餐", 200, "麥當勞")
    
    assert "amount=200" in moze3_url
    assert "amount=200" in moze_url
    assert "subcategory=%E5%8D%88%E9%A4%90" in moze3_url # 午餐
    assert "name=%E9%BA%A5%E7%95%B6%E5%8B%9E" in moze3_url # 麥當勞

def test_generate_moze_urls_with_note():
    # 測試備註功能
    _, moze_url = generate_moze_urls("採購", 500, note="買衛生紙")
    assert "note=%E8%B2%B7%E8%A1%9B%E7%94%9F%E7%B4%99" in moze_url

def test_generate_moze_urls_custom_datetime():
    # 測試自訂日期時間
    moze3_url, _ = generate_moze_urls("早餐", 100, date="2024.01.01", time="08:00")
    assert "date=2024.01.01" in moze3_url
    assert "time=08%3A00" in moze3_url

def test_generate_moze_urls_no_store():
    # 測試未提供店家名稱
    moze3_url, _ = generate_moze_urls("點心", 50)
    assert "name=" not in moze3_url
