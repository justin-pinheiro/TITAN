# TITAN

For the moment, this is a simple web app that allows you to interact with the **Ollama** model through **Streamlit**. The app lets you communicate with the `llama3.1:8b` model, which runs locally in a Dockerized environment.

## Features

- Chat with the **Ollama** model directly in your browser.
- Dockerized for easy setup and deployment.

## Requirements

- Docker
- Docker Compose
- Python 3.12+

## Setup

### 1. Clone the repository
Clone this repository to your local machine.

```bash
git clone https://github.com/justin-pinheiro/TITAN.git
cd TITAN
```

### 2. Build and run with Docker Compose
This will build then start both the **Ollama** model and the **Streamlit** app.

```bash
docker compose build
docker compose up
```

These command will:
- Start the **Ollama** model in the background.
- Start the **Streamlit** app on port `8501`.

### 3. Access the app

Once the containers are up and running, open your browser and go to:

```
http://localhost:8501
```

You should be able to interact with the **Ollama** model directly from the web app.

### 4. Chatting with the agent

You will have to wait until the Llama model is pulled to make a request, otherwise you will get an error. This will take time only when you first build the container.

You can follow the download from the ollama container logs.

When you get 🟢 Done! on you console, you can start chatting with your agent !

## Components

### Docker Compose Configuration

- **Ollama service**:
  - Runs the **Ollama** model and exposes it on port `11434`.
  - Pulls the `llama3.1:8b` model during the startup using the entrypoint script.
  
- **App service**:
  - Builds the Streamlit app from the `Dockerfile` and serves it on port `8501`.
  - The Streamlit app sends requests to the **Ollama** model running on the **Ollama** container.

### Entry Point Script (`entrypoint.sh`)

The `entrypoint.sh` script:
1. Starts the **Ollama** model.
2. Pulls the `llama3.1:8b` model.
3. Ensures the model is ready before the app starts.

### Streamlit App (`app.py`)

The Streamlit app allows you to:
- Input a message.
- Send the message to the **Ollama** model.
- Display the model's response in the app.

## Model

This app uses the `llama3.1:8b` model from **Ollama**, a tool to run large language models locally. You can modify the model used in the app by changing the model ID in the Streamlit app.

## Troubleshooting

TODO