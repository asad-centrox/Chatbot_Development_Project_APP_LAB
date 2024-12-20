"""Hi this is Chatbot
"""

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from utils import get_full_path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(
    prefix="",
    tags=["chatbot"],
    dependencies=[],
    responses={},
)

pdf_directory = get_full_path("../public/pdf")

# Ensure the PDF directory exists
os.makedirs(pdf_directory, exist_ok=True)

# Initialize variables for vector store and embeddings
vector_store = None
embeddings = None

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, max_tokens=512)

template = """Use the following pieces of information to answer the user's question. You are provided policy documents, and your purpose is to assist with inquiries related to the content of these documents. Ensure your responses are based on the information within the PDFs.

If you cannot find a relevant answer in the PDFs, politely inform the user that your knowledge is limited to the provided documents.

---

Context:
{context}

Question:
{question}

---

Only return the helpful answer below and nothing else:

Helpful answer:

---

**Response Details:**
- Ensure the response is clear, concise, and covers all relevant details.
- Use bullet points or similar formatting for readability.
- Provide a detailed yet concise explanation to enhance understanding.
"""

qa_prompt = PromptTemplate(
    template=template, input_variables=["context", "question", "chat_history"]
)

chain = None  # Initialize chain variable


class ChatbotInput(BaseModel):
    input_text: str


def create_chain():
    global chain
    if vector_store is not None:
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": 0.7},
            ),
            return_source_documents=True,
            chain_type_kwargs={
                "verbose": True,
                "prompt": qa_prompt,
            },
        )


def chatbot(chatbot_input_text: str):
    print(f"Received question: {chatbot_input_text}")

    try:
        if chain is None:
            raise Exception(
                "Chatbot chain is not initialized. Please upload a PDF first."
            )

        result = chain(chatbot_input_text)
        response = result["result"]
        source_documents = result["source_documents"]

        if "I cannot provide information on that; it's beyond my scope." in response:
            print("No relevant information found; returning only the response.")
            full_response = {"response": response}
        else:
            full_response = {
                "response": response,
                "similar_search_results": [
                    {
                        "page_content": doc.page_content,
                        "metadata": {
                            "source": os.path.basename(doc.metadata["source"]),
                            "page": doc.metadata.get("page", "unknown"),
                        },
                    }
                    for doc in source_documents
                ],
            }

        print(f"Response: {response}")
        print(f"Similarity search results: {source_documents}")
        return full_response

    except Exception as e:
        error_message = f"Internal Server Error: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message) from e


@router.post("/bot")
def chatbot_endpoint(chatbot_input: ChatbotInput):
    print(f"Request received for /bot: {chatbot_input.input_text}")
    response = chatbot(chatbot_input.input_text)
    print(f"Response for /bot: {response}")
    return response


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store, embeddings, chain  # Use global variables

    try:
        # Ensure the filename is a string
        filename = (
            file.filename if file.filename else "uploaded_file.pdf"
        )  # Fallback filename
        file_location = os.path.join(pdf_directory, filename)

        # Save the uploaded file to the specified directory
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Load the new document and process it
        loader = PyPDFDirectoryLoader(pdf_directory)
        documents = loader.load()

        # Split the documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_chunks = text_splitter.split_documents(documents)

        # Generate embeddings for the new chunks
        if text_chunks:
            embeddings = OpenAIEmbeddings(disallowed_special=())
            vector_store = FAISS.from_documents(text_chunks, embeddings)
            create_chain()  # Create the chain after the vector store is initialized

        return {
            "filename": filename,
            "message": "File uploaded and processed successfully.",
        }

    except Exception as e:
        error_message = f"Error uploading file: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message) from e


app.include_router(router)
