class LLMConfig:
    """
    Configuration class for LLM settings.
    """
    ALI_MODELS = ["deepseek-v3", "qwen-max", "deepseek-r1-distill-qwen-32b",  "deepseek-r1-distill-llama-70b"]
    ALI_API_KEY = "your-api-key-here"  
    ALI_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    GPT_MODELS = ["gpt-4o", "gpt-3.5-turbo"]
    GPT_KEY = "your-api-key-here"
    LLAMA_MODELS = ["Meta-Llama-3-70B"]
    LLAMA_ACCESS_KEY = "your-api-key-here" ## Use qianfan platform for Llama 
    LLAMA_SECRET_KEY = "your-api-key-here" ## Use qianfan platform for Llama 
