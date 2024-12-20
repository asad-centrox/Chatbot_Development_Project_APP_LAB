# RAG Chatbot


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
    - [Creating a Conda Environment](#creating-a-conda-environment)
    - [Activating the Environment](#activating-the-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Running the Project](#running-the-project)
- [Docker Setup](#docker-setup)
  - [Building the Docker Image](#building-the-docker-image)
  - [Running the Docker Container](#running-the-docker-container)
- [Usage](#usage)
  - [Uploading PDF Documents](#uploading-pdf-documents)
  - [Interacting with the Chatbot](#interacting-with-the-chatbot)
  - [Access the Chatbot Interface](#access-the-chatbot-interface)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

---

## Introduction

Welcome to the **RAG Chatbot** project! This project is a Retrieval-Augmented Generation (RAG) chatbot designed to facilitate the upload of PDF documents and provide intelligent responses based on the content of those documents. Leveraging cutting-edge technologies such as FastAPI, LangChain, and FAISS, this chatbot enables users to interact with their documents seamlessly, making it an ideal tool for information retrieval, customer support, and knowledge management.

This project has been developed for **Applab.qa** as part of the selection process for the AI/ML Engineer position.

---

## Features

- **PDF Uploading:** Easily upload PDF documents to the chatbot for processing.
- **Intelligent Q&A:** Ask questions related to the uploaded documents and receive accurate responses.
- **Document Retrieval:** Utilizes FAISS for efficient similarity search and retrieval.
- **User-Friendly Interface:** Built with FastAPI, providing a smooth and responsive user experience.
- **Scalable Architecture:** Designed to handle multiple requests and large datasets effectively.

---

## Technologies Used

- **Python 3.11**
- **FastAPI:** For building the web API.
- **LangChain:** For language model interactions.
- **FAISS:** For efficient similarity search.
- **OpenAI GPT-3.5 Turbo:** As the underlying language model.
- **Docker:** For containerization and deployment.
- **Other Libraries:** Including NumPy, Pydantic, and more as specified in `requirements.txt`.

---

## Getting Started

Follow these instructions to set up and run the RAG Chatbot locally.

### Prerequisites

- **Conda:** Ensure that Conda is installed on your machine. You can download it from [here](https://docs.conda.io/en/latest/miniconda.html).
- **Docker:** Install Docker for containerization. Download Docker from [here](https://www.docker.com/get-started).

### Environment Setup

#### Creating a Conda Environment

Open your terminal and run the following command to create a new Conda environment:

```bash
conda create -n rag_chatbot python=3.11.8

Activating the Environment
Activate the newly created environment with:

conda activate rag_chatbot

Installing Dependencies
Install the required Python packages using pip:

pip install -r requirements.txt

Running the Project
To run the project, execute the following script:

./scripts/run-dev.sh

This script will:

Export environment variables from the .env file.
Run type checks using mypy.
Format the code with black.
Lint the code using pylint.
Start the FastAPI server with Uvicorn.


For Docker Setup:

Building the Docker Image:
Build the Docker image using the following command:

sudo docker build -t chatbot .

Running the Docker Container
Run the Docker container with the following command:

sudo docker run -it -p 8080:8080 chatbot

Once the container is running, you can access the application at:

Swagger UI: http://localhost:8080/api/docs
ReDoc: http://localhost:8080/api/redocs

Usage:
Uploading PDF Documents
Navigate to the /upload endpoint to upload your PDF file.

Interacting with the Chatbot
Use the /bot endpoint to ask questions related to the content of the uploaded document.

Access the Chatbot Interface
Visit the /chatbot_interface endpoint to access the user-friendly interface.



Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.


License
This project is licensed under the MIT License.

Acknowledgments
Thanks to the LangChain and FastAPI communities for their excellent libraries and documentation.
Special thanks to Applab.qa for the opportunity to showcase this project