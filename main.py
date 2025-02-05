import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import warnings
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

from codebase.dashboard_graphs import MaternalHealthDashboard

maternal_model = pickle.load(open("model/finalized_maternal_model.sav", 'rb'))
fetal_model = pickle.load(open("model/fetal_health_classifier.sav", 'rb'))

# Sidebar for navigation
with st.sidebar:
    st.title("BellyCare")
    st.write("Welcome to BellyCare")
    st.write("Choose an option from the menu below to get started:")

    selected = option_menu('BellyCare', ['About us', 'Pregnancy Risk Prediction',
                                          'Fetal Health Prediction', 'Dashboard'],
                           icons=['chat-square-text', 'hospital', 'capsule-pill', 'clipboard-data'],
                           default_index=0)

# About us section
if (selected == 'About us'):
    st.title("Welcome to BellyCare")
    st.write("""
    At BellyCare, our mission is to revolutionize healthcare by offering innovative solutions through predictive analysis. 
    Our platform is specifically designed to address the intricate aspects of maternal and fetal health, providing accurate 
    predictions and proactive risk management.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("1. Pregnancy Risk Prediction")
        st.write("""
        Our Pregnancy Risk Prediction feature utilizes advanced algorithms to analyze various parameters, including age, 
        body sugar levels, blood pressure, and more. By processing this information, we provide accurate predictions of 
        potential risks during pregnancy.
        """)
        st.image("graphics/pregnancy_risk_image.jpg", caption="Pregnancy Risk Prediction", use_container_width=True)
    with col2:
        st.header("2. Fetal Health Prediction")
        st.write("""
        Fetal Health Prediction is a crucial aspect of our system. We leverage cutting-edge technology to assess the 
        health status of the fetus. Through a comprehensive analysis of factors such as ultrasound data, maternal health, 
        and genetic factors, we deliver insights into the well-being of the unborn child.
        """)
        st.image("graphics/fetal_health_image.jpg", caption="Fetal Health Prediction", use_container_width=True)

    st.header("3. Dashboard")
    st.write("""
    Our Dashboard provides a user-friendly interface for monitoring and managing health data. It offers a holistic 
    view of predictive analyses, allowing healthcare professionals and users to make informed decisions. 
    The Dashboard is designed for ease of use and accessibility.
    """)

    st.write("""
    Thank you for choosing BellyCare. We are committed to advancing healthcare through technology and predictive analytics. 
    Feel free to explore our features and take advantage of the insights we provide.
    """)

# Pregnancy Risk Prediction section
if (selected == 'Pregnancy Risk Prediction'):
    st.title('Pregnancy Risk Prediction')
    content = "Predicting the risk in pregnancy involves analyzing several parameters, including age, blood sugar levels, blood pressure, and other relevant factors."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.text_input('Age of the Person', key="age")
    with col2:
        diastolicBP = st.text_input('Diastolic BP in mmHg')
    with col3:
        BS = st.text_input('Blood glucose in mmol/L')
    
    with col1:
        bodyTemp = st.text_input('Body Temperature in Celsius')
    with col2:
        heartRate = st.text_input('Heart rate in beats per minute')
    
    # Prediction
    riskLevel = ""
    predicted_risk = [0]
    with col1:
        if st.button('Predict Pregnancy Risk'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                predicted_risk = maternal_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
            
            st.subheader("Risk Level:")
            if predicted_risk[0] == 0:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: green;">Low Risk</p></bold>', unsafe_allow_html=True)
            elif predicted_risk[0] == 1:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Medium Risk</p></bold>', unsafe_allow_html=True)
            else:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: red;">High Risk</p></bold>', unsafe_allow_html=True)

    with col2:
        if st.button("Clear"): 
            st.rerun()

# Fetal Health Prediction section
if (selected == 'Fetal Health Prediction'):
    st.title('Fetal Health Prediction')
    content = "Cardiotocograms (CTGs) are a simple and cost-accessible option to assess fetal health."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)

    # Getting user input for fetal health
    col1, col2, col3 = st.columns(3)
    
    with col1:
        BaselineValue = st.text_input('Baseline Value')
    with col2:
        Accelerations = st.text_input('Accelerations')
    with col3:
        fetal_movement = st.text_input('Fetal Movement')

    with col1:
        uterine_contractions = st.text_input('Uterine Contractions')
    with col2:
        light_decelerations = st.text_input('Light Decelerations')
    with col3:
        severe_decelerations = st.text_input('Severe Decelerations')

    with col1:
        prolongued_decelerations = st.text_input('Prolongued Decelerations')
    with col2:
        abnormal_short_term_variability = st.text_input('Abnormal Short Term Variability')
    with col3:
        mean_value_of_short_term_variability = st.text_input('Mean Value of Short Term Variability')

    with col1:
        percentage_of_time_with_abnormal_long_term_variability = st.text_input('Percentage of Time With ALTV')
    with col2:
        mean_value_of_long_term_variability = st.text_input('Mean Value Long Term Variability')
    with col3:
        histogram_width = st.text_input('Histogram Width')

    # Prediction button
    with col1:
        if st.button('Predict Fetal Health'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                predicted_risk = fetal_model.predict([[BaselineValue, Accelerations, fetal_movement, uterine_contractions,
                                                       light_decelerations, severe_decelerations, prolongued_decelerations,
                                                       abnormal_short_term_variability, mean_value_of_short_term_variability,
                                                       percentage_of_time_with_abnormal_long_term_variability,
                                                       mean_value_of_long_term_variability, histogram_width]])
            
            if predicted_risk[0] == 0:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: green;">Normal</p></bold>', unsafe_allow_html=True)
            elif predicted_risk[0] == 1:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: orange;">Suspect</p></bold>', unsafe_allow_html=True)
            else:
                st.markdown('<bold><p style="font-weight: bold; font-size: 20px; color: red;">Pathological</p></bold>', unsafe_allow_html=True)
    
    with col2:
        if st.button("Clear"): 
            st.rerun()

# Dashboard section
if (selected == "Dashboard"):
    api_key = "579b464db66ec23bdd00000139b0d95a6ee4441c5f37eeae13f3a0b2"
    api_endpoint = f"https://api.data.gov.in/resource/6d6a373a-4529-43e0-9cff-f39aa8aa5957?api-key={api_key}&format=csv"
    
    st.header("Dashboard")
    content = "Our interactive dashboard provides a comprehensive visual representation of maternal health achievements across diverse regions."
    st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div></br>", unsafe_allow_html=True)

    dashboard = MaternalHealthDashboard(api_endpoint)
    dashboard.create_bubble_chart()

    with st.expander("Show More"):
        content = dashboard.get_bubble_chart_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)

    dashboard.create_pie_chart()
    with st.expander("Show More"):
        content = dashboard.get_pie_graph_data()
        st.markdown(f"<div style='white-space: pre-wrap;'><b>{content}</b></div>", unsafe_allow_html=True)
