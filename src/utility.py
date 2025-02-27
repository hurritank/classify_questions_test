import re
import pandas as pd


def processing_question(question: str) -> str:
    """Processes a question string to remove noise."""
    # 1. Remove HTML tags
    question = re.sub(r"<[^>]+>", "", question)

    # 2. Replace HTML entities
    question = question.replace("&nbsp;", " ")
    question = question.replace("&deg;", "°")
    question = question.replace("&mu;", "μ")
    question = question.replace("&lt;", "<")
    question = question.replace("&gt;", ">")

    # 3. Remove subscript/superscript HTML (crude but effective for this data)
    question = re.sub(r"<sub>.*?</sub>", "", question)
    question = re.sub(r"<sup>.*?</sup>", "", question)

    # 4. Lowercase
    question = question.lower()

    # 5. Remove punctuation and special characters
    question = re.sub(
        r"[^\w\s°μ<>]", "", question
    )  # Keep degree and micro symbols, less and greater than

    # 6. Remove extra whitespace
    question = " ".join(question.split())

    return question


def extract_questions_and_correct_answers(excel_file: str) -> list[dict]:
    """
    Extracts the processed question and the text of the correct answer from an Excel file.

    Args:
        excel_file (str): The path to the Excel file.

    Returns:
        list: A list of dictionaries, where each dictionary contains the processed question and its correct answer.
              Returns an empty list if the file is not found or if there's an error.
    """
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"Error: The file '{excel_file}' was not found.")
        return []

    if "Question" not in df.columns or "Correct Answer" not in df.columns:
        print(
            "Error: The Excel file must have 'Question' and 'Correct Answer' columns."
        )
        return []

    qa_list = []
    for index, row in df.iterrows():
        question = row["Question"]
        correct_answer_num = row["Correct Answer"]

        # Process the question
        processed_question = processing_question(question)

        # Determine the correct answer column based on the 'Correct Answer' value
        if correct_answer_num == 1:
            correct_answer_column = "Answer 1"
        elif correct_answer_num == 2:
            correct_answer_column = "Answer 2"
        elif correct_answer_num == 3:
            correct_answer_column = "Answer 3"
        elif correct_answer_num == 4:
            correct_answer_column = "Answer 4"
        else:
            print("Warning: Invalid 'Correct Answer' value")
            continue

        # Extract the correct answer text
        if correct_answer_column in df.columns:
            correct_answer_text = row[correct_answer_column].lower()
        else:
            print(
                f"Warning: Column '{correct_answer_column}' not found in row {index + 2}. Skipping."
            )
            continue

        qa_list.append(
            {
                "processed_question": processed_question,
                "correct_answer": correct_answer_text,
            }
        )

    return qa_list


def extract_json_from_string(text):
    # Find the JSON part of the string
    json_pattern = r"\{.*?\}"
    match = re.search(json_pattern, text, re.DOTALL)

    if match:
        json_string = match.group()
        return json_string
    else:
        print("No JSON block found in the text.")
        return text
