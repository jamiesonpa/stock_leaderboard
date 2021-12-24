import robin_stocks.robinhood as rh
import robin_stocks.gemini as gem
import robin_stocks.tda as tda
import pyotp
import streamlit as st


def get_acct(name, userdata):
    totp = pyotp.TOTP(userdata["code"]).now()
    rh.login(username=userdata["email"], password=userdata["password"], mfa_code=totp, store_session=False)
    basics = rh.account.build_user_profile()
    stocks = rh.load_account_profile()
    cash = basics["cash"]
    equity = basics["equity"]
    # for key,value in stocks.items():
    #     print(key,value)
    retval = [cash, equity]
    print(str(retval))
    rh.logout()
    return retval


user_dict = {}

with open("auth_codes.txt") as readfile:
    ac = readfile.read().split("\n")

user_data = {}
for line in ac:
    user_data = {}
    splits = line.split(",")
    user_data["email"] = splits[1]
    user_data["password"] = splits[2]
    user_data["code"] = splits[3]
    user_dict[splits[0]] = user_data

st.title("Wheeler Stock Competition Leaderboard")
for user in user_dict.keys():
    try:
        ud = user_dict[user]
        results = get_acct(user, ud)
        ud["cash"] = results[0]
        ud["equity"] = results[1]
        user_dict[user] = ud
        st.write("user: " + user_dict[user])
    except:
        pass




