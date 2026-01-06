import streamlit as st
import re
from openai import OpenAI

st.set_page_config(page_title="Smart Math Reasoning Tutor", layout="centered")

client = OpenAI(
    api_key="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" 
)

st.title("Smart Math Reasoning Tutor")
st.write(
    "This app analyzes a student's math solution, detects logical mistakes, "
    "and explains the correct reasoning step-by-step."
)

st.divider()
question = st.text_input(
    "Enter the math question"
    placeholder="Example: Find 20% of 150"
)

student_solution = st.text_area(
    " Enter the student's solution",
    placeholder="Example: 20% × 150 = 20 × 150 = 3000"
)

analyze_btn = st.button(" Analyze Solution")

def detect_percentage_mistake(question, solution):
    """
    Rule-based logic to detect common percentage mistakes
    """
    solution_clean = solution.lower()

    # Case 1: Percentage not converted to fraction
    if "%" in solution_clean and re.search(r"\b\d+\s*[×x*]\s*\d+", solution_clean):
        return "Percentage not converted to fraction"

    # Case 2: Wrong base value assumption
    if "of" in question.lower() and "%" in question.lower():
        if "/" not in solution_clean and "100" not in solution_clean:
            return "Incorrect base value used for percentage"

    # Case 3: Looks correct but calculation error
    if "%" in solution_clean and ("0." in solution_clean or "/100" in solution_clean):
        return "Calculation error after correct setup"

    return "Unclear or mixed reasoning error"


def get_ai_explanation(mistake_type, question, student_solution):
    prompt = f"""
A student is solving a math percentage problem.

Question:
{question}

Student's solution:
{student_solution}

Detected mistake type:
{mistake_type}

Explain clearly:
1. Where the student's reasoning went wrong
2. Why it is incorrect
3. The correct approach
4. One short tip to avoid this mistake in the future

Keep the explanation simple and educational.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful math tutor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

if analyze_btn:
    if not question or not student_solution:
        st.warning("Please enter both the question and the student's solution.")
    else:
        mistake_type = detect_percentage_mistake(question, student_solution)

        st.subheader(" Detected Issue")
        st.error(mistake_type)

        with st.spinner("Thinking like a tutor..."):
            explanation = get_ai_explanation(
                mistake_type,
                question,
                student_solution
            )

        st.subheader("📘 Explanation & Correct Reasoning")
        st.write(explanation)

        st.success("Analysis complete ")


st.divider()
st.caption(
    "Built for an education-focused hackathon. "
    "Logic-driven analysis + AI-assisted explanations."
)

