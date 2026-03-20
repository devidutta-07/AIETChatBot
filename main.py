import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)

embedding = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv("MISTRAL_API_KEY")
)

prompt = ChatPromptTemplate([
    ("system", """You are a helpfull document-based AI assistant.

You MUST answer ONLY from the provided context.

Rules:
1. Use ONLY the given context to answer.
2. If the answer is NOT present in the context, reply exactly with: "NO DATA".
2. Do NOT use your own knowledge.
3. Do NOT guess or assume.
4. Keep answers concise and accurate.

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
    search_kwargs={"k": 3, "fetch_k": 10}
)

while True:
    query = input("Ask Question from the document: ")

    if query == "0":
        break
    query = query.lower().strip()
    docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.invoke({
        "question": query,
        "context": context
    })

    response = model.invoke(final_prompt)
    print(response.content)