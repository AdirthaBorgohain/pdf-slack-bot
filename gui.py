import os
import logging
import asyncio
import nest_asyncio
import streamlit as st
from typing import List
from io import StringIO

from pdf_slack_bot.utils import configs
from pdf_slack_bot.components import load_llm, ActionSelector, DocumentGetter, DocumentRAG, SlackMessageSender

nest_asyncio.apply()


class StreamlitHandler(logging.Handler):
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.log_buffer = StringIO()

    def emit(self, record):
        log_entry = self.format(record)
        self.log_buffer.write(log_entry + '\n')
        self.container.text_area("Logs", value=self.log_buffer.getvalue(), height=200)


# Set up the logger with the custom StreamHandler
@st.cache_resource
def setup_logger():
    logger = logging.getLogger("streamlit_logger")
    logger.setLevel(logging.INFO)
    log_container = st.empty()
    handler = StreamlitHandler(log_container)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger()


async def process_pdf_and_answer_questions(pdf_filename: str, questions: List[str]) -> List[dict]:
    document_getter = DocumentGetter()
    document_rag = DocumentRAG()

    pdf_filepath = os.path.join(configs.pdf_dir, pdf_filename)
    documents = document_getter.get_documents_from_pdf(filepath=pdf_filepath)
    answers = await document_rag.get_answers_from_documents(questions, documents)

    return [{"question": q, "answer": a} for q, a in zip(questions, answers)]


async def main(pdf_file, questions: List[str], agent_query: str):
    llm = load_llm(os.getenv("OPENAI_MODEL", configs.DEFAULT_LLM))
    action_selector = ActionSelector(llm_model=llm)

    try:
        # Save uploaded file
        pdf_filename = pdf_file.name
        pdf_path = os.path.join(configs.pdf_dir, pdf_filename)
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        post_to_slack, reason = action_selector.select_action(questions, agent_query)
        logger.info(reason)
        response_obj = await process_pdf_and_answer_questions(pdf_filename, questions)

        logger.info("Successfully processed user queries!")
        if post_to_slack:
            slack_sender = SlackMessageSender()
            slack_sender.send_message(message=str(response_obj))
            logger.info("Results posted to Slack!")
        return response_obj
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        st.error(f"An error occurred: {str(e)}")


st.title("PDF Question Answering Bot")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

questions = st.text_area("Enter your questions (one per line)")
agent_query = st.text_input("Enter agent query (explicitly specify if you want the answers to be posted to slack)")

if st.button("Process PDF and Answer Questions"):
    if uploaded_file is not None and questions and agent_query:
        questions_list = [q.strip() for q in questions.split("\n") if q.strip()]
        with st.spinner("Processing..."):
            results = asyncio.run(main(uploaded_file, questions_list, agent_query))

        if results:
            st.subheader("Results:")
            for item in results:
                st.write(f"**Q: {item['question']}**")
                st.write(f"A: {item['answer']}")
    else:
        st.warning("Please upload a PDF file, enter questions, and provide an agent query.")

st.sidebar.header("About")
st.sidebar.info(
    "This Streamlit app allows you to upload a PDF, ask questions about its content, and optionally post results to Slack.")
