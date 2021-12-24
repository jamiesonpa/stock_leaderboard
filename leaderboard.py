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
        results = get_acct(user, user_dict[user])
        user_dict[user]["cash"] = results[0]
        user_dict[user]["equity"] = results[1]
        total = float(user_dict[user]["cash"]) + float(user_dict[user]["equity"])
        user_dict[user]["total"] = total
        leadercheck[user] = total
    except:
        pass

counter = 0
while counter < len(leadercheck.keys())-1:
    leader = max(leadercheck, key = leadercheck.get)
    if counter == 0:
        st.write("1st place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 1:
        st.write("2nd place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 2:
        st.write("3rd place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 3:
        st.write("4th place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 4:
        st.write("5th place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 5:
        st.write("6th place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 6:
        st.write("7th place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 7:
        st.write("8th place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 8:
        st.write("9th place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    elif counter == 9:
        st.write("10th place = " + leader + ": $" + str(user_dict[leader]["equity"]))
    else:
        st.write("unranked = " + leader + ": $" + str(user_dict[leader]["equity"]))
    leadercheck.pop(leader)
    counter +=1





