# AI Telegram Bot

An asynchronous Telegram bot integrated with DeepSeek (LLM) for code generation and Q&A. Built with aiogram, asyncio, and FastAPI (for web interface, see separate repo).

## Features
- `/ask <question>` – ask any question, get AI answer.
- `/code <task>` – generate Python code for a given task.
- Asynchronous request handling with aiogram.
- Message splitting for long responses (Telegram limit 4096 chars).
- Environment variable configuration.

## Tech Stack
- Python 3.10+
- aiogram (asyncio Telegram Bot framework)
- DeepSeek API (OpenAI-compatible)
- python-dotenv for configuration
- asyncio for concurrent processing

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your tokens
4. Run: `python main.py`

## Deployment
The bot is designed to be deployed on a Linux server (Ubuntu) with systemd auto-restart and Nginx reverse proxy (optional for webhooks). See the web-interface project for a management dashboard.
