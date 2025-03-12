import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub

# Define prompt
template = f"""
You are a helpful assistant programmed to identify funding resources for startups with any given business model. 

Your output should be a list of top 5 funding sources for the given startup. Please name the funding source in bold text and provide a brief description of the funding source.

"""

# Set streamlit page configuration
st.set_page_config(page_title="Startup Funding Finder")


# Run GenAI model
def handle_userinput(businessModel):
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    print(chat_prompt)
    if model == "OpenAI (high performance)":
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=key),
            prompt=chat_prompt,
        )
        fundingSources = chain.run(businessModel)
        st.write(fundingSources)
    else:
        chain = LLMChain(
            llm=HuggingFaceHub(huggingfacehub_api_token=key, repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1"),
            prompt=chat_prompt,
        )
    fundingSources = chain.run(businessModel)
    st.write(fundingSources)

# Define visibility
if "chat_visibility" not in st.session_state:
    st.session_state.chat_visibility = False
if "api_visibility" not in st.session_state:
    st.session_state.api_visibility = False
if "model_disable" not in st.session_state:
    st.session_state.model_disable = False
if "api_disable" not in st.session_state:
    st.session_state.api_disable = False

st.header("Startup Funding Finder")

# Choose model
model = st.segmented_control(
    "Choose a model",
    options=["Hugging Face (free)", "OpenAI (high performance)"],
    disabled=st.session_state.model_disable,
)
if model:
    st.session_state.api_visibility = True

def disable_model_and_api():
    st.session_state.model_disable = True
    st.session_state.api_disable = True

# OpenAI API key input
if st.session_state.api_visibility:
    key = st.text_input("Please enter your API key:", type="password", disabled=st.session_state.api_disable)
    if st.button("Process", on_click=disable_model_and_api):
        if key != "":
            st.session_state.chat_visibility = True
            st.write("API key ✅ Refresh page to change model or API key.")

# Prompt input
if st.session_state.chat_visibility:
    user_question = st.text_input("Please describe your startup idea:")
    if user_question:
        handle_userinput(user_question)
