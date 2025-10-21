import datetime as dt, requests

def now_str():
    return dt.datetime.now().strftime("%d.%m.%Y %H:%M")

def get_fx(base="USD", targets=("TRY","EUR")):
    try:
        r = requests.get("https://api.exchangerate.host/latest", params={"base":base,"symbols":",".join(targets)}, timeout=10)
        if r.status_code == 200:
            return r.json().get("rates", {})
    except Exception: pass
    return {}

def get_gold():
    try:
        r = requests.get("https://api.metals.live/v1/spot/gold", timeout=10)
        j = r.json()
        if isinstance(j, list) and j and isinstance(j[0], list):
            return j[0][1]
    except Exception: pass
    return None
