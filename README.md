# ResearchMind 🔍

> An autonomous AI research assistant that combines web search, RAG (Retrieval-Augmented Generation), and multi-agent orchestration to produce high-quality research reports on any topic.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

- **Multi-Agent System**: Three specialized agents (Researcher, Writer, Critic) work together
- **Web Search**: Real-time information gathering using Tavily API
- **RAG Pipeline**: Semantic search with ChromaDB vector database
- **Local Embeddings**: Free, unlimited embeddings using Sentence Transformers
- **Fast LLM**: Groq integration with llama-3.3-70b-versatile for rapid inference
- **Quality Control**: Automated scoring and iterative improvement
- **LangGraph Orchestration**: Reliable workflow management

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│             │      │             │      │             │
│ RESEARCHER  │─────▶│   WRITER    │─────▶│   CRITIC    │
│             │      │             │      │             │
└─────┬───────┘      └──────▲──────┘      └──────┬──────┘
      │                     │                     │
      │                     │                     │
      │                     └─────────────────────┘
      │                        Feedback Loop       
      │                      (if score < 7/10)     
      ▼
┌─────────────────────────────────────────────────┐
│         ChromaDB Vector Store (RAG)             │
│     Chunks + Embeddings + Source Metadata       │
└─────────────────────────────────────────────────┘
```

### Agent Responsibilities

1. **Researcher Agent** 
   - Searches the web using Tavily
   - Cleans and structures findings
   - Ingests data into ChromaDB for RAG

2. **Writer Agent**
   - Retrieves relevant context via RAG
   - Generates comprehensive markdown reports
   - Incorporates feedback from Critic

3. **Critic Agent**
   - Scores reports on 5 dimensions (accuracy, citations, structure, depth, clarity)
   - Provides detailed feedback
   - Triggers rewrites if score < 7/10

## 📋 Prerequisites

- **Python 3.10+** (tested on 3.13.5)
- **API Keys**:
  - [Groq API Key](https://console.groq.com/) (free tier available)
  - [Tavily API Key](https://tavily.com/) (free tier: 1000 searches/month)
  - [LangSmith API Key](https://smith.langchain.com/) (optional, for tracing)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/vishnu-0011/ResearchMind.git
cd ResearchMind
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- `langchain` - LLM framework
- `langgraph` - Multi-agent orchestration
- `langchain-groq` - Groq LLM integration
- `tavily-python` - Web search
- `chromadb` - Vector database
- `sentence-transformers` - Local embeddings
- `llama-index` - Document processing
- `gradio` - UI framework (planned)
- `python-dotenv` - Environment management

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: Groq API Key (get from https://console.groq.com/)
GROQ_API_KEY=your_groq_api_key_here

# Required: Tavily API Key (get from https://tavily.com/)
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: LangSmith for tracing and monitoring
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=researchmind
LANGSMITH_TRACING=true
```

**Getting API Keys:**

1. **Groq API Key**:
   - Visit https://console.groq.com/
   - Sign up for free account
   - Navigate to API Keys section
   - Generate new key

2. **Tavily API Key**:
   - Visit https://tavily.com/
   - Sign up (free tier: 1000 searches/month)
   - Copy API key from dashboard

3. **LangSmith** (Optional):
   - Visit https://smith.langchain.com/
   - Sign up for free
   - Create project and get API key

### 5. Run the Project

**Basic Usage:**

```bash
python main.py
```

This will run a sample research on "Artificial Intelligence in Healthcare".

**Custom Topic:**

Edit `main.py` and change the topic:

```python
if __name__ == "__main__":
    run("Your Custom Research Topic Here")
```

Or create a custom script:

```python
from dotenv import load_dotenv
load_dotenv()

from graph.builder import build_graph
from agents.base import make_empty_state

def research(topic: str):
    graph = build_graph()
    state = make_empty_state(topic)
    result = graph.invoke(state)
    
    print("\n── Final Report ──")
    print(result["final_report"])
    
    return result

if __name__ == "__main__":
    result = research("Quantum Computing Applications")
    
    # Save report to file
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(result["final_report"])
```

## 📁 Project Structure

