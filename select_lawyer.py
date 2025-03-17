import base64
import streamlit as st

# CSS 스타일
def load_css():
    st.markdown("""
    <style>
        .container-card {
            background-color: white;
            border-radius: 10px;
            padding: rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .modal-title {
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: center;
        }

        .lawyer-card {
            border-radius: 10px;
            border: 1px solid #E5E7EB;
            padding: 1rem;
            background-color: white;
            transition: all 0.3s;
            height: 100%;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;  /* 가로 중앙 정렬 */
            justify-content: center; /* 세로 중앙 정렬 */
            text-align: center; /* 텍스트 중앙 정렬 */
        }
        
        .lawyer-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            transform: translateY(-5px);
        }
        
        .selected {
            border: 3px solid #e77d2f;
            box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.3);
        }
        
        .lawyer-name {
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 0.5rem;
            color: #1E3A8A;
        }
        
        .lawyer-specialty {
            color: #4B5563;
            font-weight: 500;
        }
        
        .lawyer-description {
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #6B7280;
        }
        
        .select-button {
            background-color: #1E3A8A;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            font-weight: bold;
        }
        
        .select-button:hover {
            background-color: #1E40AF;
        }
        
        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .profile-img {
            border-radius: 50%;
            object-fit: cover;
        }
    </style>
    """, unsafe_allow_html=True)

# 변호사 데이터
def get_lawyers():
    return [
            {
                "id":1,
                "name": "손지영", 
                "specialty": '"백전 백승, 무패의 전설 !!! 상대가 누구든 다 뿌셔드립니다."<br> • 성격: ENTJ (의뢰인에게도 화낼 수 있음 주의) <br> ',
                "description": '• 대원한국어고등학교 졸업 (2005)<br>  • 한국대학교 물리학과 학사 (2010)<br>  • 한국대학교 법학전문대학교 법학전문 석사 (2013)<br>  • 김앤손 법률 사무소 (2008 ~ 2015)<br>  • 사고닷 법률 사무소 (2015 ~ 현재)<br>',
                "image": "images/손지영.png"
            },
            {
                "id":2,
                "name": "김민주", 
                "specialty": '"법과 정의, 그리고 사람. <br>  혼자가 아닌 서비스를 제공하기 위해 최선을 다하겠습니다."<br>  • 성격: ENFP (긍정적 사고 전문)<br>', 
                "description": '• 제 7회 변호사시험 합격 (2007)<br>  • 비빔대학교 법학전문대학원 (법학전문석사, 수석 졸업, 2007)<br>  • 비빔대학교 (법학/문학, 무사 졸업, 2005)<br>  • 사고닷 법률사무소 (2020 - 현재)<br>',
                "image": "images/김민주.png"
            },
            {
                "id":3,
                "name": "김다은", 
                "specialty": '"시켜줘 그럼, SKALA 명예 변호사"<br>  • 성격: ESTJ (인성은 글쎄? 근데 이기면 되잖아)<br>', 
                "description": '• 내 머리는 너무나 나빠서 너 하나밖에 난 모른대학교<br>  (법학스칼라전문박사, 박사 졸업, 2016)<br>  • 하버드 법학대학원 (법학 박사, 2005)<br>  • 국제 법률 자문관 (2015 - 2025)<br>  • 사고닷 법률 사무소 변호사 (2016 - 현재)<br>  • SKALA 명예 변호사로 활동 (2018 - 현재)<br>',
                "image": "images/김다은.png"
            },
            {
                "id":4,
                "name": "이재웅", 
                "specialty": '"자신이 없습니다. 질 자신이.<br>  가장 확실한 해결책, 포기 없는 변호."<br>  • 성격 : INFJ (근데 사실 T임)<br>', 
                "description": '• 한국대학교 법학전문대학학원<br>  (법학스칼라전문박사, 박사 졸업, 2018)<br>  • 너뭐대학교<br>  (한국사, 문학과, 수석 졸업, 2015)<br>  • 사고닷 법률 사무소 (2016 - 현재)<br><br>',
                "image": "images/이재웅.png"
            },
            {
                "id":5,
                "name": "진실", 
                "specialty": '"믿음, 소망, 사랑, 그중에 제일은 사랑이라.<br>  이혼 전문 맡겨만 주세요."<br>  • 성격: ISFP (공감 잘함. 의뢰인과 울음 대결 가능)<br>', 
                "description": '• 제9회 변호사시험 합격 (2020)<br>  • 한국대학교 법학전문대학원<br>(법학스칼라전문석사, 수석졸업, 2020)<br>  • 두번 다시 사랑모대학교<br>  (문학사, 서양사학, 수석졸업, 2017)<br>  • 사고닷 법률사무소 (2020-현재)<br>',
                "image": "images/진실.png"
            },
            {
                "id":6,
                "name": "이효정", 
                "specialty": '"오직 노동자만을 위한<br>  노동자의, 노동자에 의한, 노동자를 위한 법률 서비스"<br>  • 성격: INTJ (노동자에게만 F)<br>',
                "description": '• 한국대학교(법학, 2020)<br>  • 한국대학교 법학전문대학원(법학전문석사, 2023)<br>  • 한국노동교육원 법률 자문(2023 - 현재)<br>  • 사고닷 법률 사무소(2024 - 현재)<br><br><br>', 
                "image": "images/이효정.png"
            }
    ]

