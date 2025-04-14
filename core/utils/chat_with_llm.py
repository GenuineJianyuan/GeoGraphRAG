import  os
from llm_config import LLMConfig
from openai import OpenAI
import  qianfan


def interact_with_llm(prompt, model="deepseek-v3"):  ## qwen-max
    content = None
    if model in LLMConfig.ALI_MODELS:
        client = OpenAI(
            api_key= LLMConfig.ALI_API_KEY,
            base_url= LLMConfig.ALI_BASE_URL
        )   
        completion = client.chat.completions.create(
            model=model,  
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        content = completion.choices[0].message.content
    elif model in LLMConfig.GPT_MODELS:
        client = OpenAI(
            api_key= LLMConfig.GPT_KEY,
        )  

        completion = client.chat.completions.create(
            model=model,
            messages= [
                {"role": "user", "content": prompt}
            ],
        )
        content = completion.choices[0].message.content
    elif model in LLMConfig.LLAMA_MODELS:
        ## 配置千帆环境
        os.environ["QIANFAN_ACCESS_KEY"] = LLMConfig.LLAMA_ACCESS_KEY
        os.environ["QIANFAN_SECRET_KEY"] = LLMConfig.LLAMA_SECRET_KEY
        completion = qianfan.ChatCompletion().do(endpoint= model, 
                                        messages=[{"role":"user","content":prompt}])
        content = completion.body["result"]
    return content
