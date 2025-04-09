import sqlite3
from databases import baseSource

class GuestbookDB:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.initialize_connection()
        
    def initialize_connection(self):
        """데이터베이스 연결 초기화"""
        self.conn = baseSource.init()
        self.conn = baseSource.connect()
        self.cursor = self.conn.cursor()
        
    def add_review(self, user_name, user_password, user_review):
        """새 리뷰 추가"""
        try:
            self.cursor.execute(
                "INSERT INTO boards (board_name, password, comment) VALUES (?, ?, ?)", 
                (user_name, user_password, user_review)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            return False, f"데이터베이스 오류: {e}"
    
    def update_likes(self, review_id):
        """리뷰 좋아요 증가"""
        try:
            self.cursor.execute("UPDATE boards SET likes = likes + 1 WHERE board_id = ?", (review_id,))   
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            return False, f"데이터베이스 오류: {e}"
    
    def delete_review(self, review_id):
        """리뷰 삭제"""
        try:
            self.cursor.execute("DELETE FROM boards WHERE board_id = ?", (review_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            return False, f"데이터베이스 오류: {e}"
    
    def update_review(self, review_id, new_comment):
        """리뷰 내용 업데이트"""
        try:
            self.cursor.execute(
                "UPDATE boards SET comment = ?, updated_at = CURRENT_TIMESTAMP WHERE board_id = ?", 
                (new_comment, review_id)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            return False, f"데이터베이스 오류: {e}"
    
    def get_all_reviews(self):
        """모든 리뷰 가져오기"""
        try:
            self.cursor.execute("SELECT * FROM boards ORDER BY created_at DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            return [], f"데이터베이스 오류: {e}"
    
    def get_review_by_id(self, review_id):
        """ID로 특정 리뷰 가져오기"""
        try:
            self.cursor.execute("SELECT * FROM boards WHERE board_id = ?", (review_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            return None, f"데이터베이스 오류: {e}"
    
    def verify_password(self, review_id, password):
        """비밀번호 확인"""
        try:
            self.cursor.execute("SELECT password FROM boards WHERE board_id = ?", (review_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0] == password
            return False
        except sqlite3.Error:
            return False
    
    def close_connection(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()