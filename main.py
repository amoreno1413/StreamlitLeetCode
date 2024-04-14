import os
import streamlit as st
from openai import OpenAI

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](" \
    "https://codespaces.new/streamlit/llm-examples?quickstart=1) "

st.title("LeetCode CoPilot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Please provide the LC question and your code!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "system", "content": "You are a coding assisstant Using the code "
                                                                   "provided by the user, "
                                      "you will generate the next line of code needed that will guide the user to"
                                      " the solution. You are not to give the user the entire solution, but "
                                      "rather a single line of code that, when added to the current code, will help "
                                                                   "the "
                                      " user reach the correct solution. Whenever possible, you are to use the top "
                                      " solution from leetcode. Whenever you give the user a line of code, you are to"
                                      "explain why that line of code will help the user, as well as provide a hint to "
                                                                   "the "
                                      " next line of code that the user will need, but do not provide that line. If the"
                                      "user replies with 'next' you will repeat the actions above. If no code is "
                                                                   "provided, "
                                      "you are to remind the user to provide their code. If only the question is "
                                                                   "provided, "
                                      "you will give the user a single line of code to start them off, as well as why "
                                                                   "that "
                                      " line is necessary, and a hint as to what to do next. Remember, you are never to"
                                      " the entire correct solution, only give them the correct solution line by line."
                                      })
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)