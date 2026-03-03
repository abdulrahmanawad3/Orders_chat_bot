from collections import deque
from typing import Optional, Any

class States:
    vectorstore: Optional[Any] = None

    embedding_model: Optional[Any] = None
    embedding_model_loaded: bool = False

    main_llm: Optional[Any] = None
    main_llm_loaded: bool = False

    secondary_llm: Optional[Any] = None
    secondary_llm_loaded: bool = False

    chain: Optional[Any] = None
    chain_loaded: bool = False

    judge_chain: Optional[Any] = None
    judge_chain_loaded: bool = False


    bm25: Optional[Any] = None
    vec_retriever: Optional[Any] = None
    retrievers_loaded: bool = False

    chat_history: deque = deque(maxlen=20)

    data: Optional[Any] = None
    data_loaded: bool = False