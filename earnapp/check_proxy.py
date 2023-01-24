import contextlib
import requests
import json


url = "https://client.earnapp.com/is_ip_blocked?uuid=sdk-node-2860405544244a948824dd6723a4d924&version=1.294.218&arch=x64&appid=node_earnapp.com"

def check_proxy(proxy_ip):
    proxies = {
        "http": proxy_ip,
        "https": proxy_ip
    }
    with contextlib.suppress(requests.exceptions.ConnectionError):
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return json.loads(response.text)
    return False


proxy_ip = input("Proxy (12.34.56.78:1234) -> ")
print("test en cours...")
if r := check_proxy(proxy_ip):
    print("[+] le proxy répond")
    if r["ip_blocked"]:
        print("[-] le proxy est bloqué")
    else:
        print("[+] le proxy est autorisé")
else:
    print("[-] le proxy ne répond pas")