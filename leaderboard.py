import robin_stocks.robinhood as rh
import robin_stocks.gemini as gem
import robin_stocks.tda as tda
import pyotp
import streamlit as st
from streamlit import secrets


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

for player in st.secrets.keys():
    user_data = {}
    playerdata = st.secrets[player].split(",")
    user_data["email"] = playerdata[0]
    user_data["password"] = playerdata[1]
    user_data["code"] = playerdata[2]
    user_dict[player] = user_data


st.title("Wheeler Stock Competition Leaderboard")
for user in user_dict.keys():
    try:
        ud = user_dict[user]
        results = get_acct(user, ud)
        ud["cash"] = results[0]
        ud["equity"] = results[1]
        user_dict[user] = ud
        st.write(user + ": cash = " + str(user_dict[user]["cash"])+ ", equity = " + str(user_dict[user]["equity"]))
    except:
        pass




