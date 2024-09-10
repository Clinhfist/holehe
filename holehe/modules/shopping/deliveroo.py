from holehe.core import *
from holehe.localuseragent import *


async def deliveroo(email, client, out):
    name = "deliveroo"
    domain = "deliveroo.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, application/vnd.api+json',
        'Accept-Language': 'en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Roo-Client': 'orderweb-client',
        'X-Roo-Country': 'fr',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://deliveroo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = {"email_address": email}

    try:
        req = await client.post('https://consumer-ow-api.deliveroo.com/orderapp/v1/check-email', headers=headers, json=data)
        payload = req.json() if req is not None else {}
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    if req.status_code == 200:
        if payload.get("registered") is True:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif payload.get("registered") is False:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
