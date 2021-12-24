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


leadercheck = {}
st.title("Wheeler Stock Competition Leaderboard")
for user in user_dict.keys():
    try:
        ud = user_dict[user]
        results = get_acct(user, user_dict[user])
        user_dict[user]["cash"] = results[0]
        user_dict[user]["equity"] = results[1]
        total = float(user_dict[user]["cash"]) + float(user_dict[user]["equity"])
        user_dict[user]["total"] = total
        leadercheck[user] = total
        # st.write(user + ": cash = " + str(user_dict[user]["cash"])+ ", equity = " + str(user_dict[user]["equity"]))
    except:
        pass

counter = 0
while counter < len(leadercheck.keys())-1:
    leader = max(leadercheck, key = leadercheck.get)
    st.write("1st place = " + leader + ": $" + user_dict[leader]["total"])
    leadercheck[leader] = 0
    counter +=1





