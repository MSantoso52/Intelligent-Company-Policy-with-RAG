import streamlit as st
import ollama
import psycopg2

# Configuration
DB_CONFIG = {
    "dbname": "company_policy",
    "user": "pgvector",
    "password": "pgvectorpasswd",
    "host": "localhost",
    "port": "5432"
}
EMBEDDING_MODEL = "nomic-embed-text"

# Page layout setup
st.set_page_config(page_title="Company Policy RAG Assistant", page_icon="💬", layout="wide")
st.title("💬 Company Policy Assistant")
st.caption("Ask questions about company policies using local Ollama LLMs and PostgreSQL pgvector.")

# Function to dynamically list installed Ollama models
@st.cache_data(ttl=60)
def get_available_models() -> list[str]:
    try:
        models_info = ollama.list()
        # Handle dict or object response from ollama library
        if isinstance(models_info, dict) and "models" in models_info:
            return [m["model"] for m in models_info["models"]]
        elif hasattr(models_info, "models"):
            return [m.model for m in models_info.models]
        return ["gemma2:2b"]
    except Exception:
        # Fallback default if Ollama service list check fails
        return ["gemma2:2b"]

# Function to perform vector similarity search
def semantic_search(query_text: str, top_k: int = 10) -> list[str]:
    """ Convert query to vector and search PostgreSQL + pgvector """
    try:
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query_text)
        query_vector = response["embedding"]

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # Execute vector similarity search using cosine distance (<=>)
        cur.execute(
            """
            SELECT content
            FROM policy
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (str(query_vector), top_k)
        )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [row[0] for row in rows]
    except Exception as e:
        st.error(f"Database/Embedding error: {str(e)}")
        return []

# RAG query execution function
def ask_rag(user_query: str, model_name: str, top_k: int):
    """ Executes Retrieval -> Augmentation -> Generation """
    retrieved_chunks = semantic_search(user_query, top_k=top_k)

    if not retrieved_chunks:
        return "I cannot find any matching records in the database.", []

    context_text = "\n\n".join([f" - {chunk}" for chunk in retrieved_chunks])

    augmented_prompt = f"""
    You are a precise technical assistant. Answer the user's question accurately using ONLY the provided context below. 
    If the answer cannot be found in the context, state "I cannot find that information in the provided records." 
    Do not make up facts.

    [Retrieved Database Context]:
    {context_text}

    User Question: {user_query}  
    """

    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": augmented_prompt}]
    )

    return response["message"]["content"], retrieved_chunks

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model Dropdown Menu
    available_models = get_available_models()
    selected_model = st.selectbox(
        "Select LLM Model",
        options=available_models,
        index=0 if "gemma2:2b" not in available_models else available_models.index("gemma2:2b")
    )
    
    # Top-K retriever slider
    top_k_val = st.slider("Retrieved Context Chunks (Top-K)", min_value=1, max_value=15, value=10)
    
    # Clear Chat History Button
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Session State Initialization for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "context" in message and message["context"]:
            with st.expander("📄 View Retrieved Context"):
                for idx, chunk in enumerate(message["context"], 1):
                    st.markdown(f"**Chunk {idx}:**\n{chunk}")

# Chat Input & Processing Loop
if user_input := st.chat_input("Ask a question about company policies..."):
    # Render user query
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Render assistant response with spinner
    with st.chat_message("assistant"):
        with st.spinner("Searching records and generating response..."):
            answer, chunks = ask_rag(user_input, model_name=selected_model, top_k=top_k_val)
            st.markdown(answer)
            
            if chunks:
                with st.expander("📄 View Retrieved Context"):
                    for idx, chunk in enumerate(chunks, 1):
                        st.markdown(f"**Chunk {idx}:**\n{chunk}")

    # Append response to session history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "context": chunks
    })
