# Qdrant Vector Database Examples

This directory contains examples demonstrating how to use Qdrant vector database with Python.

## Prerequisites

To run these examples, you need to have **Ollama installed** - Download and install from [ollama.ai](https://ollama.ai). Then, download and install the embedding model using:

```bash
ollama pull nomic-embed-text:latest
```

## Running the Examples

Once you have Ollama installed and the model downloaded, you can run:

```bash
python bearing_vectors_crud.py
```

This example demonstrates basic CRUD operations (Create, Read, Update, Delete) using Qdrant's in-memory vector database with Ollama embeddings.
