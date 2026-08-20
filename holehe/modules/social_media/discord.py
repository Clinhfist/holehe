from holehe.core import *
from holehe.localuseragent import *


async def discord(email, client, out):
    name = "discord"
    domain = "discord.com"
    method = "register"
    frequent_rate_limit=False

    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    payload = {
        "fingerprint": "",
        "email": str(email),
        "username": get_random_string(20),
        "password": get_random_string(20),
        "invite": None,
        "consent": True,
        "date_of_birth": "2000-01-01",
        "gift_code_sku_id": None,
        "captcha_key": None,
    }

    try:
        response = await client.post(
            'https://discord.com/api/v8/auth/register',
            headers=headers,
            json=payload)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return

    try:
        responseData = response.json()
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return

    # Check shapes: errors -> email -> _errors or top-level code/messages
    try:
        # email already registered detection
        email_err = None
        if isinstance(responseData, dict):
            email_err = responseData.get("errors", {}).get("email") if responseData.get("errors") else None
            if email_err:
                # could be dict with _errors
                errs = email_err.get("_errors") if isinstance(email_err, dict) else email_err
                if isinstance(errs, list) and errs:
                    first = errs[0]
                    if isinstance(first, dict) and first.get("code") in ("EMAIL_ALREADY_REGISTERED", "email_already_registered"):
                        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                                    "rateLimit": False,
                                    "exists": True,
                                    "emailrecovery": None,
                                    "phoneNumber": None,
                                    "others": None})
                        return

        # captcha detection
        if isinstance(responseData, dict) and responseData.get("captcha_key"):
            ck = responseData.get("captcha_key")
            if isinstance(ck, (list, tuple)) and ck and ck[0] == "captcha-required":
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
                return

        # if none matched, fall back to rateLimit True (service changed)
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
