# Spoiler-Free Reading Companion 
### **Open ILab Project** | *Intelligent, Context-Aware Book Summaries*

This repository hosts the development of a new reading application designed to bring the reading experience to a new level. 
Using a **RAG (Retrieval-Augmented Generation)** chatbot, the app provides summaries and character recaps that are dynamically gated based on the user's current reading progress, avoiding spoilers.

## Preliminary Project Structure

```bash
├── reference_code/        # Python & Notebook files from previous IR iterations
├── backend/
│   ├── data/              # Raw book data and processed text
│   ├── inverted_index/    # Scripts for building the search index
│   ├── preprocessing/     # Functions for text cleaning & tokenization
│   ├── retrieval/         # Logic for performing information retrieval
│   └── chatbot_rag/       # The core RAG implementation (LLM + Context)
└── frontend/
    ├── figma_prototypes/  # Design assets and UI/UX flows
    ├── html_files/        # Structure for the web-based interface
    └── css_javascript/    # Styling and interactive components
