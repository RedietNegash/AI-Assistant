import os
import time
import json
from dotenv import load_dotenv


load_dotenv() 

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

class ContextualCache:
    def __init__(self, history_file='conversation_history.json'):
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
        print("starting cache process from the cached gmenini")
        self.conversation_history.append({"role": "user", "content": user_input})
        context = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.conversation_history])

        cached_result = self.cache.get(context)
        if cached_result:
            print("Returning cached result.")
            return cached_result
        else:
            return context
    def store_result(self,result, context):
        # Cache the result
        self.cache.set(context, result)
        self.conversation_history.append({"role": "assistant", "content": result})
        self.save_history()

        return result
