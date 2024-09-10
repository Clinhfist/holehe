from holehe.core import *
from holehe.localuseragent import *


async def rocketreach(email, client, out):
    name = "rocketreach"
    domain = "rocketreach.co"
    method = "register"
    frequent_rate_limit = False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://rocketreach.co/signup',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    try:
        response = await client.get("https://rocketreach.co/signup")
        token_match = re.search(r'name="csrfmiddlewaretoken" value="(.*)"', response.text)
        if token_match is None:
            raise ValueError('csrf token not found')
        headers["x-csrftoken"] = token_match.group(1)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    try:
        r = await client.get('https://rocketreach.co/v1/validateEmail?email_address=' + email, headers=headers)
        payload = r.json()
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    result = payload.get('found')
    if result is True:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif result is False:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
