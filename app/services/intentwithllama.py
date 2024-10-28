import os
from llm_models import GeminiModel,OpenAIModel
from dotenv import load_dotenv
# from llama_index.llms.openai import OpenAI

load_dotenv()

from llama_index.core import Settings

GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY')
GeminiModel(api_key=GEMINI_API_KEY)

direct_llm_prompt = (
    "Given the user query, respond as best as possible following this guidelines:\n"
    "- If the intent of the user is to get information about the general questions about rejuve-bio, respond with: "
    "This assistant can answer questions, generate text, summarize documents, and more. \n"
    "- If the intent of the user is harmful. Respond with: I cannot help with that. \n"
    "- If the intent of the user is to get information outside of the context given, respond with: "
    "I cannot help with that. Please ask something that is relevant with the documents in the context givem. \n"
    "Query: {query}"
)





from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.tools import QueryEngineTool


class LlmQueryEngine(CustomQueryEngine):
    """custom query engine for direct calls to the LLM model."""
    llm:GeminiModel
    prompt:str

    def custom_query(self, query_str:str):
        llm_prompt = self.prompt.format(query=query_str)
        llm_response = self.llm.complete(llm_prompt)
        return str(llm_response)


llm_query_engine = LlmQueryEngine(
    llm=GeminiModel, prompt=direct_llm_prompt
)

llm_tool = QueryEngineTool.from_defaults(
    query_engine=llm_query_engine,
    name="llm_query_tool",
    description=(
        "Useful for when the INTENT of the user about rejuve-bio "
        "or when the user is asking general questions related to rejuve-bio"       
    ),
)

grpah_tool=QueryEngineTool.from_defaults(
    query_engine=llm_query_engine,
    name="graph_query_tool",
    description=(
        "Useful for when the INTENT of the user is to rerive graph"
        "retrives graph based on the user query"
    ),
)

 
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.query_engine import RouterQueryEngine

router_query_engine=RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        llm_tool,
        grpah_tool,
    ]
)

from IPython.display import display, HTML

query = (
    "In the essay, the author mentions his early experiences with programming. "
    "Describe the first computer he used for programming, the language he used, "
    "and the challenges he faced."
)
response = router_query_engine.query(query)

display(HTML(f'<p style="font-size:16px">{response.response}</p>'))

