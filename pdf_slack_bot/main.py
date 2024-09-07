import os
import json
import traceback
from typing import List

import nest_asyncio
from pdf_slack_bot.utils import configs
from pdf_slack_bot.components import load_llm, ActionSelector, DocumentGetter, DocumentRAG, SlackMessageSender

nest_asyncio.apply()


async def process_pdf_and_answer_questions(pdf_filename: str, questions: List[str]) -> List[dict]:
    """
    Process a PDF file and answer a list of questions based on its content.

    Args:
        pdf_filename (str): The name of the PDF file to process.
        questions (List[str]): A list of questions to answer.

    Returns:
        List[dict]: A list of dictionaries containing questions and their answers.
    """
    document_getter = DocumentGetter()
    document_rag = DocumentRAG()

    pdf_filepath = os.path.join(configs.pdf_dir, pdf_filename)
    documents = document_getter.get_documents_from_pdf(filepath=pdf_filepath)
    answers = await document_rag.get_answers_from_documents(questions, documents)

    return [{"question": q, "answer": a} for q, a in zip(questions, answers)]


async def main(pdf_filename: str, questions: List[str], agent_query: str):
    """
    Main function to process a PDF, answer questions, and send results to Slack.

    Args:
        pdf_filename (str): The name of the PDF file to process.
        questions (List[str]): A list of questions to answer.
        agent_query (str): The query to go to the agent along with the other inputs
    """
    logger = configs.logger
    llm = load_llm(os.getenv("OPENAI_MODEL", configs.DEFAULT_LLM))
    action_selector = ActionSelector(llm_model=llm)
    try:
        post_to_slack, reason = action_selector.select_action(questions, agent_query)
        logger.info(reason)
        response_obj = await process_pdf_and_answer_questions(pdf_filename, questions)

        logger.info("Successfully processed user queries!")
        if post_to_slack:
            slack_sender = SlackMessageSender()
            slack_sender.send_message(message=json.dumps(response_obj))
        else:
            return response_obj
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}: {traceback.print_exc()}")


if __name__ == "__main__":
    import asyncio

    PDF_FILENAME = "handbook.pdf"
    QUESTIONS = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?",
        "Who are the competitors of the company?"
    ]
    AGENT_QUERY = "Answer the questions and post results on Slack"
    asyncio.run(main(PDF_FILENAME, QUESTIONS, AGENT_QUERY))
