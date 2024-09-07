import asyncio
from typing import List
from llama_index.core import VectorStoreIndex, Document
from llama_index.core.llms import LLM
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.core.query_engine import BaseQueryEngine

from pdf_slack_bot.utils import configs
from pdf_slack_bot.components.llms import load_llm
from pdf_slack_bot.prompts import (
    create_chat_prompt,
    QA_USER_PROMPT,
    QA_REFINE_USER_PROMPT,
    QA_SYSTEM_PROMPT
)


class DocumentRAG:
    """
    A class for performing document retrieval and question answering.
    """

    def __init__(self, llm_model: LLM = None):
        """
        Initialize the DocumentRAG with the LLM instance to use and SimpleFileNodeParser.

        Args:
            llm_model (LLM, optional): The instance of the LLM model to use. Defaults to DEFAULT_LLM value in configs.
        """

        self.llm = llm_model or load_llm(model=configs.DEFAULT_LLM)
        self._node_parser = SimpleFileNodeParser()

    async def _create_query_engine(self, documents: List[Document]) -> BaseQueryEngine:
        """
        Create and return a query engine based on the given documents and LLM.

        Args:
            documents (List[Document]): List of documents to index.


        Returns:
            BaseQueryEngine: The created query engine.
        """
        try:
            nodes = self._node_parser.get_nodes_from_documents(documents)
            index = VectorStoreIndex(
                nodes,
                use_async=True,
                show_progress=True
            )
            return index.as_query_engine(
                llm=self.llm,
                use_async=True,
                text_qa_template=create_chat_prompt(QA_SYSTEM_PROMPT, QA_USER_PROMPT),
                refine_template=create_chat_prompt(QA_SYSTEM_PROMPT, QA_REFINE_USER_PROMPT),
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create query engine: {str(e)}")

    async def _get_answer(self, query_engine: BaseQueryEngine, question: str) -> str:
        """
        Get an answer for a single question using the query engine.

        Args:
            query_engine (BaseQueryEngine): The query engine to use.
            question (str): The question to answer.

        Returns:
            str: The answer to the question.
        """
        try:
            response = await query_engine.aquery(question)
            return response.response
        except Exception as e:
            return f"Error answering question: {str(e)}"

    async def get_answers_from_documents(
            self,
            questions: List[str],
            documents: List[Document],
    ) -> List[str]:
        """
        Get answers for multiple questions from the given documents.

        Args:
            questions (List[str]): List of questions to answer.
            documents (List[Document]): List of documents to use for answering.

        Returns:
            List[str]: List of answers corresponding to the questions.

        Raises:
            ValueError: If questions or documents are empty.
        """
        if not questions:
            raise ValueError("No questions provided")
        if not documents:
            raise ValueError("No documents provided")

        try:
            query_engine = await self._create_query_engine(documents)
            answers = await asyncio.gather(*[self._get_answer(query_engine, question) for question in questions])
            return answers
        except Exception as e:
            raise RuntimeError(f"Failed to get answers: {str(e)}")
