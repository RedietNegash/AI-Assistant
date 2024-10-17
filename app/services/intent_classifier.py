import os

from dotenv import load_dotenv
from llm_models import GeminiModel, LLMInterface, OpenAIModel

load_dotenv()

class IntentClassifier:
    def __init__(self, model: 'LLMInterface'):
        self.model = model

    def classify_intent(self, query: str) -> str:
        prompt = self.build_prompt(query)
        response = self.model.generate(prompt)


        intent = response.get('Detected Intent') if isinstance(response, dict) else response
        return intent

    def build_prompt(self, query: str) -> str:
        few_shot_examples = """
        🤖 System Prompt:
        You’re a LLM that detects intent from user queries. Your task is to classify the user's intent based on their query. 
        Below are the possible intents with brief descriptions. Use these to accurately determine the user's goal, and output only the intent topic.

        - Summary: The user is asking for a summary of content.
        - Graph: The user is asking for information related to graph data.

        💬 User Query:
        Show me all the nodes connected to this gene in the graph.
        🤖 Detected Intent: Graph

        💬 User Query:
        Can you provide a summary of the latest research paper on AI?
        🤖 Detected Intent: Summary

        💬 User Query:
        I need a breakdown of the key points from yesterday's meeting.
        🤖 Detected Intent: Summary
        """
        
       
        return f"{few_shot_examples}\n\n💬 User Query:\n{query}"

if __name__ == "__main__":
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    print("GEMINI_API_KEY:", gemini_api_key)
    # openai_api_key = os.getenv("OPENAI_API_KEY")

    
    model = GeminiModel(gemini_api_key)
   

    classifier = IntentClassifier(model)

 
    queries = [
        "Can you provide a summary of the latest research paper on AI?",
        "Show me all the nodes connected to this gene in the graph.",
        "I need a breakdown of the key points from yesterday's meeting.",
        "What are the connections between the nodes starting from ensg00000289505?"
    ]

    for query in queries:
        intent = classifier.classify_intent(query)
        print(f"Query: {query}")
        print(f"Detected Intent: {intent}\n")
