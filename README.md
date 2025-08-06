# RAG-Powered Voice Assistant with LiveKit and FastAPI

A voice-enabled AI assistant that provides real-time answers from your custom knowledge base using Retrieval-Augmented Generation (RAG) technology.

## Features

- 🎙️ Real-time voice interaction using LiveKit
- 📚 Knowledge retrieval from PDF documents
- 🤖 GPT-4 powered responses
- 🔊 High-quality text-to-speech with Cartesia
- ⚡ FastAPI backend for RAG processing

## Architecture

```
User Voice Input → LiveKit → STT → GPT-4 → FastAPI (RAG) → GPT-4 → TTS → LiveKit → User
```

## Prerequisites

- Python 3.11+
- OpenAI API key
- LiveKit account
- Cartesia API key
- PDF document(s) for your knowledge base

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_key
   CARTESIA_API_KEY=your_cartesia_key
   LIVEKIT_URL=wss://your-project.livekit.cloud
   LIVEKIT_API_KEY=your_livekit_key
   LIVEKIT_API_SECRET=your_livekit_secret
   ```

5. **Prepare your knowledge base**
   - Place your PDF document in the `docs/` folder
   - Rename it to `NextGen.pdf` or update `PDF_PATH` in `fastapi_app.py`

## Running the Application

1. **Start the FastAPI RAG service** (in one terminal)
   ```bash
   uvicorn fastapi_app:app --reload
   ```

2. **Start the LiveKit agent** (in another terminal)
   ```bash
   python app.py start
   ```

3. **Connect to the room**
   ```bash
   livekit-cli join-room --url wss://your-project.livekit.cloud --api-key your_api_key --api-secret your_api_secret --room your_room_name
   ```

## Project Structure

```
.
├── app.py                # LiveKit voice agent
├── fastapi_app.py        # FastAPI RAG service
├── requirements.txt      # Python dependencies
├── docs/                 # Knowledge base documents
│   └── NextGen.pdf       # Example PDF knowledge base
└── .env                  # Environment variables
```

## Customization

- **Change the knowledge base**: Replace `NextGen.pdf` with your own document
- **Modify the agent personality**: Edit the `instructions` in `app.py`
- **Adjust RAG parameters**: Modify chunk size/overlap in `fastapi_app.py`

## Troubleshooting

If you encounter DLL errors on Windows:
1. Install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Reinstall ONNX Runtime:
   ```bash
   pip uninstall onnxruntime onnxruntime-gpu -y
   pip install onnxruntime==1.16.0
   ```

## License

MIT License

## Acknowledgments

- LiveKit for real-time communication
- OpenAI for LLM capabilities
- LangChain for RAG implementation
- Cartesia for high-quality TTS
