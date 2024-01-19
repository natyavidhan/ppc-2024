from bardapi import Bard

from bardapi import BardCookies

cookie_dict = {
    "__Secure-1PSID": "egjP4T18AjffIk2CBL3i_Rf_XWHdyyRfM9uonNn-ih7HsSGeUKhIAKNEyrHqdEulqxdJNQ.",
    "__Secure-1PSIDTS": "sidts-CjIBPVxjSgE0nPdG9ALtEvWPNTrPdTTsjGBjdli-lnkJgbjPt7e77Cnk037KFByBkA2HixAA",
    "__Secure-1PSIDCC": "ABTWhQGnXcnotJkWb9jfomtkeOfqJuf7QQLMMz3XlVPckv_uQit3g7rBQFajArAAqKQWhPRZMw",
    "__Secure-1PAPISID": "10DU3mWwvXrka-zg/A9xlK92-wiDEFzGzT",
    # Any cookie values you want to pass session object.
}

bard = BardCookies(cookie_dict=cookie_dict)

print(bard.get_answer("Hello")['content'])