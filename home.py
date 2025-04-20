import streamlit as st
from firebase_admin import firestore

def app():
    db = firestore.client()

    try:
        st.title("Welcome to Dynamax :vertical_traffic_light:")

        result = db.collection('Vehcile_Details').document(st.session_state['username']).get()
        r = result.to_dict()

        fuel_type = r.get('fuel')
        vehicle_type = r.get('type')
        login_count = r.get('login_count', 0)

        # --- COMPLETE PRICE MATRIX TEMPLATE ---
        price_table = {
            'Petrol': {
                'Bike': 25,
                'Autorickshaw': 60,
                'Car/Jeep': 80,
                'LCV': 170,
                'MCV': 230,
                'HCV': 290
            },
            'Diesel': {
                'Bike': 27,
                'Autorickshaw': 65,
                'Car/Jeep': 90,
                'LCV': 180,
                'MCV': 240,
                'HCV': 300
            },
            'EV': {
                'Bike': 21,
                'Autorickshaw': 40,
                'Car/Jeep': 70,
                'LCV': 150,
                'MCV': 210,
                'HCV': 250
            },
            'Hybrid': {
                'Bike': 23,
                'Autorickshaw': 55,
                'Car/Jeep': 75,
                'LCV': 160,
                'MCV': 220,
                'HCV': 275
            },
            'Hydrogen': {
                'Bike': 20,
                'Autorickshaw': 50,
                'Car/Jeep': 65,
                'LCV': 150,
                'MCV': 200,
                'HCV': 260
            },
            'CNG': {
                'Bike': 23,
                'Autorickshaw': 50,
                'Car/Jeep': 65,
                'LCV': 170,
                'MCV': 230,
                'HCV': 275
            }
        }

        # Calculate payment
        price_per_trip = price_table.get(fuel_type, {}).get(vehicle_type, 0)
        total_pay = price_per_trip * login_count

        # --- DISPLAY ---
        st.write("Vehicle Owner:  " + r['name'])
        st.write("Vehicle Type: " + vehicle_type)
        st.write("Fuel Type: " + fuel_type)
        st.write("No. of trips: ", login_count)
        st.write("Payable Amount: ₹" + str(total_pay))

        # --- LOGIN TIMES ---
        login_times = r.get('login_times', [])
        if login_times:
            st.subheader("Recorded passes:")
            for i, time in enumerate(reversed(login_times[-5:]), 1):  # Show last 5 logins
                st.write(f"{i}. {time}")
        else:
            st.write("No login timestamps available.")

    except Exception as e:
        if st.session_state.username == '':
            st.text('Please Login first')
        else:
            st.error(f"Error: {str(e)}")
