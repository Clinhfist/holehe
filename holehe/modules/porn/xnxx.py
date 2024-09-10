from holehe.core import *
from holehe.localuseragent import *

async def xnxx(email, client, out):
    name = "xnxx"
    domain = "xnxx.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr-fr',
        'Host': 'www.xnxx.com',
        'User-Agent': random.choice(ua["browsers"]["safari"]),
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'}

    try:
        XNXX = await client.get('https://www.xnxx.com', headers=headers)
        if XNXX.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return

        headers['Referer'] = 'https://www.xnxx.com/video-holehe/palenath_fucks_xnxx_with_holehe'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        email_query = email.replace('@', '%40')
        APIRQST = await client.get(f'https://www.xnxx.com/account/checkemail?email={email_query}', headers=headers, cookies=XNXX.cookies)
        if APIRQST.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return

        API = json.loads(APIRQST.text)
        result = API.get('result')
        code = API.get('code')
        message = API.get('message', '')

        if result is False and code == 1 and message == 'Cet email est d&eacute;j&agrave; utilis&eacute; ou son propri&eacute;taire l&#039;a exclu de notre site.':
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif result is False and code == 1 and message == 'Adresse email invalide.':
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif result is True and code == 0:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif result is False and code == 2 and message == 'Trop rapide. Merci de r&eacute;essayer dans quelques secondes.':
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
    out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": True, "exists": False, ...})