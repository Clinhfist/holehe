from holehe.core import *
from holehe.localuseragent import *


async def instagram(email, client, out):
    name = "instagram"
    domain = "instagram.com"
    method = "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.instagram.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    try:
        freq = await client.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        # Try a few ways to extract the CSRF token: JSON body, plain JS object, or escaped JS
        token = None
        try:
            import json as _json
            parsed = _json.loads(freq.text)
            token = parsed.get("config", {}).get("csrf_token")
        except Exception:
            pass

        if not token:
            # plain JS-like object
            try:
                token = freq.text.split('{"config":{"csrf_token":"')[1].split('"')[0]
            except Exception:
                pass

        if not token:
            # escaped JSON inside HTML/JS
            try:
                token = freq.text.split('{\\"config\\":{\\"csrf_token\\":\\"')[1].split('\\"')[0]
            except Exception:
                token = None

        if not token:
            raise Exception('csrf token not found')
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {
        'email': email,
        'username': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(random.randint(6, 30))),
        'first_name': '',
        'opt_into_one_tap': 'false'
    }
    headers["x-csrftoken"] = token
    try:
        resp = await client.post(
            "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/",
            data=data,
            headers=headers)
        check = resp.json()
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return

    # Normalize and inspect errors in a few common shapes
    errors = check.get("errors") or {}

    def _email_taken_from_error(email_err):
        # list-like: [{"code": "email_is_taken"}, ...]
        if isinstance(email_err, list) and email_err:
            first = email_err[0]
            if isinstance(first, dict) and first.get("code") == "email_is_taken":
                return True
        # dict-like: {"_errors": [{"code": "email_is_taken"}]}
        if isinstance(email_err, dict):
            errs = email_err.get("_errors") or email_err.get("errors") or []
            if isinstance(errs, list) and errs:
                first = errs[0]
                if isinstance(first, dict) and first.get("code") == "email_is_taken":
                    return True
        # fallback: textual check
        if "email_is_taken" in str(email_err) or "email_sharing_limit" in str(email_err):
            return True
        return False

    if errors:
        email_err = errors.get("email")
        if email_err and _email_taken_from_error(email_err):
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    else:
        # No errors field: assume not taken
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
