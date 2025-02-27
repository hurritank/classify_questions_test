from enum import Enum


class LLMModelName(str, Enum):
    openai_4o_mini = "gpt-4o-mini"
    perplexity_sonar = "sonar"


class APIURL(str, Enum):
    perplexity = "https://api.perplexity.ai/chat/completions"
