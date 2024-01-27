import browser_cookie3

def get_cookies(domain):
    Cookies={}
    chromeCookies = list(browser_cookie3.chrome())
    for cookie in chromeCookies:
        if (domain in cookie.domain):
            Cookies[cookie.name]=cookie.value
    return Cookies
    
print(get_cookies(".google.com"))