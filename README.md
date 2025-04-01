# T.I.T.A.N

**Tools Intelligence and Task Assistance Network**

## Vision

We aim to develop an open-source, agentic system designed to automate simple digital tasks efficiently. 

Our system will be modular and scalable, and multilingual by default, by leveraging a multi-agent, containerized architecture powered by the phidata library.

The final agentic system will assist users through predefined agents capable of processing vocal, textual, and video inputs.

## Features

- Dockerized for easy setup and deployment.
- Simple interface powered by Streamlit.
  
## Requirements

- Docker
- Python 3.12+

## Setup

### 1. Clone the repository
Clone this repository to your local machine.

```bash
git clone https://github.com/justin-pinheiro/TITAN.git
cd TITAN
```

### 2. Build and run with Docker Compose
This will build then start both the **Ollama** container and the **App** container.

```bash
docker-compose up --build
```

### 3. Access the app

Once the containers are up and running, open your browser and go to:

```
http://localhost:8501
```

You should be able to interact with **TITAN** directly from the web app interface.

### 4. Requesting TITAN

For the first installation, you will have to wait until the Ollama model is pulled to make a request, otherwise you will get an error. This will take time only when you first build the Ollama container.

You can follow the download from the ollama container logs.

When you get 🟢 Done! on you console, you can start chatting with your agent !

### Streamlit App (`app.py`)

## Model

This app uses the `qwen2.5:14b` model from **Ollama**, a tool to run large language models locally. You can modify the model used in the app by changing the model ID in the Streamlit app.

## Troubleshooting

TODO
