from holehe.core import *
from holehe.localuseragent import *


async def snapchat(email, client, out):
    name = "snapchat"
    domain = "snapchat.com"
    method = "login"
    frequent_rate_limit = False

    try:
        req = await client.get("https://accounts.snapchat.com")
        text = req.text or ""

        # Try multiple patterns for xsrf and client id
        xsrf = None
        webClientId = None
        for pattern in [r'data-xsrf="([^"]+)"', r'data-xsrf-token="([^"]+)"', r'XSRF-TOKEN=([^;\s]+)']:
            m = re.search(pattern, text)
            if m:
                xsrf = m.group(1)
                break

        for pattern in [r'data-web-client-id="([^"]+)"', r'web_client_id=([^;\s]+)']:
            m = re.search(pattern, text)
            if m:
                webClientId = m.group(1)
                break

        if not xsrf:
            # also try cookies set in response
            xsrf = req.headers.get("set-cookie")
            if xsrf:
                m = re.search(r'xsrf_token=([^;\s]+)', xsrf)
                if m:
                    xsrf = m.group(1)
                else:
                    xsrf = None

        if not xsrf or not webClientId:
            raise ValueError('snapchat page changed')

        url = "https://accounts.snapchat.com/accounts/merlin/login"
        headers = {
            "Host": "accounts.snapchat.com",
            "User-Agent": random.choice(ua["browsers"]["firefox"]),
            "Accept": "*/*",
            "X-XSRF-TOKEN": xsrf,
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "Connection": "close",
            "Cookie": f"xsrf_token={xsrf}; web_client_id={webClientId}"
        }
        payload = {"email": email, "app": "BITMOJI_APP"}
        response = await client.post(url, json=payload, headers=headers)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
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
                    "rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
