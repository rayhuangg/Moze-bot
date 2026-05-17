import urllib.parse
from datetime import datetime

def generate_moze_urls(subcategory, amount, store=None, date=None, time=None, currency="TWD", note=None):
    """
    根據 SPEC.md 第 4 點 POC 需求產生 MOZE URL Scheme。
    按鈕 1: moze3://
    按鈕 2: moze://
    雙方內容相同，不進行 AA 分攤。
    """
    # 預設值
    if not date:
        date = datetime.now().strftime("%Y.%m.%d")
    if not time:
        time = datetime.now().strftime("%H:%M")

    # 建立參數字典
    # 根據 SPEC 需求：amount, account, category, subcategory, project
    # 以及選填的 store, date, time, currency, note
    params = {
        "amount": amount,
        "account": "錢包",
        "category": "飲食", # 預設類別，SPEC 沒說 subcategory 對應哪個 category，暫定飲食
        "subcategory": subcategory,
        "project": "生活開銷",
        "date": date,
        "time": time,
        "currency": currency
    }

    if store:
        params["store"] = store

    if note:
        params["note"] = note

    def build_url(scheme):
        # 使用 quote 編碼中文字元
        query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        return f"{scheme}new?{query_string}"

    moze3_url = build_url("moze3://")
    moze_url = build_url("moze://")

    return moze3_url, moze_url
