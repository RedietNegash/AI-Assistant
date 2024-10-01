import json
import requests
import os
from dotenv import load_dotenv
from llm_handler import Gemini

load_dotenv()


def load_cache(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_cache(file_path, cache):
    with open(file_path, 'w') as f:
        json.dump(cache, f)


cache_file_path = 'cache.json'
cache = load_cache(cache_file_path)

def search_and_generate_content(query, num_results):
    
    if query in cache:
        print("Fetching from cache...")
        return cache[query]

    host_ip = os.getenv("HOST_IP", "127.0.0.1")
    port = os.getenv("PORT")
    url = f"http://{host_ip}:{port}/search"
    params = {
        "format": "json",
        "q": query
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.json()
            top_results = sorted(result['results'], key=lambda x: x['score'], reverse=True)[:num_results]
            print("Top results:", top_results)

            content_text = [
                f'Content: {res["content"]}\nLink: {res["url"]}' 
                for res in top_results
            ]

            prompt = (
                f"You are provided with the following user history: {json.dumps(cache, indent=2)}.\n"
                f"Current user query: '{query}'\n\n"
                
                "Instructions:\n"
                "1. If the current query is seeking more clarification on a previous response (e.g., if the query is a follow-up to a previous query), refer to the latest entry in the user history (which is found at the end of the history).\n"
                "   - Check the last user query and response from the history and respond accordingly, using the most relevant past information.\n"
                "   - If more details are needed, clarify or elaborate on the last response found in the history.\n\n"
                
                "2. If the current query is unrelated to the user history, proceed with the following:\n"
                "   You have been provided with content extracted from various sources based on the user query.\n"
                f"   Results from the sources:\n{content_text}\n"
                
                "   Your task is to summarize the key insights and information from the provided content while ensuring that all relevant links to the sources are included.\n"
                "   Follow these steps:\n"
                "   1. Identify the main topics and insights from the content of each source.\n"
                "   2. Provide a concise summary that captures the essential information.\n"
                "   3. Return the summary in the following structured JSON format:\n"
                "   [\n"
                '       {"summary": "Concise summary of key insights", "for_further_reading": "URL of the source"},\n'
                "       ...\n"
                "   ]\n\n"
                
                "   If you couldn't find anything exactly related to the user query, return 'NA' and do not include a summary or links."
            )




            gemini = Gemini()
            generated_content = gemini(prompt)

            
            cache[query] = generated_content
            save_cache(cache_file_path, cache)  

            print("Generated Content from Gemini:")
            print(generated_content)
            return generated_content
        else:
            print(f"Error: Received status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":  
    num_results = int(os.getenv("NUM_RESULTS", 3))   

    
    #query1 = "more clarification on a previous response"
    query1 = "what is gene?"
    response1 = search_and_generate_content(query1, num_results)

    
    print("Response to first query:")
    print(response1)

    
   import random
import timeit

def sum_digits(numbers):
    if numbers not in sum_digits.my_cache:
        sum_digits.my_cache[numbers] = sum(
            int(digit) for number in numbers for digit in str(number)
        )
    return sum_digits.my_cache[numbers]
sum_digits.my_cache = {}

numbers = tuple(random.randint(1, 1000) for _ in range(1_000_000))

print(
    timeit.timeit(
        "sum_digits(numbers)",
        globals=globals(),
        number=1
    )
)

print(
    timeit.timeit(
        "sum_digits(numbers)",
        globals=globals(),
        number=1
    )
)

