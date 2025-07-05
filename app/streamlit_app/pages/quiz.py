import streamlit as st
import sys
import os

# Include app/utils in sys.path to import data_loader
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from data_loader import (
    get_questions_by_topic,
    get_grades,
    get_subjects,
    get_lessons,
    get_topics
)

st.set_page_config(page_title="📚 QuizPro", layout="centered")
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="baseButton-headerNoPadding"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

if 'topic' not in st.session_state or not st.session_state.topic:
    st.error("⚠️ No topic selected. Please go back and select options first.")
    st.markdown("---")
    st.page_link("main.py", label="🏠 Back to Home")
    st.stop()

# Load questions
questions = get_questions_by_topic(
    st.session_state.grade,
    st.session_state.subject,
    st.session_state.lesson,
    st.session_state.topic
)

if not questions:
    st.warning("No questions found for this topic.")
    st.markdown("---")
    st.page_link("main.py", label="🏠 Back to Home")
    st.stop()

# Initialize state variables
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Fetch selected names for breadcrumb
grade_name = next(g['name'] for g in get_grades() if g['grade_id'] == st.session_state.grade)
subject_name = next(s['name'] for s in get_subjects(st.session_state.grade) if s['subject_id'] == st.session_state.subject)
lesson_name = next(l['name'] for l in get_lessons(st.session_state.grade, st.session_state.subject) if l['lesson_id'] == st.session_state.lesson)
topic_name = next(t['name'] for t in get_topics(st.session_state.grade, st.session_state.subject, st.session_state.lesson) if t['topic_id'] == st.session_state.topic)

# Title row with Submit button
col_title, col_submit = st.columns([10, 2])

with col_title:
    st.markdown("### Quiz Time!")

with col_submit:
    if st.button("Submit", type="secondary", icon="✅"):
        st.session_state.quiz_submitted = True
        st.rerun()

st.info(f"**{grade_name}** &nbsp;>  **{subject_name}** &nbsp;> **{lesson_name}** &nbsp;> **{topic_name}**")

# If quiz is submitted, show answers
if st.session_state.get("quiz_submitted"):
    st.success("🎉 Quiz submitted successfully!")

    st.write("### Your Answers:")
    for q in questions:
        qid = q['question_id']
        ans = st.session_state.answers.get(qid, ["Not Answered"])
        st.write(f"**Q{qid}:** {ans}")

    st.markdown("---")
    st.page_link("main.py", label="🏠 Back to Home")
    st.stop()

# Display direct question number navigation
# Number of questions per row
buttons_per_row = 10
total_questions = len(questions)

for start in range(0, total_questions, buttons_per_row):
    count_in_row = min(buttons_per_row, total_questions - start)
    cols = st.columns(buttons_per_row)  # always 10 columns for even spacing

    for i in range(buttons_per_row):
        if i < count_in_row:
            q_index = start + i
            button_label = f"⚪ {q_index + 1}"

            # Current question highlight
            if q_index == st.session_state.question_index:
                button_label = f"🔵 {q_index + 1}"
            elif str(questions[q_index]['question_id']) in st.session_state.answers:
                button_label = f"🟢 {q_index + 1}"

            if cols[i].button(button_label, key=f"nav_btn_{q_index}"):
                st.session_state.question_index = q_index
                st.rerun()
        else:
            cols[i].markdown("")  # leave empty to preserve spacing



# Get current question
current_index = st.session_state.question_index
question = questions[current_index]

st.subheader(f"Question {current_index + 1} of {len(questions)}")
st.write(question['question_text'])

if 'image_url' in question and question['image_url']:
    st.image(question['image_url'])

qid = question['question_id']

# Question type handling
if question['question_type'] == 'single_choice':
    options = [opt['option_text'] for opt in question['options']]
    selected = st.radio("Choose one:", options, key=f"q_{qid}")
    st.session_state.answers[qid] = [selected]

elif question['question_type'] == 'multi_choice':
    options = [opt['option_text'] for opt in question['options']]
    selected = st.multiselect("Select one or more:", options, key=f"q_{qid}")
    st.session_state.answers[qid] = selected

elif question['question_type'] == 'text_entry':
    answer = st.text_input("Your answer:", key=f"q_{qid}")
    st.session_state.answers[qid] = [answer]

# Navigation controls
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    if st.button("⬅️ Previous") and current_index > 0:
        st.session_state.question_index -= 1
        st.rerun()

with col3:
    if st.button("Next ➡️") and current_index < len(questions) - 1:
        st.session_state.question_index += 1
        st.rerun()

st.markdown("---")
st.page_link("main.py", label="🏠 Back to Home")