from langchain_community.agent_toolkits.gmail.toolkit import GmailToolkit 
import streamlit as st 
import os 
from langchain.agents import initialize_agent, AgentType  
from langchain.chat_models import ChatOpenAI
from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials 
import pandas as pd  
import json


st.set_page_config(page_title="Gmail Assistant", page_icon="📩") 
st.title("📩 Gmail Assistant") 
st.subheader("Your Personal Assistant for Gmail")  



credentials_path= "operation_files/credentials.json"   
token_path= "operation_files/token.json"

if os.path.exists(credentials_path):  
    os.remove(credentials_path) 

if os.path.exists(token_path):  
    os.remove(token_path) 



with st.sidebar: 
    st.title("Settings") 
    openai_api_key= st.text_input("Enter your OpenAI API Key", type= "password") 
    credentials_file= st.file_uploader("Upload your Gmail Credentials file", type= ["json"])    
    if credentials_file: 
        st.success("File uploaded Successfully") 
    for i in range(0, 3, 1):  
        st.write(" ") 
    reset= st.button("Clear Session Data")


if credentials_file:  

    os.makedirs("operation_files", exist_ok=True) 
    credentials_data = json.load(credentials_file)

    with open(credentials_path, "w") as file:
        json.dump(credentials_data, file) 

    credentials= get_gmail_credentials( 
        token_file= "token.json",
        scopes= ["https://mail.google.com/"], 
        client_secrets_file= credentials_path
    ) 

    api_resource= build_resource_service(credentials= credentials)  
    toolkit= GmailToolkit(api_resource= api_resource)   
    gmail_tool= toolkit.get_tools()  

    if openai_api_key:
        llm= ChatOpenAI(model= "gpt-4o-mini", api_key= openai_api_key)

    agent= initialize_agent(gmail_tool, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION) 




if "messages" not in st.session_state or reset: 
    st.session_state.messages=[{"role": "assistant", "content": "Hi, I am your Gmail Assistant. How can I help you?"}]  
    st.session_state.data=[]

if "data" not in st.session_state: 
    st.session_state.data=[]

for msg in st.session_state.messages: 
    st.chat_message(msg["role"]).write(msg["content"]) 




query= st.chat_input(placeholder="What would you like me to do?")

if query: 
    st.session_state.messages.append({"role": "user", "content": query})  
    st.chat_message("user").write(st.session_state.messages[-1]["content"])  

    response= agent.invoke(query) 
    st.session_state.messages.append({"role": "assistant", "content": response["output"]}) 
    st.chat_message("assistant").write(st.session_state.messages[-1]["content"])  
    st.session_state.data.append([query, response["output"]])



if st.button("Show Message History"): 
    df= pd.DataFrame(st.session_state["data"], columns=["Query", "Response"]) 
    st.write(df)

















