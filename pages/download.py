from PIL import Image
import os
import streamlit as st
from yaml.loader import SafeLoader
import yaml
from datetime import datetime
import streamlit.components.v1 as com

# 현재 디렉토리 설정
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data")

# 로고 이미지 경로 설정
image_path = os.path.join(CURRENT_DIR, "logo.png")

# 버튼 및 로고 위치 수정
if os.path.exists(image_path):
    col1, col2, col3 = st.columns((1, 10, 1))
    with col2:
        st.image(Image.open(image_path))
else:
    st.error('Backend img load ERROR, Try later', icon="🚨")

with st.sidebar:
    st.title(":violet[What is Hyperlink?]")
    st.write("Hyperlink는 빠르고 간편한 파일 공유 서비스입니다. 데이터 익명성을 최우선으로 보장하며, 대용량 파일의 쉬운 공유를 지원합니다. (최대 업로드 용량: 10GB) 업로드된 파일은 지정된 기간 또는 횟수가 도달하면 즉시 영구 삭제됩니다")
    st.title(":blue[Have a problem? Contact us]")
    st.write("Email: octaxinc@gmail.com")
    st.write("Discord: @gaegeumchi")
    st.title(":orange[Powered by OctaX]")




# 사용자 입력 받기
share_code = st.text_input("공유받으신 코드를 입력해주세요")
share_password = st.text_input("비밀번호를 입력해주세요", type="password")

if st.button("조회하기"):
    if not share_code:
        st.error("공유코드를 입력해주세요")
    else:
        config_path = os.path.join(DATA_DIR, share_code, "config.yml")
        if not os.path.exists(config_path):
            st.error("유효하지 않는 공유코드 또는 존재하지 않는 코드입니다")
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
                st.error("공유된 파일이 만료되었습니다")
            elif share_password and share_password != stored_password:
                st.error("비밀번호가 일치하지 않습니다")
            else:
                if expiry_count <= 0:
                    st.error("공유된 파일이 만료되었습니다")
                else:
                    # 만료 횟수 차감
                    config["expiry_count"] -= 1
                    with open(config_path, "w") as f:
                        yaml.dump(config, f)

                    # 파일 다운로드 제공
                    file_path = os.path.join(DATA_DIR, share_code, file_name)
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="다운로드",
                            data=f,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )
                    st.success("다운로드가 허가되었습니다")

st.markdown("""
    <ins class="kakao_ad_area" style="display:none;"
    data-ad-unit = "DAN-VOns6Ms72o5v5zxW"
    data-ad-width = "320"
    data-ad-height = "100"></ins>
    <script type="text/javascript" src="//t1.daumcdn.net/kas/static/ba.min.js" async></script>     
    """, unsafe_allow_html=True
)
