from typing import List, Tuple
from llama_index.core.llms import LLM
from llama_index.core.selectors import LLMSingleSelector

from pdf_slack_bot.utils import configs
from pdf_slack_bot.components.llms import load_llm
from pdf_slack_bot.prompts import ACTION_SELECTION_PROMPT


class ActionSelector:
    """
    A class for selecting actions based on given questions and agent query.
    """

    def __init__(self, llm_model: LLM = None):
        """
        Initialize the ActionSelector with a specified LLM model.

        Args:
            llm_model (LLM, optional): The instance of the LLM model to use. Defaults to DEFAULT_LLM value in configs.
        """
        self.llm = llm_model or load_llm(model=configs.DEFAULT_LLM)
        self.selector = LLMSingleSelector.from_defaults(
            llm=self.llm,
            prompt_template_str=ACTION_SELECTION_PROMPT
        )

    def select_action(self, questions: List[str], agent_query: str) -> Tuple[bool, str]:
        """
        Select an action based on the given questions and agent query.

        Args:
            questions (List[str]): List of questions to consider.
            agent_query (str): The query from the agent.

        Returns:
            Tuple[bool, str]: A tuple containing:
                - A boolean indicating whether to post results to Slack (True) or not (False).
                - The reason for the selection.

        Raises:
            ValueError: If questions or agent_query is empty.
        """
        if not questions:
            raise ValueError("No questions provided")
        if not agent_query:
            raise ValueError("No agent query provided")

        try:
            choices = [
                "Post results to slack.",
                "Do not post results to slack.",
            ]
            selector_result = self.selector.select(
                choices, query=f"QUERY LIST: {questions}\n\nUSER QUESTION: {agent_query}"
            )
            post_to_slack = selector_result.selections[0].index == 0
            reason = selector_result.selections[0].reason
            return post_to_slack, reason
        except Exception as e:
            raise RuntimeError(f"Failed to select action: {str(e)}")


if __name__ == "__main__":
    QUESTIONS = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?",
        "Who are the competitors of the company?"
    ]
    AGENT_QUERY = "Answer the questions and post results on Slack"

    action_selector = ActionSelector()
    post_results_to_slack, reason = action_selector.select_action(QUESTIONS, AGENT_QUERY)
    print(post_results_to_slack)
    print(reason)
