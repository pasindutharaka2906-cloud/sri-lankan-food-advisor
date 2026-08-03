# Sri Lankan Food Advisor ðŸ›

## Project Overview
The **Sri Lankan Food Advisor** is an Agentic AI application built to solve a real-world problem: helping users navigate the diverse and highly spiced world of Sri Lankan cuisine. Whether a tourist looking for mild options, or a local craving traditional sweets, this app recommends the perfect dish using a RAG pipeline trained on authentic Sri Lankan culinary data.

## Agentic Design Patterns Used
This project implements the **Router**, **Tool-Use**, and **Orchestrator-Worker** (Researcher-Critic) patterns using LangGraph.
1. **Router**: The workflow starts by classifying the user's intent into taste profiles.
2. **Tool-Use**: The Researcher agent utilizes a ChromaDB vector search tool to retrieve knowledge.
3. **Self-Reflection / Critic**: The Critic agent reviews the Researcher's findings against the user's specific dietary or spice constraints before outputting the final recommendation.

## Agent-to-Agent Communication

`mermaid
sequenceDiagram
    participant User
    participant Router as Taste Router Agent
    participant Researcher as Culinary Researcher Agent
    participant DB as ChromaDB (RAG)
    participant Critic as Recommendation Critic Agent
    
    User->>Router: "I want a spicy chicken dish"
    Router->>Router: Classifies intent as SPICY_FOOD
    Router-->>Researcher: Forwards intent & query
    Researcher->>DB: Queries vector database for matching food
    DB-->>Researcher: Returns chunks (e.g. Kottu Roti, Chicken Curry)
    Researcher->>Researcher: Summarizes ingredients & flavor profile
    Researcher-->>Critic: Sends culinary summary
    Critic->>Critic: Audits for spice levels and allergies
    Critic-->>User: Generates formatted Markdown recommendation
`

## Model Selection Strategy

| Agent / Sub-task | Provider | Model | Justification |
| :--- | :--- | :--- | :--- |
| **Taste Router** | Groq | llama-3.1-8b-instant | Chosen for **very low latency** and zero cost. Intent classification is a simple task that doesn't need high reasoning. |
| **Culinary Researcher** | Groq | llama-3.3-70b-versatile | Chosen for its **large context window** to read multiple recipe chunks from RAG, and fast extraction capabilities. |
| **Recommendation Critic** | OpenRouter | google/gemini-2.5-flash | Higher reasoning quality justifies the use of a more capable model to format the final output, apply dietary constraints, and create an appetizing tone. |

## RAG Integration
- **Corpus**: 18+ domain-specific text documents containing Sri Lankan recipes, flavor profiles, and culinary history (located in data/).
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2 (Fast and runs locally).
- **Vector Store**: ChromaDB.
- **Chunking Strategy**: Recursive splitting with chunk_size=600 and chunk_overlap=100. This size optimally captures a full recipe description or flavor profile without breaking context.

## Deployment & Setup Instructions
1. Clone this repository.
2. Ensure you have Python 3.10+ installed.
3. Install dependencies: pip install -r requirements.txt
4. Run the app locally: streamlit run app.py

**To deploy on Streamlit Community Cloud:**
1. Connect your GitHub repository to [share.streamlit.io](https://share.streamlit.io).
2. Set the main file path to pp.py.
3. Under **Advanced Settings**, add the following to the **Secrets**:
   `	oml
   GROQ_API_KEY = "your_groq_key"
   OPENROUTER_API_KEY = "your_openrouter_key"
   `
4. Click Deploy.
