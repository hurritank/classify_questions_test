import os
import requests
from typing import Any
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatPerplexity
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from enums import LLMModelName, APIURL


class LLMModel:
    def __init__(self, model_name: LLMModelName, temperature=0.1):
        self.model_name = model_name

        if model_name is LLMModelName.openai_4o_mini:
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        elif model_name is LLMModelName.perplexity_sonar:
            self.llm = ChatPerplexity(
                model_name=model_name,
                temperature=temperature,
                pplx_api_key=os.getenv("PERPLEXITY_API_KEY"),
            )
        # elif model_name is LLMModelName.perplexity_sonar:
        #     self.llm = ChatOpenAI(
        #         model=model_name,
        #         temperature=temperature,
        #         api_key=os.getenv("PERPLEXITY_API_KEY"),
        #         base_url="https://api.perplexity.ai",
        #     )
        else:
            raise ValueError(f"Invalid model name: {model_name}")

    def parse_response(self, response: AIMessage):
        model_name = self.model_name.value
        if self.model_name is LLMModelName.openai_4o_mini:
            return {
                "content": response.content,
                "input_tokens": response.response_metadata["token_usage"][
                    "prompt_tokens"
                ],
                "output_tokens": response.response_metadata["token_usage"][
                    "completion_tokens"
                ],
                "model_name": model_name,
            }
        elif self.model_name is LLMModelName.perplexity_sonar:
            return {
                "content": response.content,
                "model_name": model_name,
            }
        else:
            raise ValueError(f"Invalid model name: {model_name}")

    def complete(self, human_message=None, system_message=None, output_format=None):
        messages = []
        self.llm.model_kwargs = {}
        if human_message:
            messages.append(HumanMessage(content=human_message))
        if system_message:
            messages.append(SystemMessage(content=system_message))
        if output_format:
            self.llm.model_kwargs = {"response_format": output_format}
        if not messages:
            raise ValueError("No prompt send to LLM")
        try:
            response = self.llm.invoke(messages)
            return self.parse_response(response)
        except Exception as e:
            self.llm.model_kwargs = {}
            print(f"Error invoking model: {e}")
            raise e

    async def acomplete(
        self, human_message=None, system_message=None, output_format=None
    ):
        messages = []
        self.llm.model_kwargs = {}
        if human_message:
            messages.append(HumanMessage(content=human_message))
        if system_message:
            messages.append(SystemMessage(content=system_message))
        if output_format:
            self.llm.model_kwargs = {"response_format": output_format}
        if not messages:
            raise ValueError("No prompt send to LLM")
        try:
            response = await self.llm.ainvoke(messages)
            return self.parse_response(response)
        except Exception as e:
            self.llm.model_kwargs = {}
            print(f"Error invoking model: {e}")
            raise e


def perplexity_chat_completions(
    human_mess: str,
    model_name: str,
    temperature: int = 0,
    sys_mess: str | None = None,
    output_format: Any | None = None,
) -> Any:
    if not human_mess:
        raise ValueError("Need human message")

    messages = []
    if sys_mess:
        sys_content = {"role": "system", "content": sys_mess}
        messages.append(sys_content)
    human_content = {"role": "user", "content": human_mess}
    messages.append(human_content)

    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature,
    }
    if output_format:
        response_format = {
            "type": "json_schema",
            "json_schema": {"schema": output_format.model_json_schema()},
        }
        payload["response_format"] = response_format
    api_key = os.getenv("PERPLEXITY_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.request(
        "POST", APIURL.perplexity.value, json=payload, headers=headers
    )
    if response.status_code == 200:
        return response
    elif response.status_code == 401:
        raise PermissionError("Authentication failed. Check your API key.")
    elif response.status_code == 400:
        raise ValueError("Bad Request. Check your payload.")
    elif response.status_code == 404:
        raise ValueError("Resource not found.")
    elif response.status_code == 500:
        raise RuntimeError("Server Error. Please try again later.")
    else:
        # For any other status code, raise an HTTPError
        raise requests.HTTPError(f"Unexpected status code: {response.status}")
