import os
from colorama import Fore
import chatbot.open_ai as open_ai

# Set the API Key
openai_api_key = os.environ.get("OPENAI_API_KEY", default=None)

# Establish client connection; could provide additional parameters (Temp, Penalties, etc)
client = open_ai.OpenAI(api_key=openai_api_key)

def get_openai_response(input):
    # Interact with LLM
    system_prompt = (
        "You are a helpful assistant. If you know the user's name, use it in your response."
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # LLM Model
        messages=[
            {"role": "system", "content": system_prompt},  # Prompting
            {"role": "user", "content": input},  # User Input
        ],
    )
    
    message = response.choices[0].message.content  # Extract Response
    return message

def main():
    """Main"""
    print("Type 'exit' to end the conversation.")
    ## Chat Bot Loop: take input, print response
    while True:
        user_input = input(f"{Fore.BLUE}You: ")
        if user_input.lower() in ["bye", "exit"]:
            print("Bot: Goodbye! Have a great day!")
            break
        response = get_openai_response(user_input)
        print(f"\n{Fore.BLACK}Bot: {response}\n")

if __name__ == "__main__":
    main()
