from ast import Lambda
import os
from random import seed
import autogen
from autogen import AssistantAgent, UserProxyAgent
# from llm_models import GeminiModel,OpenAIModel
from dotenv import load_dotenv
from autogen.code_utils import DEFAULT_MODEL, UNKNOWN, content_str, execute_code, extract_code, infer_lang
from flask import current_app

from llm_models import GeminiModel, OpenAIModel
from summarizer import Graph_Summarizer


# load_dotenv()

# from random import seed as random_seed
# random_seed(42)  


# llm_config = {"model": "gemini-pro", "api_key": os.environ.get("GEMINI_API_KEY")}
# config_list_gemini = autogen.config_list_from_json(
#     "OAI_CONFIG_LIST",
#     filter_dict={
#         "model": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-pro-001"],
#     },
# )

# # Start the chat
# assistant = AssistantAgent(
#     "assistant", 
#     llm_config={"config_list": config_list_gemini},
#     max_consecutive_auto_reply=5
# )

# user_proxy = UserProxyAgent(
#     "user_proxy",
#     code_execution_config={"work_dir": "coding", "use_docker": False},
#     human_input_mode="NEVER",
#     is_termination_msg=lambda x: content_str(x.get("content")).find("TERMINATE") >= 0,
# )

# result = user_proxy.initiate_chat(assistant, message="Sort the array with Bubble Sort: [4, 1, 5, 2, 3]")


import os

from autogen import ConversableAgent

# agent = ConversableAgent(
#     "chatbot",
#     llm_config={"config_list": config_list_gemini},
#     code_execution_config=False,  
#     function_map=None,  
#     human_input_mode="NEVER",  
# )

# reply = agent.generate_reply(messages=[{"content": "Tell me a joke.", "role": "user"}])
# print(reply)

# cathy = ConversableAgent(
#     "cathy",
#     system_message="Your name is Cathy and you are a part of a duo of comedians.",
#     llm_config={"config_list": config_list_gemini},
#     human_input_mode="NEVER",
    
#     is_termination_msg=lambda msg: "good bye" in msg["content"].lower(),
# )
# joe = ConversableAgent(
#     "joe",
#     system_message="Your name is Joe and you are a part of a duo of comedians.",
#      llm_config={"config_list": config_list_gemini},
#     human_input_mode="NEVER", 
    
# )

# result = joe.initiate_chat(cathy, message="Cathy, tell me a joke and then say the words GOOD BYE.")


# agent_with_number = ConversableAgent(
#     "agent_with_number",
#     system_message="You are playing a game of guess-my-number. "
#     "In the first game, you have the "
#     "number 53 in your mind, and I will try to guess it. "
#     "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
#     llm_config={"config_list": config_list_gemini},
#     max_consecutive_auto_reply=1,  
#     is_termination_msg=lambda msg: "53" in msg["content"],  
    
# )

# # agent_guess_number = ConversableAgent(
# #     "agent_guess_number",
# #     system_message="I have a number in my mind, and you will try to guess it. "
# #     "If I say 'too high', you should guess a lower number. If I say 'too low', "
# #     "you should guess a higher number. ",
# #     llm_config={"config_list": config_list_gemini},
# #     human_input_mode="NEVER",
# # )

# # result = agent_with_number.initiate_chat(
# #     agent_guess_number,
# #     message="I have a number between 1 and 100. Guess it!",
# # )

# human_proxy=ConversableAgent(
#     "human_proxy",
#     llm_config=False,
#     human_input_mode='ALWAYS'
# )

# result=human_proxy.initiate_chat(
#     agent_with_number,
#     message="10"
# )

def get_llm_model(config):
    model_type = config['llm_model']

    if model_type == 'openai':
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            raise ValueError("OpenAI API key not found")
        return OpenAIModel(openai_api_key)
    elif model_type == 'gemini':
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise ValueError("Gemini API key not found")
        return GeminiModel(gemini_api_key)
    else:
        raise ValueError("Invalid model type in configuration")
from typing import Annotated, Literal

# Operator = Literal["+", "-", "*", "/"]


# def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
#     if operator == "+":
#         return a + b
#     # elif operator == "-":
#     #     return a - b
#     # elif operator == "*":
#     #     return a * b
#     # elif operator == "/":
#     #     return int(a / b)
#     else:
#         raise ValueError("Invalid operator")
    

load_dotenv()

from random import seed as random_seed
random_seed(42)  


llm_config = {"model": "gemini-pro", "api_key": os.environ.get("GEMINI_API_KEY")}
config_list_gemini = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-pro-001"],
    },
)

assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with summerizing graph."
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": config_list_gemini},
)

user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

from autogen import register_function
summary = Graph_Summarizer(llm_config)

register_function(
    summary.open_ai_summarizer(),
    caller=assistant, 
    executor=user_proxy,
    description="graph summarizer", 
)

chat_result = user_proxy.initiate_chat(assistant)

# config = current_app.config
# llm = get_llm_model(config)
# summary = Graph_Summarizer()


# assistant.register_for_llm(name="summarizer", description="graph summarizer")(summary.open_ai_summarizer)
# assistant.llm_config["tools"]

# user_proxy.register_for_execution(name="summarizer")(summary.open_ai_summarizer)
# chat_result = user_proxy.initiate_chat(assistant, 
# message="summerize this graph")


# assistant.llm_config["tools"]
