from holehe.core import *
from holehe.localuseragent import *

async def soundcloud(email, client, out):
    name = "soundcloud"
    domain = "soundcloud.com"
    method = "register"
    frequent_rate_limit = False

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': random.choice(ua["browsers"]["iOS"])
    }

    try:
        getAuth = await client.get('https://soundcloud.com/octobersveryown', headers=headers)
        soup = BeautifulSoup(getAuth.text, 'html.parser')
        clientId = None
        for script in soup.find_all('script'):
            try:
                if not script.contents:
                    continue
                payload = json.loads(str(script.contents[0]))
                clientId = payload.get('runtimeConfig', {}).get('clientId')
                if clientId:
                    break
            except Exception:
                continue
        if clientId is None:
            raise ValueError('clientId not found')

        linkMail = email.replace('@', '%40')
        API = await client.get(f'https://api-auth.soundcloud.com/web-auth/identifier?q={linkMail}&client_id={clientId}', headers=headers)
        Json = json.loads(API.text)
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    status = Json.get('status')
    if status in ('in_use', 'available'):
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": status == 'in_use', "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
