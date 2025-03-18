import streamlit as st
import base64
import os


def get_image_base64(image_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, image_path)
    
    # 디버깅 정보 출력
    # st.write(f"찾고 있는 이미지 경로: {full_path}")
    # st.write(f"현재 작업 디렉토리: {os.getcwd()}")
    
    if not os.path.exists(full_path):
        st.error(f"⚠️ 파일을 찾을 수 없습니다: {full_path}")
        return None

    with open(full_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

    
def show_team_page():
    # 페이지 기본 설정
    # st.set_page_config(
    #     page_title="행복한 6조 - 팀 소개",
    #     page_icon=":손인사:",
    #     layout="wide"
    # )
    # CSS 스타일 적용
    st.markdown("""
    <style>
        .main {
            background-color: #F5F7FA;
        }
        .title-container {
            background-color: #3D6AFF;
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .team-intro {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .member-card {
            background-color: black;
            width: 350px;
            height: 350px;
            border-radius: 50%;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .member-card:hover {
            transform: translateY(-5px);
        }
        .member-image {
            width: 350px;
            height: 350px;
            background-color: #B8D0FF;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 4rem;
            font-weight: bold;
            border-radius: 50%;
            object-fit: cover;
        }
        .member-info {
            padding: 1.5rem;
        }
        .member-name {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            color: #3D6AFF;
        }
        .member-nickname {
            font-size: 1rem;
            color: #3D6AFF;
            background-color: #EEF2FF;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 1rem;
        }
        .member-details {
            background-color: #F8F9FB;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .member-links a {
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: #3D6AFF;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-right: 0.5rem;
            font-size: 0.9rem;
        }
        .footer {
            text-align: center;
            padding: 2rem 0;
            color: #666;
            font-size: 0.9rem;
        }
        /* 다크 모드 감지 및 스타일 적용 */
        [data-testid="stAppViewContainer"] [data-testid="stHeader"] {
            background-color: #0E1117;
        }
        
        @media (prefers-color-scheme: dark) {
            .member-details {
                background-color: #333333;
                color: white;
            }
        }
    
    /* 다크 모드 추가 감지 방법 */
    [data-testid="stAppViewContainer"][style*="background-color: rgb(14, 17, 23)"] .member-details,
    .dark-theme .member-details {
        background-color: #333333;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    # 헤더 섹션
    st.markdown("""
    <div class="title-container">
        <h1>행복한 6조 <span style="font-size: 1.5rem">(feat. 왕자님과 아이들)</span></h1>
        <p>저희 조는 웃음이 끊기지 않는 행복한 6조랍니다 🌸</p>
    </div>
    """, unsafe_allow_html=True)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # 팀원 데이터
    team_members = [
        {
            "name": "김다은",
            "nickname": "DB공듀",
            "intro": "본 프로젝트를 통해 DB를 제대로 알아버렸습니다.",
            "feature": "허풍이 심함",
            "mbti": "ENFJ",
            "role": "방명록 기능 구현 및 DB 구축",
            "image": "images/da.png"
        },
        {
            "name": "김민주",
            "nickname": "기존쎄갑",
            "intro": "귀여운 말투와 그렇지 못한 팩폭",
            "feature": "부모님 mbti 두분 다 ENTJ",
            "mbti": "ENFP",
            "role": "팀 내 분위기 메이커",
            "image": "images/min.png"
        },
        {
            "name": "손지영",
            "nickname": "이구역통제왕",
            "intro": "좋게 말하면 리더. 사실은 독재자",
            "feature": "출근, 퇴근, 이젠 하다하다 연애까지 통제",
            "mbti": "ENTJ",
            "role": "프로젝트 리더",
            "image": "images/ji.png"
        },
        {
            "name": "이재웅",
            "nickname": "코드학대범",
            "intro": "코드학대로 결과 도출을 담당하고 있습니다.",
            "feature": "코드 실행 횟수 194번은 기본",
            "mbti": "ESFJ",
            "role": "실시간 AI 법률 상담 기능, 기능 통합",
            "image": "images/ung.png"
        },
        {
            "name": "이효정",
            "nickname": "마조리카",
            "intro": "파워 J인데, 여행할 땐 P",
            "feature": "조용한 제2의 코드 학대범",
            "mbti": "INTJ",
            "role": "방명록 기능 구현 및 DB 구축",
            "image": "images/hyo.png"
        },
        {
            "name": "진실",
            "nickname": "성장괴물",
            "intro": "빠르게 성장해서 성장 괴물로 불리고 있습니다.",
            "feature": "트러블 슈팅? 그게 뭔데",
            "mbti": "ISFP",
            "role": "실시간 AI 법률 상담 기능, 방명록 기능 수정",
            "image": "images/jin.png"
        }
    ]
    # 팀원 카드 생성 - Streamlit 방식으로 수정
    cols = st.columns(3)
    for i, member in enumerate(team_members):
        col_index = i % 3
        # 각 팀원마다 카드를 컬럼에 추가
        with cols[col_index]:
            try:
                img_base64 = get_image_base64(member['image'])
                if img_base64:
                    st.markdown(f"""
                        <div class="member-card">
                            <img src="data:image/jpeg;base64,{img_base64}">
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color:red;">⚠️ 이미지 로드 실패</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"이미지 로드 중 오류 발생: {e}")



            # 정보 부분
            st.markdown(f"""
                <div class="member-info">
                    <h2 class="member-name">{member['name']}</h2>
                    <span class="member-nickname">{member['nickname']}</span>
                    <p>🔷 {member['intro']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
                <div class="member-details">
                    <p><strong>특징:</strong> {member['feature']}</p>
                    <p><strong>MBTI:</strong> {member['mbti']}</p>
                    <p><strong>담당 역할:</strong> {member['role']}</p>
                </div>
                """, unsafe_allow_html=True)

