from holehe.core import *
from holehe.localuseragent import *


async def buymeacoffee(email, client, out):
    name = "buymeacoffee"
    domain = "buymeacoffee.com"
    method = "register"
    frequent_rate_limit = True

    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.buymeacoffee.com',
        'DNT': '1',
        'TE': 'Trailers',
    }

    try:
        r = await client.get("https://www.buymeacoffee.com/", headers=headers)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    page_text = getattr(r, "text", "") or ""
    if r.status_code != 200:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    csrf_token = None
    try:
        soup = BeautifulSoup(page_text, features="html.parser")
        token_node = soup.find(attrs={'name': 'bmc_csrf_token'})
        if token_node is not None:
            csrf_token = token_node.get("value")
    except Exception:
        csrf_token = None

    if not csrf_token:
        match = re.search(r'name=["\']?bmc_csrf_token["\']?[^>]*value=["\']([^"\']+)["\']', page_text, re.I)
        if match:
            csrf_token = match.group(1)

    if not csrf_token:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    cookies = {'bmccsrftoken': csrf_token}
    data = {'email': email, 'password': get_random_string(20), 'bmc_csrf_token': csrf_token}

    try:
        r = await client.post(
            'https://www.buymeacoffee.com/auth/validate_email_and_password',
            headers=headers,
            cookies=cookies,
            data=data)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    if r.status_code == 200:
        try:
            data = r.json()
        except Exception:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return

        if data.get("status") == "SUCCESS":
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif data.get("status") == "FAIL" and "email" in str(data):
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
