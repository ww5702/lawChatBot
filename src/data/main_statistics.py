import streamlit as st

def render_statistics(conn, cursor):
    """통계 데이터를 표시합니다."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'user_view'")
        user_view = cursor.fetchall()[0][0]
        st.metric(label="누적 상담 건수", value=user_view)
        conn.commit()
        
    with col2:
        cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'report_view'")
        report_view = cursor.fetchall()[0][0]
        st.metric(label="누적 보고서 생성 수", value=report_view)
        conn.commit()
    
    with col3:
        cursor.execute("SELECT view_count FROM view_records WHERE view_type = 'total_view'")
        total_view = cursor.fetchall()[0][0]
        st.metric(label="총 누적 사용 수", value=total_view)
        conn.commit()