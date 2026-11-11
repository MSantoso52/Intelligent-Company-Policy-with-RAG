# Intelligent-Company-Policy-with-RAG
End-to-end Building An Intelligent Company Policy with RAG 

## Project Overview
This project implements a fully localized, privacy-focused Retrieval-Augmented Generation (RAG) system for querying the corporate policy manual. Using `pdfplumber`, raw policy documents are parsed to cleanly preserve table structures as Markdown alongside standard prose chunks. Text chunks are converted into 768-dimensional vector embeddings using Ollama's `nomic-embed-text` model and stored natively in a PostgreSQL database utilizing the `pgvector` extension. When a query is submitted, the system performs a cosine distance similarity search ($<=>$) to retrieve the top matching context blocks from PostgreSQL. Finally, it feeds this retrieved context into a local `gemma2:2b` LLM via Ollama to generate exact, hallucination-free answers—such as annual leave breakdowns, plant shutdown schedules, and sick leave terms—strictly grounded in official company records

## Problem To Be Solved
  * Information Fragmentation: Employees waste time navigating lengthy, scattered corporate policy manuals to find precise answers on benefits, leave entitlements, and facility guidelines.

  * Table and Data Corruption: Naive text chunkers break apart structured tables and matrices in PDF documents, causing standard RAG systems to lose relational context and fail at numeric lookups.

  * Privacy and Security Risks: Relying on third-party cloud LLM APIs exposes sensitive internal company HR documents and proprietary employee policies to external data leaks.

  * LLM Hallucinations: General-purpose language models often guess or invent company policies rather than restricting answers strictly to official documentation.

## Prerequisites

## Requirements

## Project Flow

## Pros And Cons
