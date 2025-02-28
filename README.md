# classify_questions_test

Task: Classify each question into domain, subdomain, third-level category and probability

Solution: Using LLM to classify questions (output is results/perplexity_result.json)

Step 1: Processing data, remove noise.

Step 2: Get the processing questions and answers.

Step 3: Define prompt by extract data from pdf, represent it and adding additional definition about domain, subdomain and third-level category.

Step 4: Classify with gpt4o-mini and perplexity sonar.

Step 5: After reviewing, I chose perplexity output because of the way perplexity thinks and makes decisions, which is the right answer.

## Installation

> pip install -r requirements.txt

## Usage

You can try with both ChatGPT-4o-mini and Perplexity Sonar to classify questions

> python src/main.py
