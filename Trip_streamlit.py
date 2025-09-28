import streamlit as st
import joblib
import numpy as np

# Load trained model
model = joblib.load("C:/Users/Ajay/Desktop/Python/Trip_Fare/grid_rf.pkl")

import streamlit as st

# Define your desired styles in an HTML string
custom_title = """
<style>
.custom-title {
    font-family: 'Georgia', serif; 
    font-size: 2em; 
    
    font-weight: bold;
    text-shadow: 2px 2px 4px #000000; 
}
</style>
<span class="custom-title">Trip Fare Prediction</span>
"""

# Use st.markdown() to render the styled title
st.markdown(custom_title, unsafe_allow_html=True)


# Streamlit UI
#st.title("Trip Fare Prediction")

#st.image("C:/Users/Ajay/Desktop/Python/Trip_Fare/taxi.png", width=100)

st.markdown("📍 Estimate Your Trip Fare")

st.markdown("Get an instant fare prediction based on your trip details")

st.markdown("Fill in trip parameters on the sidebar to see your estimated cost")


st.sidebar.markdown("Enter Trip Details")
passenger_count = st.sidebar.number_input("Number of Passengers", min_value=1, max_value=6, value=1)
trip_distance = st.sidebar.number_input("Trip Distance (km)", min_value=1, value=15)
trip_duration = st.sidebar.number_input("Trip Duration (minutes)", min_value=1, value=20)
pickup_hour = st.sidebar.number_input("Pickup Hour (0-23)", min_value=0, max_value=23, value=12)
is_night = st.sidebar.selectbox("Is it Night?(10Pm to 5am) ", [0, 1])
rate_code = st.sidebar.number_input("Rate Code", min_value=1, max_value=6, value=1)


payment_map = {
    "Cash": 1,
    "Credit Card": 2,
    "Digital Wallet": 3,
    "Other": 4,
}
# Let user select the payment type as a string
payment_str = st.sidebar.selectbox("Payment Type", options=list(payment_map.keys()))
# Convert to the code (digit)
payment_type = payment_map[payment_str]


#payment_type = st.sidebar.number_input("Payment Type", min_value=1, max_value=4, value=1)

am_pm = st.sidebar.selectbox("Select Time of Day", ["AM", "PM"])

# Encode it to 0 / 1
if am_pm == "AM":
    am_pm = 0
else:
    am_pm = 1

st.sidebar.markdown("<hr style='border: 0; height: 1px; ;background-color: #333333; margin: 20px 0 10px 0;'>", unsafe_allow_html=True)

# The developer credit line
st.sidebar.markdown("<i>Developed By [thejj_theju]</i>", unsafe_allow_html=True)


# Predict button
if st.button("Predict Fare"):
   
    dist_log = np.log1p(trip_distance)
    dur_log = np.log1p(trip_duration)

     # Create input array in the same order as model expects
    input_data = np.array([[passenger_count, rate_code, 
                            payment_type, 
                            dist_log,
                            dur_log, pickup_hour, 
                            am_pm, is_night
                             ]])



    # Get the log-domain prediction
    y_log_pred = model.predict(input_data)[0]
    
    # Convert the prediction back to original scale using expm1
    predicted_amount = np.expm1(y_log_pred)
    
    st.success(f"Estimated Trip Fare: ${predicted_amount:.2f}")
   

    
    # Predict
    #predicted_fare = model.predict(input_data)
    #st.success(f"Estimated Trip Fare: ₹{predicted_fare[0]:.2f}")





