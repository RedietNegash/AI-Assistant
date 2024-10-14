class ConversationCache:
    def __init__(self):
        self.cache = {}

    def add_conversation(self, user_id, session_id, message):
        if user_id not in self.cache:
            self.cache[user_id] = {}
        if session_id not in self.cache[user_id]:
            self.cache[user_id][session_id] = {
                "assistant": []
            }
        self.cache[user_id][session_id]["assistant"].append(message)

    def get_conversation(self, user_id, session_id):
        if user_id in self.cache and session_id in self.cache[user_id]:
            return self.cache[user_id][session_id]["assistant"]
        return None

    def clear_user_session(self, user_id, session_id):
        if user_id in self.cache and session_id in self.cache[user_id]:
            del self.cache[user_id][session_id]
        if user_id in self.cache and not self.cache[user_id]:
            del self.cache[user_id]
