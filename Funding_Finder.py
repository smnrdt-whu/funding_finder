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
    st.write(fundingSources[fundingSources.index("Assistant:") + len("Assistant:"):])


# Define visibility
if "chat_visibility" not in st.session_state:
    st.session_state.chat_visibility = False
if "api_visibility" not in st.session_state:
    st.session_state.api_visibility = False

st.header("Startup Funding Finder")

# Choose model
model = st.segmented_control(
    "Choose a model",
    options=["Hugging Face (free)", "OpenAI (high performance)"],
)

if model:
    st.session_state.api_visibility = True
    choice = model

# OpenAI API key input
if st.session_state.api_visibility:
    key = st.text_input("Please enter your API key:", type="password")
    if st.button("Process"):
        if key != "":
            st.write("API key ✅")
            st.session_state.chat_visibility = True

# Prompt input
if st.session_state.chat_visibility:
    user_question = st.text_input("Please describe your startup idea in one sentence:")
    if user_question:
        handle_userinput(user_question)
