# Ask My Doc

**Ask My Doc** is an intuitive Q&A system that lets you upload your documents (PDF, Markdown, or text files) and ask questions in natural language. Powered by a backend microservice that processes your documents into a Retrieval Augmented Generation (RAG) model, Ask My Doc instantly retrieves relevant answers along with their sources.

---

## Features

- **Multi-File Support:** Upload PDFs, Markdown, and plain text files.
- **Dynamic UI:** The upload section disappears after successful processing and the Q&A section appears.
- **Intelligent Querying:** Ask questions about your documents and get precise answers.
- **Easy Setup:** Built with [Streamlit](https://streamlit.io/) for a smooth, web-based interface.

---

Note: This code uses ChatGPT APIs.

## Prerequisites

* You will need to have an OpenAI API account, with available usage tokens for ChatGPT4.
* You will also need an API Key, which you can create from https://platform.openai.com/account/api-keys
* Python 3.12 with libraries FastAPI, Pydantic (see requirements.txt)
* Docker on Linux (or Docker Desktop for MacOS)

## Steps to Run As Dockerised Web Service

1. Build and start up the services.
   ```
   ./rebuild.sh 
   ```
2. Check that the container is up.
   ```
   docker compose ps -a
   ```

To do limited customisation of the look of the UI, modify the [config.toml](frontend/.streamlit/config.toml) file.