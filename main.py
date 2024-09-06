import os
import json
from typing import List

import nest_asyncio
from utils import configs
from components import DocumentGetter, DocumentRAG, SlackMessageSender

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
    rag = DocumentRAG()

    pdf_filepath = os.path.join(configs.pdf_dir, pdf_filename)
    documents = document_getter.get_documents_from_pdf(filepath=pdf_filepath)
    answers = await rag.get_answer_from_documents(questions, documents)

    return [{"question": q, "answer": a} for q, a in zip(questions, answers)]


async def main(pdf_filename: str, questions: List[str]):
    """
    Main function to process a PDF, answer questions, and send results to Slack.

    Args:
        pdf_filename (str): The name of the PDF file to process.
        questions (List[str]): A list of questions to answer.
    """
    try:
        logger = configs.logger
        response_obj = await process_pdf_and_answer_questions(pdf_filename, questions)

        slack_sender = SlackMessageSender()
        slack_sender.send_message(message=json.dumps(response_obj))

        logger.info("Processing completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    import asyncio

    PDF_FILENAME = "handbook.pdf"
    QUESTIONS = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ]

    asyncio.run(main(PDF_FILENAME, QUESTIONS))
