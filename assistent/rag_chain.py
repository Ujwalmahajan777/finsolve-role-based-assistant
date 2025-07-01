from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import ContextualCompressionRetriever
from langchain_chroma import Chroma  
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnableSequence
)
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os


load_dotenv()

# combine retrieved documents into string context
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



def get_rag_chain(role: str):
    # Load existing vector DB
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory="./vector_store", embedding_function=embedding)

    # LLM 
    model = ChatDeepSeek(model_name="deepseek-chat")


    # Role-based filtering 
    role = role.strip().lower()
    if role == "c-level":
        base_retriever = vector_store.as_retriever(search_kwargs={"k": 15})  # Full access
    else:
        base_retriever = vector_store.as_retriever(search_kwargs={"k": 15, "filter": {"role": role}})

    # Optional: compress documents for better context
    base_compressor = LLMChainExtractor.from_llm(model)
    retriever = ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=base_compressor
    )

    # Prompt 
    prompt = PromptTemplate(
        template=(
           " You are a domain expert AI working at a FinTech company."
            "You are assisting a user with the rYour job is to analyze the provided internal dole: **{role}**."
            "Your job is to analyze the provided internal documentation and generate a thorough, insightful response."
            "The response should be:"
            "- Specific to the user's role and access level"
            "- c level has full access of documents doesnt matter which sector it belong"
            "- In-depth and structured like a financial analyst's report"
            "- Include key numbers, insights, and relevant trends"
            "- Reference key facts from the documents when possible"

            "Only use information from the context provided."
            "If data is not found or not permitted, respond: “I don’t have access to that information.”"

            "Context:{context}"
            

            "Question:{question}"
            

        ),
        input_variables=["context", "question", "role"]
    )

    # Runnable chain
    parallel_chain = RunnableParallel({
        "context": RunnableLambda(lambda x: x["question"]) | retriever | RunnableLambda(format_docs),
        "question": RunnableLambda(lambda x: x["question"]),
        "role": RunnableLambda(lambda x: x["role"])
    })

    main_chain = RunnableSequence(
        parallel_chain | prompt | model | StrOutputParser()
    )

    return main_chain



