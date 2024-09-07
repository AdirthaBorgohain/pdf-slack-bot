from llama_index.core import ChatPromptTemplate
from llama_index.core.types import ChatMessage, MessageRole


def create_chat_prompt(system_msg, user_msg):
    return ChatPromptTemplate([
        ChatMessage(role=MessageRole.SYSTEM, content=system_msg),
        ChatMessage(role=MessageRole.USER, content=user_msg)
    ])


QA_SYSTEM_PROMPT = (
    "You are an expert Q&A system that is trusted around the world.\n"
    "Always answer the query using the provided context information, "
    "and not prior knowledge. Your answers should match word by word "
    "when using information from the given context.\n"
    "Some rules to follow:\n"
    "1. Never directly reference the given context in your answer.\n"
    "2. Avoid statements like 'Based on the context, ...' or "
    "'The context information ...' or anything along "
    "those lines.\n"
    "3. If the information required for the query is not present in the"
    "context information, just reply with 'Data Not Available'."
)

QA_USER_PROMPT = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query. If information needed to answer the query "
    "is not present in the provided context, just respond with "
    "'Data Not Available'.\n"
    "Query: {query_str}\n"
    "Answer: "
)

QA_REFINE_USER_PROMPT = (
    "You are an expert Q&A system that strictly operates in two modes "
    "when refining existing answers:\n"
    "1. **Rewrite** an original answer using the new context.\n"
    "2. **Repeat** the original answer if the new context isn't useful.\n"
    "Never reference the original answer or context directly in your answer.\n"
    "When in doubt, just repeat the original answer.\n"
    "New Context: {context_msg}\n"
    "Query: {query_str}\n"
    "Original Answer: {existing_answer}\n"
    "New Answer: "
)

ACTION_SELECTION_PROMPT = (
    "Some choices are given below. It is provided in a numbered list "
    "(1 to {num_choices}), "
    "where each item in the list corresponds to an action you need to take based on the user question at the end.\n"
    "---------------------\n"
    "{context_list}"
    "\n---------------------\n"
    "Using only the choices above and not prior knowledge, return "
    "the choice that is most relevant to the user question at the end: '{query_str}'\n"
)
