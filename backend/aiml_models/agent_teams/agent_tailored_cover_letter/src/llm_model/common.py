from llm_agents import LLM_model
from backend.services.service_cover_letter.src.config.config_low_level import GPT_API

def get_llm_model():
    llm_instance = LLM_model.LLMModel(openai_api_key=GPT_API, temperature=0.1)
    return llm_instance.get_llm_model()