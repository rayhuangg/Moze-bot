import urllib.parse

def generate_moze_urls(payer, subcategory, amount, item=None):
    """
    根據 SPEC.md 第 4 點 POC 需求產生 MOZE URL Scheme。
    男友 (Ray): moze3://
    女友 (Moyichen): moze://
    """
    # AA 分攤邏輯：餘數由男友負擔
    girl_amount = amount // 2
    boy_amount = amount - girl_amount

    # 預設值與編碼
    # POC 範例中包含 account, category, subcategory, project, name
    # 我們假設 category 與 project 為固定值，item 映射到 name
    base_params = {
        "account": "錢包",
        "category": "飲食",
        "subcategory": subcategory,
        "project": "生活開銷"
    }
    
    if item:
        base_params["name"] = item

    def build_url(scheme, split_amount):
        params = base_params.copy()
        params["amount"] = split_amount
        # 使用 quote 編碼中文字元
        query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
        return f"{scheme}new?{query_string}"

    boy_url = build_url("moze3://", boy_amount)
    girl_url = build_url("moze://", girl_amount)

    return boy_url, girl_url
