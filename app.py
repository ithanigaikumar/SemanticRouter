import streamlit as st

# Main title
st.title("Your Application Name")

# Sidebar
st.sidebar.title("Configuration")
user_key = st.sidebar.text_input("Enter your UNIFY_KEY", value="")

# Displaying the entered UNIFY_KEY in the main page to confirm it's been entered
st.write("The current UNIFY_KEY is:", user_key)
