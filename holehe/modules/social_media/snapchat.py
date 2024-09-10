from holehe.core import *
from holehe.localuseragent import *


async def snapchat(email, client, out):
    name = "snapchat"
    domain = "snapchat.com"
    method = "login"
    frequent_rate_limit = False

    try:
        req = await client.get("https://accounts.snapchat.com")
        xsrf_match = re.search(r'data-xsrf="([^"]+)"', req.text)
        web_client_match = re.search(r'data-web-client-id="([^"]+)"', req.text)
        if xsrf_match is None or web_client_match is None:
            raise ValueError('snapchat page changed')
        xsrf = xsrf_match.group(1)
        webClientId = web_client_match.group(1)

        url = "https://accounts.snapchat.com/accounts/merlin/login"
        headers = {
            "Host": "accounts.snapchat.com",
            "User-Agent": random.choice(ua["browsers"]["firefox"]),
            "Accept": "*/*",
            "X-XSRF-TOKEN": xsrf,
            "Accept-Encoding": "gzip, late",
            "Content-Type": "application/json",
            "Connection": "close",
            "Cookie": "xsrf_token=" + xsrf + "; web_client_id=" + webClientId
        }
        payload = {"email": email, "app": "BITMOJI_APP"}
        response = await client.post(url, json=payload, headers=headers)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    try:
        if response.status_code == 204:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return
        data = response.json()
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": bool(data.get("hasSnapchat", False)), "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