```
ResearchMind/
├── agents/              # Agent implementations
│   ├── researcher.py    # Web search + RAG ingestion
│   ├── writer.py        # Report generation with LLM
│   ├── critic.py        # Quality scoring & feedback
│   └── base.py          # Shared utilities
├── graph/               # LangGraph orchestration
│   ├── state.py         # State management (TypedDict)
│   ├── builder.py       # Pipeline assembly
│   └── router.py        # Conditional routing logic
├── rag/                 # RAG components
│   ├── chunker.py       # Text splitting (512 chars)
│   ├── embedder.py      # Sentence Transformers embeddings
│   └── vectorstore.py   # ChromaDB interface
├── tools/               # Utility functions
│   ├── search.py        # Tavily web search
│   ├── fetcher.py       # Content extraction & cleaning
│   ├── ingestor.py      # Batch ingestion pipeline
│   └── retriever.py     # RAG retrieval
├── config/              # Configuration
│   ├── settings.py      # App settings
│   └── prompts.py       # Agent system prompts
├── tests/               # Test suite
│   ├── test_vectorstore.py  # Vector store tests (18 tests)
│   ├── test_rag.py      # RAG pipeline tests
│   └── test_search.py   # Search integration tests
├── evals/               # Evaluation framework
│   ├── benchmark.py     # Performance benchmarks
│   └── metrics.py       # Quality metrics
├── ui/                  # User interface (planned)
│   └── app.py           # Gradio UI
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── README.md            # This file
├── PROJECT_STORY.md     # Complete project narrative
└── VECTORSTORE_ANALYSIS.md  # Security analysis
```

## 🧪 Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
# Vector store tests (18 tests)
pytest tests/test_vectorstore.py -v

# RAG pipeline tests
pytest tests/test_rag.py -v

# Search integration tests
pytest tests/test_search.py -v
```

### Test Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

View coverage report at `htmlcov/index.html`.

## 📊 Example Output

```
🔍 Researcher searching for: Artificial Intelligence in Healthcare
   Found 5 results
   [1] How AI Is Transforming Healthcare...
   [2] Machine Learning in Medical Diagnosis...
   [3] The Future of AI-Powered Medicine...
   [4] Deep Learning for Drug Discovery...
   [5] AI Ethics in Healthcare Systems...
✅ Researcher done — 5 findings collected

📥 Ingesting 5 findings into vector store...
   → 12 chunks from: How AI Is Transforming Healthcare...
   → 15 chunks from: Machine Learning in Medical Diagnosis...
   → 10 chunks from: The Future of AI-Powered Medicine...
   → 18 chunks from: Deep Learning for Drug Discovery...
   → 13 chunks from: AI Ethics in Healthcare Systems...
   Embedding 68 chunks...
   Stored 68 chunks in ChromaDB
✅ Ingestion complete — 68 chunks ready for retrieval

✍️  Writer drafting report (attempt 1)...
   Retrieving relevant chunks from vector store...
✅ Writer done — 4521 characters written

=> Critic reviewing draft...
   Score: 8/10
   Feedback: The report demonstrates strong structure and comprehensive coverage...

── Sources Used ──
  [1] https://example.com/ai-healthcare
  [2] https://example.com/ml-diagnosis
  [3] https://example.com/ai-future
  [4] https://example.com/drug-discovery
  [5] https://example.com/ai-ethics

── Critic Score: 8/10 ──
Feedback: The report demonstrates strong structure and comprehensive coverage...

── Final Report ──
# Artificial Intelligence in Healthcare

## Executive Summary
Artificial intelligence is revolutionizing healthcare delivery...

[Full markdown report follows]
```

## ⚙️ Configuration

### Adjusting Agent Behavior

Edit `config/prompts.py` to customize agent prompts:

```python
WRITER_PROMPT = """
You are a research report writer.
[Customize instructions here]
"""

CRITIC_PROMPT = """
You are a quality control critic.
[Customize scoring criteria]
"""
```

### Changing LLM Models

Edit agent files to use different models:

```python
# In agents/writer.py or agents/critic.py
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Change model here
    temperature=0.3,                   # Adjust creativity
    api_key=os.environ["GROQ_API_KEY"]
)
```

**Available Groq Models:**
- `llama-3.3-70b-versatile` (recommended, balanced)
- `llama-3.1-70b-versatile` (fast)
- `mixtral-8x7b-32768` (longer context)

### Adjusting RAG Parameters

Edit `rag/chunker.py`:

```python
def chunk_text(text: str, chunk_size: int = 512, chunk_overlap: int = 50):
    # Increase chunk_size for longer chunks
    # Increase chunk_overlap for more context preservation
