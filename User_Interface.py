import streamlit as st
from streamlit_option_menu import option_menu
import pyarrow
from login import test_signin_credentials

if "username" in st.session_state: #check if any user logged in,every time a user logs in, it is saved in session
    st.write("Hello ",st.session_state["username"],"!")

st.title("Home")  # Display name for main page

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
    if menu == "Simulation":
        st.switch_page("pages/page1.py")
    elif menu=="Real-time Analysis":
        st.switch_page("pages/page2.py")
    elif menu=="Log Out": #go back to home
        if "username" in st.session_state:
            del st.session_state["username"]
        st.switch_page("User_Interface.py")
        st.write("Logged Out!")
        st.session_state.selected_menu ="Home"
    elif menu=="Sign Up":
        st.switch_page("pages/SignUp.py")


# Main page content
if st.session_state.selected_menu == "Home":
    st.write(
        "Obtain real-time tweets from Twitter and get sentiment analysis based on the results"
    )

    st.subheader("Log In")
    username = st.text_input("User name")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        user_details={'username':username, 'password':password}
        status = test_signin_credentials(user_details)
        st.write(status)
        st.session_state["username"]=username
        
