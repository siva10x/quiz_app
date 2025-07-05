import json
import os

# Define paths to data files
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
METADATA_FILE = os.path.join(DATA_DIR, 'metadata.json')
QUESTIONS_FILE = os.path.join(DATA_DIR, 'questions.json')


def load_metadata():
    """Load metadata.json into a Python list."""
    with open(METADATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_questions():
    """Load questions.json into a Python list."""
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_grades():
    """Return a list of grade names and IDs."""
    metadata = load_metadata()
    return [
        {
            'name': grade['name'],
            'grade_id': grade['grade_id']
        }
        for grade in metadata
    ]

def get_subjects(grade_id):
    """Return subject names and IDs for a given grade."""
    metadata = load_metadata()
    for grade in metadata:
        if grade['grade_id'] == grade_id:
            return [
                {
                    'name': subject['name'],
                    'subject_id': subject['subject_id']
                }
                for subject in grade['subjects']
            ]
    return []


def get_lessons(grade_id, subject_id):
    """Return lesson names and IDs for a given grade and subject."""
    metadata = load_metadata()
    for grade in metadata:
        if grade['grade_id'] == grade_id:
            for subject in grade['subjects']:
                if subject['subject_id'] == subject_id:
                    return [
                        {
                            'name': lesson['name'],
                            'lesson_id': lesson['lesson_id']
                        }
                        for lesson in subject['lessons']
                    ]
    return []


def get_topics(grade_id, subject_id, lesson_id):
    """Return topic names and IDs for a given grade, subject, and lesson."""
    metadata = load_metadata()
    for grade in metadata:
        if grade['grade_id'] == grade_id:
            for subject in grade['subjects']:
                if subject['subject_id'] == subject_id:
                    for lesson in subject['lessons']:
                        if lesson['lesson_id'] == lesson_id:
                            return [
                                {
                                    'name': topic['name'],
                                    'topic_id': topic['topic_id']
                                }
                                for topic in lesson['topics']
                            ]
    return []


def get_questions_by_topic(grade_id, subject_id, lesson_id, topic_id):
    """Return questions filtered by grade, subject, lesson, and topic."""
    questions = load_questions()
    return [
        q for q in questions
        if q['grade_id'] == grade_id
        and q['subject_id'] == subject_id
        and q['lesson_id'] == lesson_id
        and q['topic_id'] == topic_id
    ]


# Optional: Quick test run (when run standalone)
if __name__ == '__main__':
    print("Grades:", json.dumps(get_grades(), indent=4))
    print()
    print("Subjects for Grade 10:", json.dumps(get_subjects('grade_10'), indent=4))
    print()
    print("Lessons for Math in Grade 10:", json.dumps(get_lessons('grade_10', 'math_10'), indent=4))
    print()
    print("Topics for Algebra in Grade 10:", json.dumps(get_topics('grade_10', 'math_10', 'algebra_10'), indent=4))
    print()
    print("Questions for Linear Equations:", json.dumps(get_questions_by_topic('grade_10', 'math_10', 'algebra_10', 'linear_equations_10'), indent=4))
