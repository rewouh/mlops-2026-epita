import numpy as np
import streamlit as st
import joblib
import pathlib

MODEL_PATH = pathlib.Path(__file__).parent / 'regression.joblib'

st.set_page_config(page_title="House Price Predictor", page_icon="🏠")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

st.title("House price predictor 3000")

with st.form("prediction_form"):
    size = st.number_input("Size m2", min_value=0.0, step=1.0, format="%.1f")
    bedrooms = st.number_input("Nb bedrooms", min_value=0, step=1)
    garden = st.number_input("Has garden", min_value=0, max_value=1, step=1)

    submitted = st.form_submit_button("Predict")

if submitted:
    features = np.array([[float(size), float(bedrooms), float(garden)]], dtype=float)
    prediction = model.predict(features)
    st.write(f"Prediction: {prediction[0]:,.2f}")
