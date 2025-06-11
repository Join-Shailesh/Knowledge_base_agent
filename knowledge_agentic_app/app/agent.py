from pydantic_ai import Agent, Tool
import os
from app.kb_manager import search_knowledge

# Set your Groq API key as an environment variable (recommended)
os.environ["GROQ_API_KEY"] = "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"

@Tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information."""
    return f"Web search result for: {query}"

class KnowledgeAgent(Agent):
    def answer(self, question: str, knowledge_only: bool = True) -> str:
        kb_results = search_knowledge(question)
        kb_context = "\n".join([item["content"] for item in kb_results])

        if knowledge_only:
            if not kb_context:
                return "No knowledge available to answer this question."
            print("Knowledge base content found, using it to answer the question.")
            context = f"format this Knowledge Base content only:\n{kb_context}\n"
        else:
            if kb_context:
                print("No Knowledge base content found, using it to answer the question.")
                context = f"format this Knowledge Base and procide some references or souce alongside :\n{kb_context}\n"
            else:
                print("No knowledge base content found, using web search tool.")
                # Instruct the agent/model to use the web_search tool if needed
                context = (
                    "Append note 'fond no knowledge base content, so did web search' "
                    "No knowledge base content found. "
                    "You may use the web_search tool to answer the question.\n"
                )

        result = self.run_sync(
            f"{context}\nQuestion: {question}\nAnswer:"
        )
        return result.output.strip()


# Instantiate the agent with the Groq model string
agent = KnowledgeAgent(model="groq:llama-3.3-70b-versatile")
