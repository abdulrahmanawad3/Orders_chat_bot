from states import States
from prompts_ import rewrite_query_prompt
from rag.retrievers import load_retrievers

def query_gate(query :str):
    query = query.strip().lower()
    if len(query)<3 or query in ["hi","ok","thank","thanks","bye","okay","hey","welcome","test"]:

        return []
    return True

def clean_to_dict(retrieved_data):
    fdicta={}
    names=set()

    for no, block in enumerate(retrieved_data):

        dicta={}
        skip=False

        for content in block:

            key,val=content.split(":",1)
            key=key.strip()
            val=val.strip()

            if key=="Name":

                if val.strip() in names:
                    skip=True
                    break
                names.add(val)
            dicta[key]=val

        if not skip:    
            fdicta[f"Item {no}"]=dicta

    return fdicta


def rag_(query):

    if not States.retrievers_loaded:
        load_retrievers()

    rewriten = States.secondary_llm.invoke(rewrite_query_prompt(query)).content.strip()

    if query_gate:
        reteived_vec=States.vec_retriever.invoke(rewriten)
        reteived_bm25=States.bm25.invoke(rewriten)
    else:
        reteived_vec=[]
        reteived_bm25=[]

    output=[d.page_content.split("\n") for d in reteived_vec + reteived_bm25]
    
    return clean_to_dict(output)