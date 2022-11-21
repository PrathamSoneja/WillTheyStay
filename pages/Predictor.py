import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler
choice = ['Select', 'Yes', 'No']
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.xls')
for col in df.columns:
    if str(df[col].dtype) == 'uint8':
        df[col] = df[col].astype('int64')
    if df[col].dtype == np.float:
        df[col] = df[col].astype('float64')

# Streamlit app
st.markdown("<h1 style='text-align: center; color: red;'>WillTheyStay.ai</h1>", unsafe_allow_html=True)
st.markdown("Fill in the mentioned details to predict whether the customer will be availing your company's services in the future or not.")
st.write('')
st.write('')
st.subheader("Personal Details\n")
st.write('')
name = "the customer"
name_ = st.text_input("Name", value="customer")
st.write('')
gender = st.selectbox('Gender', ['Select', 'Male', 'Female'])
st.write('')
SeniorCitizen = st.selectbox(f'Is {name} a senior citizen?', choice)
st.write('')
partner = st.selectbox(f'Is {name} married?', choice)
st.write('')
dependents = st.selectbox(f'Does {name} have any dependents?', choice)

st.write('')
st.write('')
st.subheader("Service Details\n")
st.write('')
tenure = st.slider(f"How long {name} been using company's service? (in years)", 0, 100)
st.write('')
PhoneService = st.selectbox(f'Has {name} opted for phone service?', choice)
st.write('')
MultipleLines = st.selectbox(f'Does {name} have multiple connections?', ['Select', 'Yes', 'No', 'No phone service'])
st.write('')
InternetService = st.selectbox(f'What kind of internet service has {name} opted for?', ['Select', 'DSL', 'Fiber Optic', 'No'])
st.write('')
OnlineSecurity = st.selectbox(f'Has {name} opted for online security?', ['Select', 'Yes', 'No internet service ', 'No'])
st.write('')
OnlineBackup = st.selectbox(f'Has {name} opted for online backup?', ['Select', 'Yes', 'No internet service ', 'No'])
st.write('')
DeviceProtection = st.selectbox(f'Has {name} opted for device protection?', ['Select', 'Yes', 'No internet service ', 'No'])
st.write('')
TechSupport = st.selectbox(f'Has {name} opted for technical support?', ['Select', 'Yes', 'No internet service ', 'No'])
st.write('')
StreamingTV = st.selectbox(f'Has {name} opted for a TV subscription?', ['Select', 'Yes', 'No internet service ', 'No'])
st.write('')
StreamingMovies = st.selectbox(f'Has {name} opted for an OTT subscription?', ['Select', 'Yes', 'No internet service ', 'No'])

st.write('')
st.write('')
st.subheader("Payment Details\n")
st.write('')
Contract = st.selectbox(f"What is the time period of {name}'s billing cycle?", ['Select', 'Month-to-Month', 'One Year', 'Two Year'])
st.write('')
PaymentMethod = st.selectbox(f"What is {name}'s preffered mode of payment", ['Select', 'Bank transfer', 'Credit card', 'Electronic check', 'Mailed check'])
st.write('')
PaperlessBilling = st.selectbox(f'Does {name} receive paperless bills?', choice)
st.write('')
MonthlyCharges = int(st.slider(f'What are the average monthly charges of {name}?', 0, 10000))
st.write('')
TotalCharges = int(st.slider(f'What are the average annual charges of {name}', 0, 10000))

if st.button('Submit'):
    #input cleaning
    features = list()
    yes_no_other_feat = [MultipleLines,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies]
    yes_no_feat = [SeniorCitizen, partner, dependents, PhoneService, PaperlessBilling]

    def encoder_1(variable, features):
        if variable == 'Yes':
            features.append(1)
        else:
            features.append(0)
        return features

    def encoder_2(variable, features):
        if variable == 'Yes':
            h = [0, 0, 1]
            for i in h:
                features.append(i)
        elif variable == 'No':
            h = [1, 0, 0]
            for i in h:
                features.append(i)
        else:
            h = [0, 1, 0]
            for i in h:
                features.append(i)
        return features


    if gender == 'Male':
        features.append(0)
    else:
        features.append(1)

    for var in yes_no_feat[0:3]:
        features = encoder_1(var, features)

    scaler = MinMaxScaler(feature_range=(0, 1))
    df['tenure'] = df['tenure'].astype('float64')
    df['tenure'] = pd.DataFrame(scaler.fit_transform(df['tenure'].to_numpy().reshape(-1, 1)), dtype='float64')
    tenure_ = scaler.transform([[tenure]])[0][0]
    features.append(np.round(tenure_, 3))

    for var in yes_no_feat[3:]:
        features = encoder_1(var, features)

    scaler = MinMaxScaler(feature_range=(0, 1))
    df['MonthlyCharges'] = df['MonthlyCharges'].astype('float64')
    df['MonthlyCharges'] = pd.DataFrame(scaler.fit_transform(df['MonthlyCharges'].to_numpy().reshape(-1, 1)))
    MonthlyCharges_ = scaler.transform([[MonthlyCharges]])[0][0]
    features.append(np.round(MonthlyCharges_, 3))

    scaler = MinMaxScaler(feature_range=(0, 1))
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].apply(lambda x: float(x))
    df['TotalCharges'] = pd.DataFrame(scaler.fit_transform(df['TotalCharges'].to_numpy().reshape(-1, 1)))
    TotalCharges_ = scaler.transform([[TotalCharges]])[0][0]
    features.append(np.round(TotalCharges_, 3))

    features = encoder_2(MultipleLines, features)

    if InternetService == 'DSL':
        features+=[1,0,0]
    elif InternetService == 'Fiber Optic':
        features+=[0,1,0]
    else:
        features+=[0,0,1]

    for var in yes_no_other_feat[1:]:
        features = encoder_2(var, features)

    if Contract == 'Month-to-Month':
        features += [1, 0, 0]
    elif Contract == 'One Year':
        features += [0, 1, 0]
    else:
        features += [0, 0, 1]

    if PaymentMethod == 'Bank transfer':
        features += [1, 0, 0, 0]
    elif PaymentMethod == 'Credit card':
        features += [0, 1, 0, 0]
    elif PaymentMethod == 'Electronic check':
        features += [0, 0, 1, 0]
    else:
        features += [0, 0, 0, 1]


    loaded_model = pickle.load(open('churn_predictor.sav', 'rb'))
    result = loaded_model.predict_proba([features])
    st.write(f"The probability of customer leaving your company's services is {np.round(result[0][1]*100, 2)}% ")