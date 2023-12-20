import streamlit as st
import pickle
import numpy as np




def load_model():
    with open('salary_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data



data = load_model()

regressor_loaded = data["model"]
le_coun = data["le_country"]
le_edu = data["le_education"]
le_remote = data["le_remote"]
mm = data["scaler"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        "United States of America",                               
        "Germany",                                                  
        "United Kingdom of Great Britain and Northern Ireland",     
        "Canada",                                                   
        "India",                                                    
        "France",                                                  
        "Netherlands",                                              
        "Australia",                                                 
        "Brazil",                                                    
        "Spain",
        "Sweden",                                                    
        "Italy",                                                     
        "Poland",                                                    
        "Switzerland",                                              
        "Denmark",                                                  
        "Norway",                                                   
        "Israel",
    )

    education = (
        "Bachelor's degree",
        "Master's degree",
        "Professional degree",
        "Less than a Bachelors",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

   # Ensure the LabelEncoder is fitted with all possible categories
   # le_edu.classes_ = np.unique(le_edu.classes_ + education)

    expericence = st.slider("Years of Experience", 0, 50, 3)
    
    remote_work = st.selectbox("Remote Work", ["In-person", "Remote"])

    age = st.slider("Age", 18, 65, 25)

    ok = st.button("Calculate Salary")
    if ok:
        Y = np.array([[country, age, remote_work, education, expericence]])
        Y[:,0] = le_coun.transform(Y[:,0])
        Y[:,2] = le_remote.transform(Y[:,2])
        # Ensure the LabelEncoder is fitted with all possible categories
        le_edu.classes_ = np.unique(np.concatenate([le_edu.classes_, ['Less than a Bachelors']]))

        # Handle unseen labels for education
        Y[:, 3] = le_edu.transform(np.where(np.isin(Y[:, 3], le_edu.classes_), Y[:, 3], 'Less than a Bachelors'))
        Y = Y.astype(float)
        Y = mm.transform(Y)
        """Z[:,0] = le_coun.transform(Z[:,0])
        Z[:,2] = le_remote.transform(Z[:,2])
         # Handle unseen labels for education
        Z[:, 3] = np.where(np.isin(Z[:, 3], le_edu.classes_), le_edu.transform(Z[:, 3]), le_edu.transform(['Less than a Bachelors']))

        Z = Z.astype(float)

        # Print the final transformed input values
        print("Final Transformed Input:", Z)"""

        salary = regressor_loaded.predict(Y)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
       
    