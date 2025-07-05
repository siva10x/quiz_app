import streamlit as st
import sys
import os

# Include app/utils in sys.path to import data_loader
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from data_loader import get_grades, get_subjects, get_lessons, get_topics

st.set_page_config(page_title="QuizPro", layout="centered")
st.title("QuizPro")
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="baseButton-headerNoPadding"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.markdown("#### Select your quiz options 👇")

# Grade selection
grades = get_grades()
grade_options = ["-- Select Grade --"] + [g['name'] for g in grades]
grade_selected = st.selectbox("Select Grade:", grade_options)

if grade_selected != "-- Select Grade --":
    grade_id = next(g['grade_id'] for g in grades if g['name'] == grade_selected)
    st.session_state.grade = grade_id

    # Subject selection
    subjects = get_subjects(grade_id)
    subject_options = ["-- Select Subject --"] + [s['name'] for s in subjects]
    subject_selected = st.selectbox("Select Subject:", subject_options)

    if subject_selected != "-- Select Subject --":
        subject_id = next(s['subject_id'] for s in subjects if s['name'] == subject_selected)
        st.session_state.subject = subject_id

        # Lesson selection
        lessons = get_lessons(grade_id, subject_id)
        lesson_options = ["-- Select Lesson --"] + [l['name'] for l in lessons]
        lesson_selected = st.selectbox("Select Lesson:", lesson_options)

        if lesson_selected != "-- Select Lesson --":
            lesson_id = next(l['lesson_id'] for l in lessons if l['name'] == lesson_selected)
            st.session_state.lesson = lesson_id

            # Topic selection
            topics = get_topics(grade_id, subject_id, lesson_id)
            topic_options = ["-- Select Topic --"] + [t['name'] for t in topics]
            topic_selected = st.selectbox("Select Topic:", topic_options)

            if topic_selected != "-- Select Topic --":
                topic_id = next(t['topic_id'] for t in topics if t['name'] == topic_selected)
                st.session_state.topic = topic_id

                # Start Quiz button
                if st.button("🚀 Start Quiz"):
                    # Clear only quiz-specific session state — keep selection state intact
                    for key in ['question_index', 'answers', 'quiz_submitted']:
                        if key in st.session_state:
                            del st.session_state[key]

                    st.switch_page("pages/quiz.py")

st.markdown("---")
st.write("Made with ❤️ using Streamlit.")