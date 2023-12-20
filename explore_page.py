import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

"""def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map"""
def shorten_categories(categories,cutoff):
    categories_map = {}
    for i in range(len(categories)):
        if categories.values[i]>=cutoff:
            categories_map[categories.index[i]] = categories.index[i]
        else:
            categories_map[categories.index[i]] = 'Other'
    return categories_map


"""def clean_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)"""
def cleaned_exp(x):
    if x == "More than 50 years":
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


"""def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'"""
def cleaned_edu(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Professional degree'
    return 'Less than a Bachelors'


@st.cache_data
def load_data():
    """df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)
    df = pd.read_csv("survey_results_public.csv")"""
    df=df.rename({'ConvertedCompYearly':"Salary"},axis=1)
    df = df[df["Salary"].notnull()]
    df = df[["Country",'Age','RemoteWork','Employment','EdLevel','YearsCodePro','Salary']]
    df=df.dropna()
    df = df[df["Employment"]=="Employed, full-time"]
    df = df.drop("Employment",axis=1)

    """country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]"""
    country_map = shorten_categories(df['Country'].value_counts(),400)
    df["Country"] = df["Country"].map(country_map)
    data = df.groupby('Country')['Salary'].describe().reset_index()[['Country','25%','75%']]
    df = df.merge(data, on = "Country",how ="left")
    mask = df["Salary"]<df['25%']
    df.loc[mask,"Salary"] = df["25%"]

    mask = df["Salary"]>df['75%']
    df.loc[mask,"Salary"] = df["75%"]
    df.drop(['25%','75%'],axis=1,inplace=True)


    """df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)"""
    df["YearsCodePro"].unique()
    df["YearsCodePro"] = df["YearsCodePro"].apply(cleaned_exp)
    df["YearsCodePro"].unique()

    #apne aap added
    df["EdLevel"].unique()
    df["EdLevel"] = df["EdLevel"].apply(cleaned_edu)
    df["EdLevel"].unique()
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """### Stack Overflow Developer Survey 2023"""
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    patches, texts, _ = ax1.pie(data, autopct="", startangle=90)

    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Adding a legend with color coding
    ax1.legend(patches, data.index, title="Countries", loc="center left", bbox_to_anchor=(1, 0.5))

    # Optionally, you can adjust the layout to avoid overlap
    plt.tight_layout()

    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)


    #fig1, ax1 = plt.subplots()
    #ax1.pie(data, labels=data.index, autopct="%1.0f%%", startangle=90)
    #ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    #st.write("""#### Number of Data from different countries""")

    #st.pyplot(fig1)
    
    st.write(
        """#### Mean Salary Based On Country"""
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """#### Mean Salary Based On Experience"""
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