# 세션 상태 초기화 함수
def init_session_state():
    if 'confirmed_lawyer' not in st.session_state:
        st.session_state.confirmed_lawyer = None
    
# 변호사 매칭 완료 함수
def confirm_selection(lawyer_id):
    st.session_state.confirmed_lawyer = lawyer_id

# 모달 닫기 함수
def close_modal():
    st.session_state.show_modal = False

def get_base64_image(image_path):
    """이미지를 Base64로 변환"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# 변호사 선택 화면 표시 함수
def show_lawyer_selection_modal():

    # 세션 상태 초기화
    init_session_state()
    
    # CSS 로드
    load_css()
    
    # 변호사 선택 카드 컨테이너
    st.markdown("<h2 class='modal-title'>원하시는 변호사를 선택해 주세요!</h2>", unsafe_allow_html=True)
    
    # 변호사 카드 표시
    lawyers = get_lawyers()
    cols = st.columns(3)
    for i, lawyer in enumerate(lawyers):
        with cols[i % 3]:
            # 선택된 변호사 스타일 적용
            card_class = "lawyer-card"
            if st.session_state.confirmed_lawyer == lawyer["id"]:
                card_class += " selected"

            local_image_path = lawyer["image"]  # 같은 디렉토리에 있는 경우
            image_base64 = get_base64_image(local_image_path)

            # 변호사 정보 출력
            st.markdown(f"""
                <div class='{card_class}' style="
                    border: 1px solid #ddd;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    max-width: 300px;
                    margin: auto;
                ">
                    <img src="data:image/png;base64,{image_base64}" width=150 alt="변호사 사진">
                    <div style="font-size: 20px; font-weight: bold;">{lawyer['name']} 변호사</div>
                    <div style="font-size: 16px; font-weight: bold;">{lawyer['specialty']}</div>
                    <div style="margin-top: 10px;">{lawyer['description']}</div>
                </div>
            """, unsafe_allow_html=True)

            # 버튼 추가 (개별 변호사 ID를 처리)
            if st.button(f"{lawyer['name']} 변호사 매칭하기!", key=f"match_{lawyer['id']}", use_container_width=True):
                confirm_selection(lawyer["id"])
                print(f"Selected Lawyer ID: {lawyer['id']}")  # 콘솔 출력
    
    st.markdown("</div>", unsafe_allow_html=True)

# 이 모듈을 직접 실행했을 때의 테스트 코드
if __name__ == "__main__":
    st.set_page_config(page_title="변호사 선택 테스트", layout="wide")
    show_lawyer_selection_modal()