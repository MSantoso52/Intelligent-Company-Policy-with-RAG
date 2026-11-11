# Intelligent-Company-Policy-with-RAG

https://github.com/user-attachments/assets/3cde7a6d-ba3a-47f2-b2d4-ce1616b831bb

End-to-end Building An Intelligent Company Policy with RAG 

## Project Overview
This project implements a fully localized, privacy-focused Retrieval-Augmented Generation (RAG) system for querying the corporate policy manual. Using `pdfplumber`, raw policy documents are parsed to cleanly preserve table structures as Markdown alongside standard prose chunks. Text chunks are converted into 768-dimensional vector embeddings using Ollama's `nomic-embed-text` model and stored natively in a PostgreSQL database utilizing the `pgvector` extension. When a query is submitted, the system performs a cosine distance similarity search ($<=>$) to retrieve the top matching context blocks from PostgreSQL. Finally, it feeds this retrieved context into a local `gemma2:2b` LLM via Ollama to generate exact, hallucination-free answers—such as annual leave breakdowns, plant shutdown schedules, and sick leave terms—strictly grounded in official company records

## Problem To Be Solved
  * Information Fragmentation: Employees waste time navigating lengthy, scattered corporate policy manuals to find precise answers on benefits, leave entitlements, and facility guidelines.

  * Table and Data Corruption: Naive text chunkers break apart structured tables and matrices in PDF documents, causing standard RAG systems to lose relational context and fail at numeric lookups.

  * Privacy and Security Risks: Relying on third-party cloud LLM APIs exposes sensitive internal company HR documents and proprietary employee policies to external data leaks.

  * LLM Hallucinations: General-purpose language models often guess or invent company policies rather than restricting answers strictly to official documentation.

## Prerequisites
* Install Ollama with free LLM model example `gemma2:2b` for reasoning and `nomic-embed-text` for generate vector embedding
  ```bash
  sudo pacman -S ollama

  ollama --version
  ollama version is 0.33.3

  ollama pull gemma2:2b
  ollama pull nomic-embed-text

  ollama ls
  NAME                       ID              SIZE      MODIFIED
  nomic-embed-text:latest    0a109f422b47    274 MB    3 weeks ago
  gemma2:2b                  8ccf136fdd52    1.6 GB    2 months ago  
  
  ```
* Install `PostgreSQL` with `pgvector` for database
  ```bash
  podman exec -it vector_db psql -U pgvector -d vectordb

  podman ps
  CONTAINER ID  IMAGE                             COMMAND     CREATED      STATUS            PORTS                   NAMES
  9bee8589eafb  docker.io/pgvector/pgvector:pg17  postgres    3 weeks ago  Up About an hour  0.0.0.0:5432->5432/tcp  vector_db 
  ```
* Install `streamlit` for web app
  ```bash
  sudo pacman -S python-streamlit

  streamlit version
  Streamlit, version 1.66.0
  ```

## Requirements

## Project Flow

## Pros And Cons
### Pros
 * Complete Data Privacy: Runs entirely on local infrastructure using Ollama and PostgreSQL, ensuring sensitive internal HR documents never leave company servers.
 * Table and Markdown Preservation: Utilizes specialized parsing to extract tables into structured Markdown chunks, preventing numeric and policy lookups from breaking.
 * Zero-Hallucination Grounding: Enforces strict prompt boundaries so the local LLM answers using only retrieved database context or explicitly declines to guess.
### Cons
 * Infrastructure Overhead: Demands local compute resources to host PostgreSQL with the pgvector extension and run local embedding and generation models. 
 * Maintenance Effort: Requires manual management of database updates, pipeline scripts, and local model versioning.
