import streamlit as st

st.set_page_config(page_title="MistakeSense", layout="centered")

st.title("MistakeSense ")
st.write("Learn *why* you got something wrong, not just what is wrong.")

question = st.text_area(" Question")
student_answer = st.text_area("Your Answer")
correct_answer = st.text_area(" Correct Answer")

def classify_mistake(student, correct):
    if student.strip() == "":
        return "Incomplete Answer", "You didn’t complete the solution."

    if student == correct:
        return "No Mistake", "Your answer is correct."

    if any(op in student for op in ["+", "-", "*", "/"]) and any(op in correct for op in ["+", "-", "*", "/"]):
        return "Calculation Error", "Your method seems correct, but there may be an arithmetic mistake."

    if len(student) < len(correct) / 2:
        return "Incomplete Reasoning", "Your answer lacks sufficient steps or explanation."

    return "Conceptual Error", "There may be a misunderstanding of the underlying concept."

if st.button("🔍 Analyze Mistake"):
    category, explanation = classify_mistake(student_answer, correct_answer)

    st.subheader(" Analysis Result")
    st.write(f"**Mistake Type:** {category}")
    st.write(f"**Explanation:** {explanation}")

    st.subheader(" What to do next")
    if category == "Calculation Error":
        st.write("Practice step-by-step calculations and double-check arithmetic.")
    elif category == "Conceptual Error":
        st.write("Revise the core concept and try similar conceptual questions.")
    elif category == "Incomplete Answer":
        st.write("Focus on writing complete solutions with all steps.")
    else:
        st.write("Keep practicing. You are doing gooa.")
