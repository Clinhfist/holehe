from holehe.core import *
from holehe.localuseragent import *


async def evernote(email, client, out):
    name = "evernote"
    domain = "evernote.com"
    method = "login"
    frequent_rate_limit = False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.evernote.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.evernote.com/Login.action',
        'TE': 'Trailers',
    }
    try:
        page = await client.get("https://www.evernote.com/Login.action", headers=headers)
        hpts = re.search(r'document.getElementById\("hpts"\)\.value = "([^"]+)"', page.text)
        hptsh = re.search(r'document.getElementById\("hptsh"\)\.value = "([^"]+)"', page.text)
        source_page = re.search(r'<input type="hidden" name="_sourcePage" value="([^"]+)"', page.text)
        fp = re.search(r'<input type="hidden" name="__fp" value="([^"]+)"', page.text)
        if None in (hpts, hptsh, source_page, fp):
            raise ValueError('evernote login fields missing')

        data2 = {
            'username': email,
            'evaluateUsername': '',
            'hpts': hpts.group(1),
            'hptsh': hptsh.group(1),
            'analyticsLoginOrigin': 'login_action',
            'clipperFlow': 'false',
            'showSwitchService': 'true',
            'usernameImmutable': 'false',
            '_sourcePage': source_page.group(1),
            '__fp': fp.group(1),
        }
        response = await client.post('https://www.evernote.com/Login.action', data=data2, headers=headers)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    if "usePasswordAuth" in response.text:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "displayMessage" in response.text:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
