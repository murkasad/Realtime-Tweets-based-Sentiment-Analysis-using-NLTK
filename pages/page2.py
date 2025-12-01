import streamlit as st
from streamlit_option_menu import option_menu
from realtime_analysis import tweet_extraction


if "username" in st.session_state: #check if any user logged in,every time a user logs in, it is saved in session
    st.write("Hello ",st.session_state["username"],"!")

st.title("Real time Tweets")  # Display name for this page

# Initialize session state
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "Home"

# Sidebar menu
with st.sidebar:
    menu = option_menu(
        menu_title="Main Menu",
        options=["Home", "Simulation", "Real-time Analysis","Sign Up", "Log Out"],
        icons=["house", "clipboard-pulse", "clipboard-data-fill","database-fill-add", "arrow-right-square"], #values obtained from bootstrap website
        default_index=["Home", "Simulation", "Real-time Analysis","Sign Up", "Log Out"].index(st.session_state.selected_menu)
    )


# Update session state and navigate
if menu != st.session_state.selected_menu:
    st.session_state.selected_menu = menu
    if menu == "Home":
        st.switch_page("User_Interface.py")        # Navigate back to main page
    elif menu=="Simulation":
        st.switch_page("pages/page1.py")
    elif menu=="Log Out":
        if "username" in st.session_state:
            del st.session_state["username"]
        st.switch_page("User_Interface.py")
        st.write("Logged Out!")
        st.session_state.selected_menu ="Home"
    elif menu=="Sign Up":
        st.switch_page("pages/SignUp.py")

# Simulation page content
if st.session_state.selected_menu == "Real-time Analysis":
    st.write("Realtime stream of tweets from Twitter")

    #asking user to input a word/topic
    u_input= st.text_input("Enter a topic/keyword")

    #search tweets of the given topic in old tweets
    if st.button("Search Tweets"):
        top_positive, top_negative, top_neutral, percent_pos, percent_neg, percent_neu = tweet_extraction(u_input)
        st.write("Tweets Extracted, Analysis Done!")
        
        st.session_state["top_positive"]=top_positive #saving data otherwise it vanishes away, since this is done inside it, reloading page after clicking anybutton removes everything
        st.session_state["top_negative"]=top_negative
        st.session_state["top_neutral"]=top_neutral
        st.session_state["percent_pos"]=percent_pos
        st.session_state["percent_neu"]=percent_neu
        st.session_state["percent_neg"]=percent_neg
        st.session_state["u_input"]=u_input
    
    if "u_input" in st.session_state:
        #once tweets have generated now give the options to display statistics

        #reassign to make these variables for global use
        top_positive=st.session_state["top_positive"] 
        top_negative=st.session_state["top_negative"]
        top_neutral=st.session_state["top_neutral"]
        percent_pos=st.session_state["percent_pos"]
        percent_neu=st.session_state["percent_neu"]
        percent_neg=st.session_state["percent_neg"]
        u_input=st.session_state["u_input"]


        #for a better layout of output results, put them in a container or placeholder
        col1, col2, col3=st.columns(3)

        with col1:
            if st.button("Get Sentiment Percentage"):
                st.write(f"{percent_pos} % Positive Sentiments")
                st.write(f"{percent_neg} % Negative Sentiments") 
                st.write(f"{percent_neu} % Neutral Sentiments") 

        with col2:
            if st.button("Get Top Postive Tweets"):
                st.write(top_positive)
        with col3:  
            if st.button("Get Top Negative Tweets"):
                st.write(top_negative)


