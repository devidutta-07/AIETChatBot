import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# Load models once
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)

embedding = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv("MISTRAL_API_KEY")
)

prompt = ChatPromptTemplate([
    ("system", """You are a helpful AI assistant.

Answer ONLY using provided context.

If answer not found → reply "NO DATA".

Context:
{context}
"""),
    ("human", "Question: {question}")
])

vectordb = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embedding,
    namespace="aiet_data"
)

retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20}
)

def ask_question(query):
    docs = retriever.invoke(query)

    if not docs:
        return "NO DATA"

    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.invoke({
        "question": query,
        "context": context
    })

    response = model.invoke(final_prompt)

    return response.content