# TDS Virtual TA

A virtual teaching assistant built for the "Tools in Data Science" course of the IIT Madras Online BSc Degree.  
It answers student questions by searching through the course content and Discourse forum discussions.

---

## Project Summary

This tool uses **FAISS** for vector similarity search and **OpenAI GPT** for generating answers based on relevant chunks from:

- `discourse_data.json`: Posts from the TDS Discourse forum
- `tds_content.json`: Official course content of Tools in Data Science

---

## How It Works

1. **Data Ingestion**: Course and Discourse content are loaded.
2. **Embedding**: Content is broken into chunks and embedded using Sentence Transformers.
3. **Storage**: Embeddings are stored in a FAISS index and metadata is stored in JSON.
4. **API**: User questions are matched against stored data, and relevant chunks are passed to OpenAI to generate a response.

