#------------------------------------------
# Import Statements
#------------------------------------------

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


#------------------------------------------
# Load Raw PDF
#------------------------------------------

pdfs_directory = "pdfs/"

def upload_pdf(file):
    with open(pdfs_directory + file.name , "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader = PDFPlumberLoader(file_path=file_path)
    documents = loader.load()
    return documents 


#------------------------------------------
# Chunks from PDF
#------------------------------------------

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        add_start_index = True
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks


#------------------------------------------
# Setup Embeddings model
#------------------------------------------

# ollama_model = "deepseek-r1:8b"
def get_embeddings_model():
    embeddings_model = OllamaEmbeddings(model = "nomic-embed-text")
    return embeddings_model


#------------------------------------------
# Setup FAISS
#------------------------------------------


documents = load_pdf('pdfs/sample_pdf_file.pdf')
print("Len of Document :- " , len(documents))
text_chunks = create_chunks(documents)
print("Chunk Count :- " , len(text_chunks))
FAISS_DB_PATH = "vectorstore/db_faiss"
faiss_db = FAISS.from_documents(text_chunks , get_embeddings_model())
faiss_db.save_local(FAISS_DB_PATH)


