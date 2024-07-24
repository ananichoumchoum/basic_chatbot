# Imports
from colorama import Fore
import os
import streamlit as st
from streamlit import session_state as state

# Langchain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# Establish Client connection; could provide additional parameters (Temp, Penalties, etc)
model = "gpt-4.0-mini"
client = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", default=None), 
    temperature=1.5, 
    model=model
)

# Store Chat History
if "chat_history" not in state:
    state.chat_history = InMemoryChatMessageHistory()

def get_openai_response(input):
    system_prompt = (
        "You are a helpful assistant. If you know the user's name, use it in your response."
    )
    
    qa_prompt = ChatPromptTemplate.from_messages([
        {"role": "system", "content": system_prompt},
        MessagesPlaceholder("chat_history"),
        {"role": "user", "content": "{input}"}
    ])
    
    chain = qa_prompt | client
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: state.chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    
    return chain_with_history.invoke({"input": input})

# Regurgitate Chat History
for msg in state.chat_history.messages:
    st.chat_message(msg.type).write(msg.content)

user_input = st.chat_input("Ask your question here...")
if user_input:
    st.chat_message("user").write(user_input)
    response = get_openai_response(user_input)
    st.chat_message("ai").write(response.content)

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
        print(f"\n{Fore.BLACK}Bot: {response.content}\n")

if __name__ == "__main__":
    main()
