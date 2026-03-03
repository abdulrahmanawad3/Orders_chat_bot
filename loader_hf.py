from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace,HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from states import States
from prompts_ import MAIN_PROMPT_TEMPLATE,QA_PROMPT
from rag.ingest import rag_
from dotenv import load_dotenv
import os
from helper import TOOLS,handle_tool_calls

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def load_main_model():
    
    hf_model = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.5,
        timeout=120,
        huggingfacehub_api_token=HF_TOKEN,
        streaming=True,
        model=""
    )
    States.main_llm = ChatHuggingFace(llm=hf_model, verbose=True).bind_tools(
        list(TOOLS.values())
    )
    States.main_llm_loaded = True
    print("main Loaded")


def load_embedding_model():
    States.embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder=os.path.expanduser("~/.cache/huggingface/embeddings")
    )
    States.embedding_model_loaded = True
    print("embedding Loaded")


def load_secondary_model():

    hf_rewriter_model = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-4B-Instruct-2507",
    task="text-generation",
    max_new_tokens=256,
    temperature=0.3,
    huggingfacehub_api_token=HF_TOKEN,
    model="",
    )
    States.secondary_llm = ChatHuggingFace(llm=hf_rewriter_model, verbose=True)
    print("secondary Loaded")
    
def load_judge():
    States.judge_chain = QA_PROMPT | States.main_llm | StrOutputParser()
    States.judge_chain_loaded = True
    

def load_chain():
    if not States.main_llm_loaded:
        load_main_model()
    
    if not States.secondary_llm_loaded:
        load_secondary_model()

    if not States.embedding_model_loaded:
        load_embedding_model()

    States.chain = (
        {"context": rag_, "question": RunnablePassthrough()}
        | MAIN_PROMPT_TEMPLATE
        | States.main_llm
        | RunnableLambda(handle_tool_calls)
    )
    States.chain_loaded = True
