from PIL import Image
import os
import streamlit as st
from yaml.loader import SafeLoader
import yaml
from datetime import datetime
import streamlit.components.v1 as com

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data")

image_path = os.path.join(CURRENT_DIR, "logo.png")

if os.path.exists(image_path):
    col1, col2, col3 = st.columns((1, 10, 1))
    with col2:
        st.image(Image.open(image_path))
else:
    st.error('logo.png not found', icon="🚨")


# input file data
share_code = st.text_input("Please enter the code you received")
share_password = st.text_input("Please enter your password", type="password")

if st.button("View"):
    if not share_code:
        st.error("Please enter the sharing code")
    else:
        config_path = os.path.join(DATA_DIR, share_code, "config.yml")
        if not os.path.exists(config_path):
            st.error("Invalid shared code or non-existent code")
        else:
            with open(config_path, "r") as f:
                config = yaml.load(f, Loader=SafeLoader)

            # 설정된 만료 날짜와 비밀번호 확인
            expiry_date = datetime.strptime(config["expiry_date"], "%Y-%m-%d %H:%M:%S")
            stored_password = config["password"]
            expiry_count = config["expiry_count"]
            file_name = config["file_name"]
            current_time = datetime.now()

            if current_time > expiry_date:
                st.error("The shared file has expired")
            elif share_password and share_password != stored_password:
                st.error("Password does not match")
            else:
                if expiry_count <= 0:
                    st.error("The shared file has expired")
                else:
                    # deduct expiration count
                    config["expiry_count"] -= 1
                    with open(config_path, "w") as f:
                        yaml.dump(config, f)

                    # start file downloads
                    file_path = os.path.join(DATA_DIR, share_code, file_name)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="download",
                            data=f,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )
                    st.success("Download is enabled")
