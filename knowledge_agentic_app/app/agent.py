from pydantic_ai import Agent, Tool
import os
from app.kb_manager import search_knowledge

# Set your OpenAI API key as an environment variable for best practice
os.environ["OPENAI_API_KEY"] = "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"

@Tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information."""
    return f"Web search result for: {query}"

class KnowledgeAgent(Agent):
    def answer(self, question: str, knowledge_only: bool = True) -> str:
        kb_results = search_knowledge(question)
        kb_context = "\n".join([item["content"] for item in kb_results])
        if knowledge_only or not kb_context:
            context = f"Knowledge Base:\n{kb_context}\n"
        else:
            web_result = web_search(question)
            context = f"Knowledge Base:\n{kb_context}\nWeb Search:\n{web_result}\n"
        result = self.run_sync(
            f"{context}\nQuestion: {question}\nAnswer:"
        )
        return result.output.strip()

# Instantiate the agent with the model string
agent = KnowledgeAgent(model="openai:gpt-3.5-turbo")
