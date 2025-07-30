import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load('model/model.pkl')

st.title("Iris Flower Predictor")
st.write("Enter flower measurements to predict the species.")

# Input fields
sepal_length = st.slider("Sepal Length", 4.0, 8.0)
sepal_width  = st.slider("Sepal Width", 2.0, 5.0)
petal_length = st.slider("Petal Length", 1.0, 7.0)
petal_width  = st.slider("Petal Width", 0.1, 3.0)

# Predict button
if st.button("Predict"):
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(input_data)
    class_map = ['Setosa', 'Versicolor', 'Virginica']
    st.success(f"The predicted species is: **{class_map[prediction[0]]}**")
