# Restaurant Chatbot with LangChain and FastAPI

A restaurant chatbot that can answer customer questions, show menu items, and evaluate AI responses using LangChain and HuggingFace embeddings. Built with FastAPI and a modern Python backend.

---

## Features

- Conversational chatbot for restaurant queries.
- Menu lookup tools.
- Semantic search using HuggingFace embeddings.
- QA evaluation using evaluation tools.
- Clean architecture for easy extension and maintenance.

---

## Project Structure

itifinal/
│
├── app/
│ ├── init.py
│ ├── main.py # FastAPI application
│ ├── loader.py # Load chains and embeddings models
│ ├── prompts.py # All prompt templates
│ ├── tools.py # Menu tools
│ ├── states.py # Global state (chat history, chain)
│ └── models.py # Pydantic models
│
├── templates/ # HTML templates
│ └── index.html
│
├── static/ # JS, CSS
│ 
│
├── data/ # Menu CSV
│ └── menu.csv
│
├── requirements.txt
└── README.md

---

## Prerequisites

- Python **3.10**
- Linux or macOS recommended for proper HuggingFace support
- pip install all the libraries in requirements

---

## Setup

Open a terminal in the project root:

cd "Restaurant Chatbot/itifinal"

-

create .env file and add this line, replace it with your HuggingFace API Key:

HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxx"

-

"Restaurant Chatbot/itifinal/test/bin/python" -m uvicorn app:app --reload