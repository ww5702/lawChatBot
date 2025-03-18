import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: center;
            color: #3d6aff;
        }
        
        .main-subtitle {
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 2rem;
            color: #4B5563;
        }
        
        .center-button {
            display: flex;
            justify-content: center;
            margin: 2rem 0;
        }
        
        
        .lawyer-info {
            padding: 15px;
            border-radius: 10px;
            background-color: #f8f9fa;
            margin-bottom: 15px;
            transition: transform 0.3s ease;
        }

        .st-emotion-cache-iyz50i {
            transition: transform 0.3s all ease;
        }       
                
        .st-emotion-cache-iyz50i:hover {
            border-color: rgb(255, 75, 75);
            color: rgb(255, 75, 75);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
                
                
        .emoji-large {
            font-size: 48px;
            margin-bottom: 10px;
        }
        
        .lawyer-name {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        .lawyer-specialty {
            font-size: 18px;
            color: #3d6aff;
            margin-bottom: 8px;
        }
        
        .lawyer-personality {
            font-size: 16px;
            color: #4B5563;
            margin-bottom: 15px;
        }
        
        .lawyer-description {
            white-space: pre-line;
            font-size: 14px;
        }
        
        .selected-lawyer {
            background-color: #F1F5F9;
            padding: 3rem;
            padding-bottom: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;

        }
        
        .home-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
            text-align: center;
            padding: 2rem;
        }
        
        .home-image {
            font-size: 100px;
            margin-bottom: 2rem;
        }
        
        .home-title {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #3d6aff;
        }
        
        .home-subtitle {
            font-size: 1.5rem;
            color: #4B5563;
            margin-bottom: 3rem;
        }
        
        .big-button {
            padding: 0.75rem 2rem;
            font-size: 1.2rem;
            border-radius: 8px;
            background-color: #E53935;
            color: white;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .big-button:hover {
            background-color: #C62828;
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        /* ✅ 다크모드 스타일 추가 */
        @media (prefers-color-scheme: dark) {
            .lawyer-info {
                background-color: #1E1E1E !important; /* 검은 배경 */
                color: #FFFFFF !important; /* 흰 글씨 */
                border: 1px solid #555 !important;
            }
            
            .selected-lawyer {
                background-color: #121212 !important; /* 어두운 배경 */
                color: #FFFFFF !important; /* 흰 글씨 */
                border: 1px solid #555 !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
