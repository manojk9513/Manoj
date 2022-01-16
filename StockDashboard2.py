import re
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import hashlib
from PIL import Image

# mongodb connection
client = MongoClient('localhost', 27017)
db = client["stocks"]
col = db["stock_metadata"]
db2 = client["Validate"]
col2 = db2["Login"]
reg = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\W{2,3}$'
img = 'C:/Users/hp/PycharmProjects/stock_dashboard/NSE.jpg'
l = list(db.list_collection_names())
for i in l:
    if i == 'stock_metadata':
        l.remove(i)


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password,) == hashed_text:
        return hashed_text
    return False


def add_userdata(name, email, username, password, password2):
    d = list(col2.find({"username": username},{"username":1,"_id":0}))
    print(d)
    if d:
        st.error("Username already exist, enter different username")
    else:
        col2.insert_one({"name": name, "email": email, "username": username, "password": password, "confirm_password": password2})
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")


def login_user(username, password):
    data = list(col2.find({"username": username, "password": password}))
    return data


def view_users(username, password):
    data = col2.find({"username": username, "password": password})
    return data


def main():
    st.header("Stock Market Dashboard")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.radio("STOCK DASHBOARD", menu)
    st.sidebar.form("abc")
    if choice == "Home":
        st.title("Home")
        st.info('What is the Stock Market?')
        st.write('The stock market refers to the collection of markets and exchanges'
                 ' where regular activities of buying, selling, and issuance of shares of publicly-held companies take place. '
                 'Such financial activities are conducted through institutionalized formal exchanges or over-the-counter (OTC) marketplaces '
                 'which operate under a defined set of regulations. '
                 'There can be multiple stock trading venues in a country or a region which allow transactions in stocks and other forms of securities.')
        img1 = Image.open("C:/Users/hp/PycharmProjects/stock_dashboard/img4.jpg")
        #st.image(img1, width=500)
        st.info('National Stock Exchange of India Limited (NSE)')
        st.image(img,caption='NSE')
        st.write('National Stock Exchange of India Limited (NSE) is the leading government owned stock exchange of India,'
                 ' located in Mumbai, Maharashtra. It is under the ownership of Some leading financial institutions, '
                 'Banks and Insurance companies. NSE was established in 1992 as the first dematerialized electronic exchange in the country.'
                 ' NSE was the first exchange in the country to provide a modern, fully automated screen-based electronic '
                 'trading system that offered easy trading facilities to investors spread across the length and breadth of the country.'
                'Vikram Limaye is Managing Director & Chief Executive Officer of NSE.')
        st.write('National Stock Exchange has a total market capitalization of more than US$3 trillion, making it the world'
            '9th-largest stock exchange as of May 2021.NSE flagship index, the NIFTY 50, a 50 stock index is used '
            'extensively by investors in India and around the world as a barometer of the Indian capital market. '
            'The NIFTY 50 index was launched in 1996 by NSE.However,' 
            ' Vaidyanathan (2016) estimates that only about 4% of the Indian economy / GDP is actually derived from the stock exchanges in India.')
        st.info("Trading Schedule")
        st.write("Trading on the equities segment takes place on all days of the week (except Saturdays and Sundays and holidays declared by the Exchange in advance). "
                 "The market timings of the equities segment are:")
        st.markdown('(1) Pre-open session:')
        st.write('-Open Time: 09:00 hrs(9 am)')
        st.write('-Close Time: 17:00 hrs(5 pm)')

        st.info("List of Comapnies in NIFTY-50")
        st.table(l)

    elif choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                task = st.radio("Task", ["About Companies", "Analytics", "Profiles"])

                if task == "Analytics":
                    st.info("Analytics")
                    st.sidebar.header('Nifty50')
                    task2 = st.selectbox("Analytical Task", ["Charts", "Data Frames"])

                    def get_input():
                        start_date = st.sidebar.text_input("Start Date", "2007-11-27")
                        end_date = st.sidebar.text_input("End Date", "2021-04-30")
                        stock_symbol = st.sidebar.selectbox("Select company", l)
                        st.header(stock_symbol)

                        return start_date, end_date, stock_symbol

                    def getdata(symbol, start, end):
                        for i in db.list_collection_names():
                            if symbol == i:
                                a = db[i]
                                c = a.find()
                                df = pd.DataFrame(list(c))
                                for j in df:
                                    if j == '_id':
                                        del df['_id']

                                df.to_csv(symbol+'.csv', index=False)
                                #x = pd.DataFrame(df)
                                x = pd.read_csv("C:/Users/hp/PycharmProjects/stock_dashboard/"+symbol+".csv")
                                #print(x)

                        start = pd.to_datetime(start)
                        end = pd.to_datetime(end)

                        start_row = 0
                        end_row = 0

                        for i in range(0, len(x)):
                            if start <= pd.to_datetime(x['Date'][i]):
                                start_row = i
                                break

                        for j in range(0, len(x)):
                            if end >= pd.to_datetime(x['Date'][len(x) - 1 - j]):
                                end_row = len(x) - 1 - j
                                print(end_row)
                                break

                        x = x.set_index(pd.DatetimeIndex(x['Date'].values))
                        return x.iloc[start_row:end_row + 1, :]

                    start, end, symbol = get_input()
                    x = getdata(symbol, start, end)

                    if task2 == "Charts":
                        st.write("Open Chart")
                        st.line_chart(x['Open'])
                        st.write("Close Chart")
                        st.line_chart(x['Close'])
                        st.write("Open & Close Chart")
                        chardata1 = pd.DataFrame(x, columns=['Open', 'Close'])
                        st.line_chart(chardata1)

                        st.write("High Chart")
                        st.line_chart(x['High'])
                        st.write("Low Chart")
                        st.line_chart(x['Low'])
                        chardata2 = pd.DataFrame(x, columns=['High','Low'])
                        st.write("High & Low Chart")
                        st.line_chart(chardata2)
                    elif task2 == "Data Frames":
                        st.write("Data")
                        st.dataframe(x)
                        st.write("Average")
                        st.write(x.describe())

                elif task == "Profiles":
                    st.info("User Profiles")
                    f = pd.DataFrame(list(col2.find({"username": username})))
                    for j in f:
                        if j == '_id':
                            del f['_id']
                            del f['password']
                            del f['confirm_password']

                    st.table(f)
                elif task == "About Companies":
                    st.info("Company Details")
                    df = pd.DataFrame(list(col.find()))
                    for j in df:
                        if j == '_id':
                            del df['_id']
                    st.table(df)
            else:
                st.sidebar.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        name = st.text_input("Name")
        email = st.text_input("Email")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_password2 = st.text_input("Password2", type='password')
        if st.button("Signup"):
            if new_password != new_password2:
                st.sidebar.error("Passwords do not match")
            else:
                add_userdata(name, email, new_user, make_hashes(new_password), make_hashes(new_password2))


if __name__ == '__main__':
    main()