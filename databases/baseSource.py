import os
import sqlite3
import streamlit as st

# DB 연동
#conn = sqlite3.connect('databases/user_review.db', check_same_thread=False)  

# 현재 실행 파일 기준으로 절대 경로 설정

def connect():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(base_dir, "db")

    # 폴더가 없으면 생성
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    db_path = os.path.join(db_folder, "reviews.db")

    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

# @st.cache_resource -> 최초 실행 시 오류남. 그냥 중복 방지로 실행 가능 
def init():
    conn = connect()
    cursor = conn.cursor()

    # DB 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boards (
            board_id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            comment TEXT NOT NULL,
            likes INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 좋아요 기록 테이블 생성 (사용자가 어떤 댓글에 좋아요를 눌렀는지 기록)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS like_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            UNIQUE(board_id, session_id)
        )
    ''')

    # 전체 조회수 기록 테이블
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS view_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            view_type TEXT NOT NULL,
            view_count INTEGER NOT NULL DEFAULT 0
        )
    ''')

    cursor.executemany("INSERT OR IGNORE INTO view_records (view_type) VALUES (?)", [("total_view",), ("user_view",), ("report_view",)])

    conn.commit()
    return conn

def updateView(view_type):
    conn = connect()
    cursor = conn.cursor()
    
    # 현재 조회수 가져오기
    cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'user_view'")
    user_view = cursor.fetchone()[0]
    
    cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'report_view'")
    report_view = cursor.fetchone()[0]
    
    # 조회수 업데이트
    if view_type == "user_view":
        user_view += 1
        cursor.execute("UPDATE view_records SET view_count = ? WHERE view_type = 'user_view'", (user_view,))
    
    if view_type == "report_view":
        report_view += 1
        cursor.execute("UPDATE view_records SET view_count = ? WHERE view_type = 'report_view'", (report_view,))
    
    # 전체 조회수 업데이트
    total_view = user_view + report_view
    cursor.execute("UPDATE view_records SET view_count = ? WHERE view_type = 'total_view'", (total_view,))
    
    conn.commit()
    conn.close()