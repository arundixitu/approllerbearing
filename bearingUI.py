import subprocess
import sys

# Function to install a missing package
def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Failed to install {package}: {e}")
        sys.exit(1)

# Try importing the required package
try:
    import lightgbm as lgb
except ModuleNotFoundError:
    print("Module 'lightgbm' is not installed. Installing now...")
    install("lightgbm")
    import lightgbm as lgb  # Retry the import after installation
   
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

# Load required files
optimized_lgbm = joblib.load('optimized_lgbm.pkl')
label_encoder = joblib.load("label_encoder.pkl")
scaler = joblib.load("scaler.pkl")

def visualize_class_distribution(data):
    class_counts = data['Category'].value_counts()
    st.subheader("Class Distribution in Uploaded Dataset")
    st.bar_chart(class_counts)

def visualize_feature_importance():
    st.subheader("Feature Importance")

    # Extract feature importance from the trained LightGBM model
    feature_importance = optimized_lgbm.feature_importances_

    # Ensure the number of feature names matches the model
    feature_names = ['RMS', 'KU', 'CF', 'IF', 'PP', 'EN', 'Energy/Peak']

    if len(feature_importance) != len(feature_names):
        st.error("Mismatch between feature importance values and feature names.")
        return

    # Plot the feature importance
    plt.figure(figsize=(8, 6))
    plt.barh(feature_names, feature_importance, color='teal')
    plt.xlabel("Importance")
    plt.title("Feature Importance in LightGBM Model")
    st.pyplot(plt)


# Streamlit App Layout
st.set_page_config(page_title="Bearing Fault Detection", layout="wide")

# Header Section
col1, col2, col3 = st.columns([1, 5, 1])  # Adjust column ratios for symmetry

with col1:
    st.image("aicte_logo.png", width=100)  # Left logo

with col1:
    st.image("bearing2.png", width=250)  

with col2:
    st.markdown("""
        <h2 style='text-align: center;'>AICTE QIP PG Certificate Program on Machine Learning</h2>
        <h4 style='text-align: center;'>Centre: Indian Institute of Science (IISc), Bengaluru</h4>
        <h3 style='text-align: center;'>Project Title: Rolling Element Bearing Fault Detection and Classification using Machine Learning</h3>
    """, unsafe_allow_html=True)  # Centered text

with col3:
    st.image("iisc_logo1.jpg", width=100)  # Right logo

with col3:
    st.image("bearing1.png", width=300)  


# Sidebar Section with Modified Input and Output Descriptions
st.sidebar.markdown(
    """<h3 style='text-align: center;'>Fault Diagnosis & Classification in Rolling Element Bearings</h3>""",
    unsafe_allow_html=True
)
st.sidebar.markdown("### Flowchart of the ML Analysis")
st.sidebar.markdown("[View Flowchart](https://drive.google.com/file/d/1QZDHXltP4DmZjrKYdVFairiUQp6D2Spb/view?usp=sharing)", unsafe_allow_html=True)

# Placeholder for Setup and Input Capturing Details
st.sidebar.markdown("### Details about the Work")
st.sidebar.markdown("[About work](https://drive.google.com/file/d/1QgaP9y8C-igJQaKHRVhK-0bE_TftbEXJ/view?usp=drive_link)")  

st.sidebar.markdown("""<h4>Dataset Features (Input):</h4>""", unsafe_allow_html=True)
st.sidebar.markdown("""
- **RMS (Root Mean Square):** Measure of the magnitude of vibration signals.
- **KU (Kurtosis):** Describes the sharpness of the vibration signal peaks.
- **CF (Crest Factor):** Ratio of the peak amplitude to the RMS value.
- **IF (Impulse Factor):** Indicates the impulsiveness of the vibration signal.
- **PP (Peak-to-Peak):** The difference between the maximum and minimum signal amplitudes.
- **EN (Energy):** The total energy contained in the vibration signal.
""")
st.sidebar.markdown("### Download/View Trained Dataset")
st.sidebar.markdown("[Download as Excel](https://docs.google.com/spreadsheets/d/15d9dXWdSoltzsxZuj-TGDvTUE9Yjd0aT/edit?usp=drive_link&ouid=114859279630461352273&rtpof=true&sd=true)", unsafe_allow_html=True)
st.sidebar.markdown("[Download as CSV](https://drive.google.com/file/d/1QYPWs_7bGWXzCNvttIuUZUb8ccBM-t1w/view?usp=sharing)", unsafe_allow_html=True)

st.sidebar.markdown("### Unseen Dataset Details")
st.sidebar.markdown("The unseen dataset is used to validate the model's performance on new data, ensuring its reliability and robustness.")
st.sidebar.markdown("[Download Unseen Dataset (CSV)](https://drive.google.com/file/d/1QRbt_zOj6ZpVJgofNb2hEtUJ-ufphvud/view?usp=drive_link)", unsafe_allow_html=True)
st.sidebar.markdown("**Accuracy on Unseen Dataset:** 100%")


st.sidebar.markdown("""<h4>Output Classes (Bearing Conditions):</h4>""", unsafe_allow_html=True)
st.sidebar.markdown("""
- **HB (Healthy Bearing):** The bearing is operating under normal conditions with no faults.
- **IRD (Inner Race Defect):** Fault detected in the inner race of the bearing.
- **ORD (Outer Race Defect):** Fault detected in the outer race of the bearing.
- **RED (Rolling Element Defect):** Fault detected in the rolling elements of the bearing.
""")

