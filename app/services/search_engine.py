import requests
import os
from dotenv import load_dotenv
from llm_handler import Gemini  


load_dotenv()

def search_and_generate_content(query, num_results):
    host_ip = "127.0.0.1"
    host_ip=os.getenv("HOST_IP")
    port=os.getenv("PORT")
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
                f"based on the user query {query}"
                "You have been provided with content extracted from various sources based on a user query."
                f"results from the sources {content_text}" 
                "Your task is to summarize the key insights and information from the provided content while ensuring that all relevant links " 
                "to the sources are included. Follow these steps:\n" 
                "1. Identify the main topics and insights from the content of each source.\n" 
                "2. Provide a concise summary that captures the essential information.\n" 
                "3. Return the information in a structured format as follows:\n" 
                "4. Include a note for further reading at the end of your response, with a direct link to the original source of the content between the summery and the link of each responses.\n" 
                "5. make sure you return the summary in one json format as follows if you only found responses exactly matching the user query otherwise just reutn NA"
                "[\n" 
                "    {\n" 
                '        "summary": "Concise summary of key insights",\n' 
                '        "For further reading, visit "URL of the source\n"",\n' 
                "    },\n" 
                "    ...\n" 
                "]\n" 
                "Make sure the summary is clear, informative, and relevant to the user’s query." 
                "if you couldn't find anything exactly related to the user query only return NA  and don't include summery and link."
)

           
            content_text = [
                f'Content: {res["content"]}\nLink: {res["url"]}' 
                for res in top_results
            ]

            gemini = Gemini()
            # generated_content = gemini(prompt, "\n\n".join(content_text))  
            generated_content = gemini(prompt)  


            
            print("Generated Content from Gemini:")
            print(generated_content)
        else:
            print(f"Error: Received status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":  
    num_results = int(os.getenv("NUM_RESULTS", 3))   

    query = "What enhancers are involved in the formation of the protein p78504? "
    search_and_generate_content(query, num_results)