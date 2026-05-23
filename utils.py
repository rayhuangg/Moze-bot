import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo

TAIPEI_TZ = ZoneInfo("Asia/Taipei")


def get_taipei_now():
    return datetime.now(TAIPEI_TZ)

def generate_moze_urls(subcategory, amount, store=None, date=None, time=None, currency="TWD", note=None, name=None):
    """
    根據 SPEC.md 第 4 點 POC 需求產生 MOZE URL Scheme。
    按鈕 1: moze3://
    按鈕 2: moze://
    """
    # 預設值
    if not date:
        date = get_taipei_now().strftime("%Y.%m.%d")
    if not time:
        time = get_taipei_now().strftime("%H:%M")

    # 建立參數字典
    # 根據 SPEC 需求：amount, account, subcategory, project
    # 以及選填的 store, date, time, currency, note, name
    params = {
        "amount": amount,
        "account": "錢包",
        "subcategory": subcategory,
        "project": "生活開銷",
        "date": date,
        "time": time,
        "store": store
    }

    if currency:
        params["currency"] = currency

    if note:
        params["note"] = note

    if name:
        params["name"] = name

    def build_url(scheme):
        # 使用 quote 編碼中文字元
        query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        return f"{scheme}new?{query_string}"

    moze3_url = build_url("moze3://")
    moze_url = build_url("moze://")

    return moze3_url, moze_url
