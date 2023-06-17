import streamlit as st
import pandas as pd
import plotly.express as px
import json
import time
import utils as ut
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner 



@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

favicon = open("favicon-gold.ico", "rb").read()

def setdf(year,exam):
    df = ut.get_df(year,exam)

st.set_page_config(
    page_title="RankSage",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="auto",
)


with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
@st.cache_data
def home():
    col1,col2 = st.columns([2,1])
    col1.title("Welcome to Jee RankSage")
    col1.markdown("[![GitHub stars](https://img.shields.io/github/stars/your-username/your-repository.svg?style=social)](https://github.com/your-username/your-repository)")
    with col2:
        lottie = load_lottiefile("img/started.json")
        st_lottie(
        lottie,
        speed=1,
        reverse=False,
        loop=True,
        quality="high", # canvas
        height=150,
        width=150,
        key="All",) 
    st.divider()
    with st.expander("**Introduction to RankSage**",expanded=True):
        st.subheader("Introduction")
        st.write("JEE RankSage: Your Ultimate JEE Counseling Companion! :dart:")
        st.write('''* This is a no spam , straight to the point site.''')
        st.write( '''* It will help you in making better decisions for counseling process using datasets like this''')
        st.dataframe(pd.read_csv("data/2022/DataFinal.csv"))
        st.write('''* Below is a short explanation of each tab(or hints are provided)''')
        st.write('''* Do share with any aspirants , if you like this''')
        st.write('''* you can collapse this part now''')
    st.divider()
    with st.expander("**Exproler**",expanded=False):
        st.subheader("Filters everywhere")
        st.write("As easy as previous cutoff search can be :wrench:")
        st.write('''* Just choose a year and an exam (2021 currently not available)''')
        st.write( '''* Choose appropriate filters , the institute and program are multiselect filters so you can select only choices that you want.''')
        st.write('''* Results will be displayed(better viewed fullscreen), feel free to click on column names to filter them''')
        st.write('''* Download as csv and convert it to pdf for better viewing on mobile''')
        st.write('''* you can collapse this part now''')
    st.divider()
    with st.expander("**Trends**",expanded=False):
        st.subheader("Graphs for you :chart:")
        st.write(''' * Choose from two types of graph''')
        st.write(''' 1. Program level  : this graph is better for seeing trend of particular branch ''')
        st.write(''' 2. Institute Level : this graph is better for seeing trend of Institute as a whole.''')
        st.write('''* Input Data and click submit''')
        st.write( '''* Genereal Trends:''')
        st.write('''1. If the graph is going upwards , cutoff most likely will increase''')
        st.write('''2. If the graph is going downwards , cutoff most likely will decrease''')
        st.write('''3. Stagnated Graph/ no trend , cutoff more likely nearly to remain same unless some event''')
    
    
    
    
def exproler():
    st.title("Rank Exproler")
    st.divider()
    st.subheader("Basic Setup")
    with st.expander(":gear:",expanded=True):
        year = st.select_slider("Year",[2016,2017,2018,2019,2020,2022],value=2022)
        exam = st.selectbox("Exam",["Jee Mains","Jee Advanced"],index=0)
    # done = st.button("Done",on_click=setdf(year,exam))
    # st.write("Click ⬆ this button again to change Year or Exam")
    # if done:
    #     df = ut.get_df(year,exam)
    # else:
    df = ut.get_df(year,exam)
    st.divider()
    st.subheader("Filters")
    institutes = ut.get_institutes(df,all=True)
    academic_programs = ut.get_programs(df,all=True)
    quotas = ut.get_quota(df,all=True)
    seatTypes = ut.get_seatType(df,all=True)
    genders = ut.get_gender(df,all=True)

    #Form inputs
    institute = st.multiselect("**Institute**", institutes,default="All")
    academic_program = st.multiselect("**Academic Program**", academic_programs,default="All")
    quota = st.selectbox("Quota", quotas)
    seatType = st.selectbox("Seat Type",seatTypes)
    gender = st.selectbox("Gender", genders)
    rank = st.number_input(label = "Rank(Put according to Seat Type)",value=0)
    # Submit button
    submitted = st.button("Submit :rocket:")
        
    # Display submitted form values
    if submitted:
        submitted = 0
        lottieload = load_lottiefile("img/loader.json")
        with st_lottie_spinner(lottieload,reverse=1, loop=True,quality="high", height=100, width=100, key="download"):
            time.sleep(1) 
        st.success("Sucessfully submitted")
        st.divider()
        st.subheader("Results")
        result = ut.apply_filters(df,institute,academic_program,quota,seatType,gender,rank)
        result = result.sort_values(by='Closing Rank')
        csv = convert_df(result)
        st.download_button(
            "Download as CSV",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv',
        )
        st.write("Hint : Convert to Pdf")
        st.write("Hint2 : Clicking on Column name sorts it")
        st.warning("Tldr : Clicking Download will remove current Results",icon="⚠")
        st.dataframe(result,use_container_width=True,hide_index=True)

