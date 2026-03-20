# AIET Coaching Document Assistant

A document-based AI assistant for the AIET Coaching Website that enables users to ask questions about course materials, documents, and website content using natural language.

## Features

- **Multi-source Document Loading**: Supports PDF, DOCX, and web content loading
- **Intelligent Retrieval**: Uses vector similarity search with MMR (Maximal Marginal Relevance) for relevant document retrieval
- **AI-Powered Responses**: Leverages Google Gemini 2.5 Flash Lite model for accurate, context-aware answers
- **Vector Database Storage**: Utilizes Pinecone for efficient document embedding storage and retrieval
- **Interactive Chat Interface**: Command-line interface for real-time Q&A

## Installation

### Prerequisites

- Python 3.12 or higher
- Pinecone account and API key
- Google AI API key
- Mistral AI API key

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pdf
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or if using pyproject.toml
   pip install -e .
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=your_pinecone_index_name
   GOOGLE_API_KEY=your_google_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   ```

## Data Loading

Before running the assistant, load the documents into the vector database:

```bash
python load_data.py
```

This script will:
- Load content from `aiet.pdf`, `pgdca.docx`, and `https://aiet-classes.vercel.app/`
- Split documents into chunks of 500 characters with 50-character overlap
- Generate embeddings using Mistral AI
- Store embeddings in Pinecone under the "aiet_data" namespace

## Usage

Run the interactive chat assistant:

```bash
python main.py
```

The assistant will prompt you to ask questions. Enter your question and press Enter. Type `0` to exit.

### Example Interaction

```
Ask Question from the document: What are the admission requirements for PGDCA?
[Assistant provides answer based on retrieved documents]

Ask Question from the document: 0
```

## Project Structure

- `main.py`: Main chat application with retrieval-augmented generation
- `load_data.py`: Document loading and vector database population script
- `pyproject.toml`: Project configuration and dependencies
- `Chroma/`: Local Chroma database (if used for local storage)

## Dependencies

- `langchain`: Framework for building LLM applications
- `langchain-google-genai`: Google Gemini integration
- `langchain-mistralai`: Mistral AI embeddings
- `langchain-pinecone`: Pinecone vector store integration
- `pinecone`: Pinecone client
- `pymupdf`: PDF document loading
- `python-docx`: DOCX document loading
- `unstructured`: Document processing
- `dotenv`: Environment variable management

## Configuration

The system uses the following configuration:

- **Embedding Model**: Mistral Embed
- **LLM**: Google Gemini 2.5 Flash Lite
- **Vector Store**: Pinecone
- **Retriever**: MMR with k=3, fetch_k=10
- **Text Splitter**: RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Contact

For questions or support, please contact the AIET Coaching team.
