# Fin-ChatBot Technical Documentation

Fin-ChatBot is an AI-powered chatbot designed to answer financial queries. It utilizes OpenAI's GPT-4o-mini model via OpenRouter API to provide intelligent responses. The project focuses on a robust backend API and is deployed on Render for online access.

## Project Structure

Fin-ChatBot/
├── app/
│   ├── main.py           # FastAPI server with chat endpoint
│   ├── models.py         # Pydantic models for request/response
│   ├── llm\_backends.py   # Logic for AI interaction with OpenRouter
│   ├── db.py             # Database connections and operations (if used)
│   └── requirements.txt  # Python dependencies
├── README.md            # Project documentation
└── .gitignore           # Git ignore file

## Features

* AI-Powered Chat: Provides intelligent responses to financial queries.
* FastAPI Backend: Lightweight and fast API server.
* Health Check Endpoint: /health to verify server status.
* Chat Endpoint: /chat for sending user messages and receiving AI responses.
* Deployed on Render: [(https://fin-chatbot.onrender.com)](https://fin-chatbot.onrender.com) – accessible online without local setup.
* Extensible: Modular design for features like context memory, multi-user support, and analytics.

## Getting Started

### Prerequisites

* Python 3.10+
* pip
* OpenRouter API Key

### Installation

1. Clone the repository:

```
git clone https://github.com/abhijitupasani/Fin-ChatBot.git
cd Fin-ChatBot
```

2. Create a virtual environment:

```
python -m venv .venv
```

3. Activate the virtual environment:

* Windows: `.venv\Scripts\activate`
* Linux/MacOS: `source .venv/bin/activate`

4. Install dependencies:

```
pip install -r app/requirements.txt
```

5. Set your OpenRouter API Key:

* Windows: `setx OPENROUTER_API_KEY "your_api_key_here"`
* Linux/MacOS: `export OPENROUTER_API_KEY="your_api_key_here"`

## Running the Server

```
uvicorn app.main:app --reload
```

* Server runs at [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
* Chat Endpoint: [http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)
* Deployed Render URL: [https://fin-chatbot.onrender.com](https://fin-chatbot.onrender.com)

## API Documentation

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Example Request

POST `/chat` with JSON body:

```
{
  "user_id": "u1",
  "message": "What is the best way to save for retirement? Answer in bullet points"
}
```

Example Response:

```
{
  "reply": "• Start with an emergency fund\n• Contribute to retirement accounts (401k, IRA)\n• Diversify investments\n• Review your plan annually\n• Consider consulting a financial advisor"
}
```

## Deployment

* Live version on Render: [https://fin-chatbot.onrender.com](https://fin-chatbot.onrender.com)
* Send POST requests directly to: `https://fin-chatbot.onrender.com/chat`
* Automatic deployment via GitHub integration.
* Environment variables used for sensitive API keys.

## Future Enhancements

* Multi-user support with session memory.
* Logging and analytics for chat interactions.
* Frontend interface for user-friendly chat.
* Enhanced AI response tuning with context awareness.
* Database integration for conversation history.

## License

MIT License
