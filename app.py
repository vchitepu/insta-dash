import streamlit as st
import os
import shutil
from lib.redfin import RedFinImages

redfin = RedFinImages()

def check_user_input(f_name, l_name, email, url, images):
	if (f_name == '') or (l_name == '') or (email == ''):
		return False
	elif (url == '') and (images == None):
		return False
	elif (url != '') and (images != None):
		return False
	return True

st.set_page_config(
	page_title="LeadState Reel Generator",
	layout="wide"
)

st.title("LeadState Reel Generator :film_projector:")

with st.form(key="redfin_user_form"):
	st.subheader("User Information")
	st.write("General information so we know where to send the video")
	col1, col2 = st.columns(2)
	with col1:
		f_name = st.text_input(label="First Name")
	with col2:
		l_name = st.text_input(label="Last Name")
	email = st.text_input(label="Email")
	st.text("")
	st.text("")
	st.subheader("Provide some images")
	st.write("Give us your own images or provide a home address/RedFin URL")
	url = st.text_input(label="Enter RedFin URL or Home Address")
	st.text("or")
	images = st.file_uploader("Upload images", accept_multiple_files=True)
	submit = st.form_submit_button(label="Submit")


if submit:
	if check_user_input(f_name, l_name, email, url, images) == False:
		st.error("Please fill out all required fields")
	else:
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
