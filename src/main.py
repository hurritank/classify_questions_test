import json
import time
from pydantic import BaseModel, Field

from utility import extract_questions_and_correct_answers, extract_json_from_string
from prompts import (
    prompt,
    definition_data,
    definition_data_v2,
    perplexity_return_prompt,
)
from llms import LLMModel, perplexity_chat_completions
from enums import LLMModelName


class CategoryOutput(BaseModel):
    id: int = Field(description="The ID of question")
    domain: str = Field(description="The domain classify")
    subdomain: str = Field(description="The subdomain classify")
    third_level_category: str = Field(description="The third-level category classify")
    probability: float


FILE_PATH = (
    "/Users/jin/Desktop/classify_questions_test/Exam tagging sample questions.xlsx"
)
CHATGPT_OUTPUT_PATH_V1 = "results/chatgpt_result.json"
CHATGPT_OUTPUT_PATH_V2 = "results/chatgpt_result_v2.json"
PERPLEXITY_OUTPUT_PATH = "results/perplexity_result.json"

# Processing and get question and answer pairs
question_answer_pairs = extract_questions_and_correct_answers(FILE_PATH)

# Run with openai
model = LLMModel(LLMModelName.openai_4o_mini)
final_response = []
for i, item in enumerate(question_answer_pairs):
    final_prompt = prompt.format(
        definition_data=definition_data_v2,
        question_id=str(i + 1),
        question=item["processed_question"],
        answer=item["correct_answer"],
    )
    response = model.complete(system_message=final_prompt, output_format=CategoryOutput)

    # Validate response
    validate_response = CategoryOutput.model_validate_json(response["content"])
    final_response.append(validate_response.model_dump_json())
    time.sleep(10)

# Write the list to a JSON file
with open(CHATGPT_OUTPUT_PATH_V2, "w") as json_file:
    json.dump(final_response, json_file, indent=4)

# Run with perplexity
final_response = []
for i, item in enumerate(question_answer_pairs):
    final_prompt = prompt.format(
        definition_data=definition_data_v2,
        question_id=str(i + 1),
        question=item["processed_question"],
        answer=item["correct_answer"],
    )
    response = perplexity_chat_completions(
        human_mess=final_prompt + perplexity_return_prompt,
        model_name=LLMModelName.perplexity_sonar,
        output_format=CategoryOutput,
    )
    json_ressponse = json.loads(response.text)
    extract_json_response = extract_json_from_string(
        json_ressponse["choices"][0]["message"]["content"]
    )
    output = json.loads(extract_json_response)
    final_response.append(output)
    time.sleep(10)

# Write the list to a JSON file
with open(PERPLEXITY_OUTPUT_PATH, "w") as json_file:
    json.dump(final_response, json_file, indent=4)
