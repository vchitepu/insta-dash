import streamlit as st
import os
import re
import shutil
from lib.redfin import RedFinImages
from lib.videowriter import VideoWriter

redfin = RedFinImages()

def check_user_input(f_name, l_name, email, url, images):
	missing = []
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
	if (f_name == ''):
		missing.append("First Name")
	if (l_name == ''):
		missing.append("First Name")
	if (email == ''):
		missing.append("Email")
	if len(missing) > 0:
		message = "Missing the following fields: " + str(missing)
		return [False, message]

	if not (re.fullmatch(regex, email)):
		return [False, "Please enter a valid email address"]

	if (url == '') and (images == []):
		return [False, "Please enter either a URL/Home Adress or Upload Images"]
	if (url != '') and (images != []):
		return [False, "Please enter either a URL/Home Adress or Upload Images. But not both"]

	return [True, "Generating your reel. Please wait"]

st.set_page_config(
	page_title="LeadState Reel Generator",
	layout="wide"
)

st.title("LeadState Reel Generator :film_projector:")

with st.form(key="reel_user_form", clear_on_submit=True):
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
	res = check_user_input(f_name, l_name, email, url, images)
	if res[0] == False:
		st.error(res[1])
	else:
		st.success(res[1])
		dir = redfin.download_images(url)
		vw = VideoWriter(dir)
		vw.generate_video()
		fp = open('images/{dir}.avi'.format(dir=dir), "rb")
		st.download_button(
			label="Download Video",
			data=fp,
			file_name='video.avi',
			mime='video/avi'
		)
		fp.close()
		shutil.rmtree('images')
