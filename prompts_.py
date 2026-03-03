from langchain_core.prompts import PromptTemplate,ChatPromptTemplate


def rewrite_query_prompt(query):

    new_query=f"""
        Rewrite this query to be optimized for semantic search in a food menu database:
        User query: {query}

        Return a short, keyword-only search query.
        If the input is not related to food (like greetings), just return an empty string.
        """
    
    return new_query


MAIN_PROMPT_TEMPLATE = PromptTemplate.from_template(
    """You are a helpful restaurant assistant.
You have access to the following tool:

menu() - Use this tool ONLY when the user asks to see the restaurant menu or asks what items are available.

Use the context provided to answer user questions:

Context:
{context}

Question:
{question}

Answer concisely and meaningfully based on the user question. If a tool is relevant, call it."""
)


QA_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strict QA evaluator for a fried chicken restaurant chatbot. 
        Given a customer question and the AI's answer, evaluate the response.\n
        Reply with ONLY valid JSON — no markdown, no extra text:\n
        '{{"score": <float 0.0-1.0>, "comment": "<one sentence reasoning>"}}'"""
    ),
    (
        "human",
        "Question: {inputs}\nAnswer: {outputs}"
    ),
])