def trends():
    #st.markdown('<iframe src="https://cutoffs.iitr.ac.in/" width="800" height="600"></iframe>', unsafe_allow_html=True)
    st.title("Trend Analyzer")
    st.divider()
    trend = st.selectbox("**Select Visualizer**",["Institute Level","Program Level"],index=0)
    
    if(trend == "Program Level"):
        with st.expander("Data :chart_with_upwards_trend:",expanded=True):
            st.subheader("Basic")
            exam = st.selectbox("Exam",["Jee Mains","Jee Advanced"],index=0)
            if(exam == "Jee Advanced"):
                df = pd.read_csv("data/All/AdvAll.csv")
            else:
                df = pd.read_csv("data/All/MainsAll.csv")
            st.divider()
            st.subheader("Advanced")
            institutes = ut.get_institutes(df)
            academic_programs = ut.get_programs(df)
            quotas = ut.get_quota(df)
            seatTypes = ut.get_seatType(df)
            genders = ut.get_gender(df)

    
            institute = st.selectbox("Institute", institutes,index=1)
            academic_program = st.selectbox("Academic Program", academic_programs,index = 4)
            quota = st.selectbox("Quota", quotas)
            seatType = st.selectbox("Seat Type",seatTypes)
            gender = st.selectbox("Gender", genders)
            #rank = st.number_input(label = "Rank(Put according to Quota)",value=0)
            
            submitted = st.button("Submit :rocket:")
        if submitted:
            result = ut.apply_filters(df,[institute],[academic_program],quota,seatType,gender,0)
            
            lottieload = load_lottiefile("img/loader.json")
            with st_lottie_spinner(lottieload,reverse=1, loop=True,quality="high", height=100, width=100, key="download"):
                time.sleep(1)
                st.divider()
                st.subheader("Plot")
                fig = ut.plotter_program(result)
                st.plotly_chart(fig,use_container_width=True,theme=None)
    elif(trend == "Institute Level"):
        with st.expander("Data :chart_with_upwards_trend:",expanded=True):
            st.subheader("Basic")
            exam = st.selectbox("Exam",["Jee Mains","Jee Advanced"],index=0)
            if(exam == "Jee Advanced"):
                df = pd.read_csv("data/All/AdvAll.csv")
            else:
                df = pd.read_csv("data/All/MainsAll.csv")
            st.divider()
            st.subheader("Advanced")
            institutes = ut.get_institutes(df)
            quotas = ut.get_quota(df)
            seatTypes = ut.get_seatType(df)
            genders = ut.get_gender(df)

    
            institute = st.selectbox("Institute", institutes,index=1)
            quota = st.selectbox("Quota", quotas)
            seatType = st.selectbox("Seat Type",seatTypes)
            gender = st.selectbox("Gender", genders)
            #rank = st.number_input(label = "Rank(Put according to Quota)",value=0)
            
            submitted = st.button("Submit")
        if submitted:
            result = ut.apply_filters(df,[institute],["All"],quota,seatType,gender,0)
            
            lottieload = load_lottiefile("img/loader.json")
            with st_lottie_spinner(lottieload,reverse=1, loop=True,quality="high", height=100, width=100, key="download"):
                time.sleep(1)
                st.divider()
                st.subheader("Plot")
                st.write("Hint : Go fullscreen by clicking on right side icon")
                st.write("Hint2 : Clicking on Program name disables it, and double click isolates it")
                fig = ut.plotter_institute(result,institute)
                st.plotly_chart(fig,use_container_width=True)
        




# Navbar
with st.sidebar:
    nav = option_menu("Jee RankSage", ["Home", "Explorer","Trends"], 
        icons=['house', 'signpost-split','reception-4'], 
        menu_icon="sunrise", 
        default_index=0,
        styles={ 
        "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500&display=swap')"
        "container": {"font-family": "Montserrat"},
        "nav-link": { "fony-size":"25px","--hover-color": "#FF4B4B"},
        }
        )
    
    
if nav == "Home":
    home()
elif nav == "Explorer":
    exproler()
elif nav == "Trends":
    trends()

