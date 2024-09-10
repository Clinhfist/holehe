from holehe.core import *
from holehe.localuseragent import *


async def pinterest(email, client, out):
    name = "pinterest"
    domain = "pinterest.com"
    method = "register"
    frequent_rate_limit = False

    try:
        req = await client.get(
            "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
            params={
                "source_url": "/",
                "data": '{"options": {"email": "' + email + '"}, "context": {}}'})
        payload = req.json()
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        return

    response_data = payload.get("resource_response", {}).get("data")
    if isinstance(response_data, dict) and 'source_field' in str(response_data):
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response_data:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
