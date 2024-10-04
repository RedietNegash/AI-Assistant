import time
import json
from llm_handler import Gemini  

class Cache:
    def __init__(self, expiration_time=3600):
        self.cache = {}
        self.expiration_time = expiration_time

    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.expiration_time:
                return value
            else:
                del self.cache[key]  
        return None

    def set(self, key, value):
        self.cache[key] = (value, time.time())

class CachedGemini:
    def __init__(self, history_file='conversation_history.json'):
        self.gemini = Gemini()  
        self.cache = Cache()  
        self.history_file = history_file
        self.conversation_history = self.load_history()

    def load_history(self):
        try:
            with open(self.history_file, 'r') as file:
                history = json.load(file)
                return [entry for entry in history if isinstance(entry, dict) and 'role' in entry and 'content' in entry]
        except (FileNotFoundError, json.JSONDecodeError):
            return []  
    
    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.conversation_history, file)

    def __call__(self, user_input: str):
     
        self.conversation_history.append({"role": "user", "content": user_input})
        
       
        context = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.conversation_history])
        cached_result = self.cache.get(context)
        if cached_result:
            print("Returning cached result.")
            return cached_result

     
        try:
            result = self.gemini(context)  
        except Exception as e:
            print("Error calling Gemini API:", e)
            return None 

        
        self.cache.set(context, result)
        self.conversation_history.append({"role": "assistant", "content": result})
        self.save_history()

        return result
# Example usage
if __name__ == "__main__":
    cached_gemini = CachedGemini()

    # response_1 = cached_gemini("my name is boo")
    # print("First Response:", response_1)

    # response_2 = cached_gemini("what is my name?")
    # print("Second Response:", response_2)

    # response_3 = cached_gemini("what is protein.")
    # print("Third Response:", response_3)
 
    # response_4 = cached_gemini("could you tell me a bit more?")
    # print("Fourth Response:", response_4)

