import asyncio
from typing import List
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import Document
from llama_index.core.node_parser import SimpleFileNodeParser

from components.llms import load_llm


class DocumentRAG:
    def __init__(self):
        self._node_parser = SimpleFileNodeParser()

    async def get_answer_from_documents(self, questions: List[str], documents: List[Document], llm_to_use: str = None):
        async def _get_answer(question):
            print(question)
            response = await query_engine.aquery(question)
            print(response)  # TODO: extract more info from the responses
            return response.response

        llm = load_llm(model=llm_to_use or 'gpt-4o-mini')
        nodes = self._node_parser.get_nodes_from_documents(documents)
        index = VectorStoreIndex(
            nodes,
            use_async=True,
            show_progress=True
        )
        # TODO: Add custom prompts
        query_engine = index.as_query_engine(
            llm=llm,
            use_async=True,
            # streaming=stream,
            # text_qa_template=ChatPromptTemplate(qa_prompt or []),
            # refine_template=ChatPromptTemplate(refine_prompt or [])
        )
        answers = await asyncio.gather(*[_get_answer(question) for question in questions])
        return answers