```

Edit `tools/retriever.py`:

```python
def retrieve(query: str, n_results: int = 5):
    # Increase n_results to retrieve more context
```

### Quality Threshold

Edit `graph/router.py` to change retry threshold:

```python
def should_retry(state: ResearchState) -> str:
    score = state.get("score", 0)
    
    # Change threshold (default: 7)
    if score >= 7:  # Increase for stricter quality
        return "done"
    else:
        return "retry"
```

## ⚠️ Known Issues

**CRITICAL**: The vectorstore module has security vulnerabilities that need fixing before production use. See `VECTORSTORE_ANALYSIS.md` for details.

### Issue #1: ID Collision Vulnerability (CRITICAL)
- **Problem**: Hash-based ID generation causes ~5-10% data loss
- **Impact**: Chunks silently overwritten
- **Status**: ⚠️ Unfixed
- **Workaround**: Use small batch sizes (<100 chunks)

### Issue #2: Empty Collection Bug (HIGH)
- **Problem**: Crashes when querying empty collections
- **Impact**: Application crashes
- **Status**: ⚠️ Unfixed
- **Workaround**: Ensure data is ingested before querying

### Issue #3: No Input Validation (HIGH)
- **Problem**: None values accepted without validation
- **Impact**: Potential data corruption
- **Status**: ⚠️ Unfixed
- **Workaround**: Validate inputs in calling code

**Fix Status**: Comprehensive test suite written (18 tests). Fixes are documented in `VECTORSTORE_ANALYSIS.md` and ready for implementation.

## 🐛 Troubleshooting

### "ModuleNotFoundError" when running

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

### "API key not found" error

**Solution**: Check `.env` file exists and contains valid API keys:
```bash
cat .env  # Linux/macOS
type .env  # Windows
```

### "ChromaDB connection failed"

**Solution**: ChromaDB runs in-memory by default. If issues persist:
```python
# In rag/vectorstore.py, try persistent storage:
_client = chromadb.Client(Settings(
    persist_directory="./chroma_db",
    anonymized_telemetry=False
))
```

### Slow embeddings

**Solution**: First run downloads the model (~80MB). Subsequent runs use cached model.

### "Rate limit exceeded" from Tavily

**Solution**: Free tier has 1000 searches/month. Check usage at https://tavily.com/

### LangSmith tracing not working

**Solution**: LangSmith is optional. Set `LANGSMITH_TRACING=false` to disable, or verify API key.

## 📚 Documentation

- **[PROJECT_STORY.md](PROJECT_STORY.md)** - Complete project narrative with development timeline
- **[VECTORSTORE_ANALYSIS.md](VECTORSTORE_ANALYSIS.md)** - Security analysis and test report
- **[CLAUDE.md](CLAUDE.md)** - Ruflo configuration and coordination patterns

## 🔒 Security

This project has undergone security analysis using ruflo swarm coordination. Key findings:

- ✅ 18 comprehensive tests written
- ✅ 16 tests passing
- ⚠️ 2 critical vulnerabilities identified (see VECTORSTORE_ANALYSIS.md)
- ⚠️ Fixes documented and ready for implementation

**For production use**: Implement fixes from `VECTORSTORE_ANALYSIS.md` before deployment.

## 🤝 Contributing

Contributions are welcome! Priority areas:

1. **Fix critical vulnerabilities** (see VECTORSTORE_ANALYSIS.md)
2. **Implement Gradio UI** (ui/app.py is currently empty)
3. **Add more evaluation metrics** (evals/)
4. **Improve test coverage**
5. **Add support for more LLM providers**

### Development Setup

```bash
# Fork and clone the repo
git clone https://github.com/YOUR_USERNAME/ResearchMind.git
cd ResearchMind

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
pytest tests/ -v

# Commit and push
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** - LLM framework
- **LangGraph** - Multi-agent orchestration
- **Groq** - Fast LLM inference
- **Tavily** - Web search API
- **ChromaDB** - Vector database
- **Sentence Transformers** - Local embeddings
- **Ruflo** - Security analysis and coordination

## 📧 Contact

**Author**: vishnu-0011  
**Repository**: https://github.com/vishnu-0011/ResearchMind  
**Issues**: https://github.com/vishnu-0011/ResearchMind/issues

---

**Built with ❤️ using LangGraph, Groq, and Ruflo coordination**
