import os
from dotenv import load_dotenv

from langchain_mistralai import MistralAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader,WebBaseLoader,UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
load_dotenv()

embedding = MistralAIEmbeddings(
    model="mistral-embed"
)
os.environ["USER_AGENT"] = "AIETChatBot/1.0"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
pc = Pinecone(api_key=PINECONE_API_KEY)

# PDF
pdf_loader = PyMuPDFLoader("aiet.pdf")
pdf_docs = pdf_loader.load()

# DOCX
docx_loader = UnstructuredWordDocumentLoader("pgdca.docx")
docx_docs = docx_loader.load()

# Website
web_loader = WebBaseLoader("https://aiet-classes.vercel.app/")
web_docs = web_loader.load()

for doc in pdf_docs:
    doc.metadata["source"] = "pdf"
    doc.metadata["file"] = "aiet.pdf"

for doc in docx_docs:
    doc.metadata["source"] = "docx"
    doc.metadata["file"] = "pgdca.docx"

for doc in web_docs:
    doc.metadata["source"] = "web"
    doc.metadata["url"] = "https://aiet-classes.vercel.app/"

all_docs = pdf_docs + docx_docs + web_docs

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(all_docs)


vectordb = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embedding,
    index_name=INDEX_NAME,
    namespace="aiet_data"
)
