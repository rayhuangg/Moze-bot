import urllib.parse
from utils import generate_moze_urls

def test_generate_moze_urls_even_amount():
    # 測試偶數金額：200 -> 100/100
    boy_url, girl_url = generate_moze_urls("Ray", "午餐", 200, "麥當勞")
    
    assert "amount=100" in boy_url
    assert "amount=100" in girl_url
    assert "moze3://" in boy_url
    assert "moze://" in girl_url
    assert "subcategory=%E5%8D%88%E9%A4%90" in boy_url # "午餐" 的 URL 編碼
    assert "name=%E9%BA%A5%E7%95%B6%E5%8B%9E" in boy_url # "麥當勞" 的 URL 編碼

def test_generate_moze_urls_odd_amount():
    # 測試奇數金額：201 -> 男友 101 / 女友 100
    boy_url, girl_url = generate_moze_urls("Ray", "午餐", 201, "麥當勞")
    
    assert "amount=101" in boy_url
    assert "amount=100" in girl_url

def test_generate_moze_urls_no_item():
    # 測試未提供店家名稱
    boy_url, girl_url = generate_moze_urls("Ray", "點心", 50)
    
    assert "name=" not in boy_url
    assert "subcategory=%E9%BB%9E%E5%BF%83" in boy_url