st.sidebar.markdown("**Machine Learning Model Used:** Light Boost Gradient Model (BGM) ")
st.sidebar.markdown("**Accuracy Achieved:** 90%")

# Add Links to the Model Trained in Google Colab
st.sidebar.markdown("### Google Colab ML Model Link")
st.sidebar.markdown("[View Trained Model in Google Colab](https://colab.research.google.com/drive/1MqN_IIy6Jf4KBmWxBgJ6MWQE5-BKoSPh)")
# Add PDF Link for Google Colab Code
st.sidebar.markdown("[Download Colab Code (PDF)](https://drive.google.com/file/d/1QZcQVsB0qLENjcQlUk9WbqreNB6WrhmK/view?usp=sharing)")
st.sidebar.markdown("[Confusion Matrix from trained model](https://drive.google.com/file/d/1QiTpUaVFULuEpx0lQ5Buwp-hCxO3mr20/view?usp=drive_link)")


# Main Layout
st.write("This application detects faults in bearing systems using a Light Boost Gradient Model (LightBGM) trained on vibration dataset features. Upload a dataset or enter values manually to predict the bearing condition.")

# File Upload Section
st.markdown("""<h4>Upload Your Vibration Dataset (CSV format):</h4>""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop file here or browse", type=["csv"])

st.markdown("<h4 style='text-align: center;'>OR</h4>", unsafe_allow_html=True)

# Manual Input Section
st.markdown("**Enter Individual Variable Values:**", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
with col1:
    rms = st.number_input("RMS", value=0.0, step=0.1)
with col2:
    ku = st.number_input("KU", value=0.0, step=0.1)
with col3:
    cf = st.number_input("CF", value=0.0, step=0.1)
with col4:
    impulse = st.number_input("IF", value=0.0, step=0.1)
with col5:
    pp = st.number_input("PP", value=0.0, step=0.1)
with col6:
    energy = st.number_input("EN", value=0.0, step=0.1)

probability_threshold = st.slider("Set Probability Threshold (%)", min_value=0, max_value=100, value=50, step=1)

if st.button("Predict for Manual Input"):
    energy_peak = energy / pp if pp != 0 else 0.0 
    manual_input = np.array([[rms, ku, cf, impulse, pp, energy, energy_peak]])
    scaled_input = scaler.transform(manual_input)
    probabilities = optimized_lgbm.predict_proba(scaled_input)[0] * 100
    predicted_class = optimized_lgbm.predict(scaled_input)[0]
    class_name = label_encoder.inverse_transform([predicted_class])[0]
    explanations = {
        "HB": "Healthy Bearing: Normal operation.",
        "IRD": "Inner Race Defect: Fault in the inner race.",
        "ORD": "Outer Race Defect: Fault in the outer race.",
        "RED": "Rolling Element Defect: Fault in rolling elements."
    }
    if probabilities.max() >= probability_threshold:
        st.write(f"### Predicted Class: {class_name} ({probabilities.max():.2f}%)")
        st.write(f"**Explanation:** {explanations[class_name]}")
    else:
        st.write(f"### Prediction Confidence Below Threshold ({probabilities.max():.2f}%)")

# File Processing Section
if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)

        # Ensure required columns exist in the uploaded file
        required_columns = ['RMS', 'KU', 'CF', 'IF', 'PP', 'EN']
        for column in required_columns:
            if column not in data.columns:
                st.error(f"Missing required column: {column}")
                st.stop()

        # Check if Energy/Peak exists; compute it if missing
        if 'Energy/Peak' not in data.columns:
            st.warning("'Energy/Peak' not found in uploaded file. Computing it automatically.")
            data['Energy/Peak'] = data['EN'] / data['PP'].replace(0, np.nan)  # Avoid division by zero
            data['Energy/Peak'].fillna(0, inplace=True)  # Replace NaN values with 0

        # Select features for scaling and prediction
        features = data[['RMS', 'KU', 'CF', 'IF', 'PP', 'EN', 'Energy/Peak']]
        scaled_features = scaler.transform(features)  # Scale features

        # Make predictions
        predictions = optimized_lgbm.predict(scaled_features)
        probabilities = optimized_lgbm.predict_proba(scaled_features) * 100

        # Add predictions and probabilities to the dataset
        data['Prediction'] = label_encoder.inverse_transform(predictions)
        data['Probability (%)'] = probabilities.max(axis=1)

        # Display results
        st.write("### Prediction Results")
        st.dataframe(data)
        st.download_button("Download Results", data.to_csv(index=False), file_name="results.csv", mime="text/csv")

        # Visualizations
        visualize_class_distribution(data)
        visualize_feature_importance()

    except Exception as e:
        # Catch and handle errors
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a valid CSV file to begin.")

# Footer Section
st.markdown("""<hr style='border: 1px solid gray;'>""", unsafe_allow_html=True)
st.markdown(
    """<p style='text-align: center;'>Developed as a part of project work for AICTE QIP PG Certificate Program on Machine Learning at IISc, Bengaluru</p>""",
    unsafe_allow_html=True
)
st.markdown(
    """<p style='text-align: center;'>Developed by: Arun C Dixit U & Nithin M</p>""",
    unsafe_allow_html=True
)
st.markdown(
    """<p style='text-align: center;'>Contact: <a href='mailto:arundixitu@vvce.ac.in'>arundixitu@vvce.ac.in</a> | 9900479762</p>""",
    unsafe_allow_html=True
)
