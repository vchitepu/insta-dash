import streamlit as st
import os
import shutil
from streamlit_imagegrid import streamlit_imagegrid
from lib.redfin import RedFinImages

redfin = RedFinImages()


st.set_page_config(
	page_title="Redfin Scraper",
	layout="wide"
)

st.title("RedFin Image Scraper")

with st.form(key="redfin_user_form"):
	url = st.text_input(label="Enter RedFin URL or Home Address ")
	submit = st.form_submit_button(label="Submit")

if submit:
	dir = redfin.download_images(url)
	fp = open('images/{dir}.zip'.format(dir=dir), "rb")
	st.download_button(
		label="Download Images",
		data=fp,
		file_name='images.zip',
		mime='application/zip'
	)
	fp.close()
	shutil.rmtree('images')
