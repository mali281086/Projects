import string
import streamlit as st
import pickle
import webbrowser

global langdet_model

langdet_file = open('model.pckl','rb')
langdet_model = pickle.load(langdet_file)
langdet_file.close()
st.title("Language Detection Tool")
input_test = st.text_input("Provide your text input here","Some shit thing")

button_clicked = st.button("Get Language Name")
if button_clicked:
    st.text(langdet_model.predict([input_test]))
