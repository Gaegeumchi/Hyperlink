from PIL import Image
import os
import streamlit as st
import yaml
from datetime import datetime, timedelta
import random
import string
# import streamlit.components.v1 as com

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data")

image_path = os.path.join(CURRENT_DIR, "logo.png")

if os.path.exists(image_path):
    col1, col2, col3 = st.columns((1, 10, 1))
    with col2:
        st.image(Image.open(image_path))
else:
    st.error('logo.png not found', icon="🚨")


# file upload logic
uploaded_file = st.file_uploader("Please select the file to upload")
expiry_date_input = st.date_input("Expiration date (defaults to one week if not specified)", value=None)
expiry_count = st.number_input("Expiration count", value=1, min_value=1, step=1, format="%d", placeholder="Type a number...")
password = st.text_input("Password (If left blank, there is no password.)", type="password")

if st.button("Upload!", type="primary"):
    if not uploaded_file:
        st.error("Please upload the file first")
    else:
        # set expiration date
        if expiry_date_input is None:
            expiry_date = datetime.now() + timedelta(days=1)
        else:
            expiry_date = datetime.combine(expiry_date_input, datetime.min.time())
            if expiry_date <= datetime.now():
                st.error("You cannot set the expiration date in the past!")
                st.stop()
            if expiry_date > datetime.now() + timedelta(days=7):
                st.error("The expiration date cannot exceed 7 days!")
                st.stop()

        # generate random sharing code
        share_code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        share_folder = os.path.join(DATA_DIR, share_code)
        os.makedirs(share_folder, exist_ok=True)

        # save file
        file_path = os.path.join(share_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # save settings
        config = {
            "expiry_date": expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
            "password": password,
            "expiry_count": expiry_count,
            "file_name": uploaded_file.name
        }
        config_path = os.path.join(share_folder, "config.yml")
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        st.success(f"File upload was successful! Share code: :orange[{share_code}]")
