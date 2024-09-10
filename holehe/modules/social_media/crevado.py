from holehe.core import *
from holehe.localuseragent import *


async def crevado(email, client, out):
    name = "crevado"
    domain = "crevado.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://crevado.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }
    try:
        req = await client.get("https://crevado.com")
        token_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', req.text)
        if token_match is None:
            raise ValueError('csrf token missing')
        token = token_match.group(1)

        data = {
            'utf8': '\u2713',
            'authenticity_token': token,
            'plan': 'basic',
            'account[full_name]': '',
            'account[email]': email,
            'account[password]': '',
            'account[domain]': '',
            'account[confirm_madness]': '',
            'account[terms_accepted]': '0',
            'account[terms_accepted]': '1',
        }

        response = await client.post('https://crevado.com/', headers=headers, data=data)
        response_text = response.text or ''
        if 'showFormErrors' not in response_text:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return

        msg_error_match = re.search(r'showFormErrors\(\{"([^"]+)"', response_text)
        if msg_error_match and msg_error_match.group(1) == 'account_email':
            error_match = re.search(r'showFormErrors\(\{"account_email":\{"error_message":"([^"]+)"', response_text)
            if error_match and error_match.group(1) == 'has already been taken':
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
