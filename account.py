import streamlit as st
import firebase_admin
from firebase_admin import firestore
from datetime import datetime

from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('dynamax-cab38-194fb85c7f98.json')
firebase_admin.initialize_app(cred)

def app():

    if 'db' not in st.session_state:
        st.session_state.db = ''

    db=firestore.client()

    st.title("Login/Signup")

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''


    def f(): 
        try:
            user = auth.get_user_by_email(email)
            print(user.uid)
            st.write('Login successful!')

            st.session_state.username = user.uid
            st.session_state.useremail = user.email

            st.session_state.signout = True
            st.session_state.signedout = True
            # Update login count and time
            user_ref = db.collection('Vehcile_Details').document(user.uid)
            user_doc = user_ref.get()

            if user_doc.exists:
                data = user_doc.to_dict()

                # Get current login count and increment
                login_count = data.get('login_count', 0) + 1

                # Append timestamp to login_times list
                login_times = data.get('login_times', [])
                login_times.append(datetime.now().isoformat())

                user_ref.update({
                    'login_count': login_count,
                    'login_times': login_times
                })

        except:
            st.warning('Login Failed!')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''
        st.session_state.useremail = ''

    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False    

    if not st.session_state['signedout']:
        choice = st.selectbox("Login/Signup", ['Login', "Signup"])

        if choice == "Login":

            email = st.text_input("Email Address")
            password = st.text_input("Password", type = 'password')

            st.button("Login", on_click=f)



        else:
            name = st.text_input("Owner's Name")
            email = st.text_input("Email Address")
            username = st.text_input("License Plate")
            password = st.text_input("Password", type = 'password')
            fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "CNG", "EV", "Hydrogen"])
            vtype = st.selectbox("Vehicle Type", ["Bike", "Autorickshaw", "Car/Jeep", "LCV", "MCV", "HCV"])

            if st.button("Create my account"):
                user = auth.create_user(email = email, password = password, uid = username)
                st.success('Account created successfully!')
                st.markdown('Please login using your email and password')
                st.balloons()

                data = {
                    "fuel": fuel,
                    "license_plate": username,
                    "name": name,
                    "type": vtype,
                    "pay": "0",
                    "unpaid_trips": "0",
                    "login_count": 1,
                    "login_times": [datetime.now().isoformat()]
                }
                db.collection('Vehcile_Details').document(username).set(data)

    if st.session_state.signout:
        st.text('License Plate: '+ st.session_state.username)
        st.text('Email ID: '+st.session_state.useremail)
        st.button("Sign out", on_click = t)