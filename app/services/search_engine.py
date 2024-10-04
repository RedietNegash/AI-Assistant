import json
import requests
import os
from dotenv import load_dotenv
from llm_handler import Gemini

load_dotenv()

def search_and_generate_content(query, num_results):
    


    host_ip = os.getenv("HOST_IP")
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
            # print("Top results:", top_results)

            content_text = [
                f'Content: {res["content"]}\nLink: {res["url"]}' 
                for res in top_results
            ]

            prompt = (
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


            # print("Generated Content from Gemini:")
            # print(generated_content)
            return generated_content
        else:
            print(f"Error: Received status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":  
    num_results = int(os.getenv("NUM_RESULTS", 3))   

    
    query1 = "what is gene?"
    response1 = search_and_generate_content(query1, num_results)

    
    # print("Response to first query:")
    # print(response1)

    
