import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain

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
    chain = LLMChain(
        llm=ChatOpenAI(openai_api_key=key),
        prompt=chat_prompt,
    )
    fundingSources = chain.run(businessModel)
    st.write(fundingSources)

# Define visibility of input field
if "chat_visibility" not in st.session_state:
    st.session_state.chat_visibility = False

st.header("Startup Funding Finder")

# OpenAI API key input
key = st.text_input("Please enter your OpenAI API key:", type="password")
if st.button("Process"):
    if key != "":
        st.write("OpenAI API key ✅")
        st.session_state.chat_visibility = True
            
# Prompt input
if st.session_state.chat_visibility:
    user_question = st.text_input("Please describe your startup idea in one sentence:")
    if user_question:
        handle_userinput(user_question)