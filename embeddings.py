from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

loader1 = PyPDFLoader("data/Carton Caps Referral FAQs.pdf")
loader2 = PyPDFLoader("data/Carton Caps Referral Program Rules.pdf")
docs = loader1.load() + loader2.load()
embedding = OllamaEmbeddings(model="snowflake-arctic-embed")
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="data/chroma_db"
)

def load_pdf_context(query: str) -> str:
    results = vectorstore.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])