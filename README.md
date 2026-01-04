# 🤖 Snowflake-Cortex-AISQL: Multimodal Customer Service Intelligence

A unified analytics platform that leverages **Snowflake Cortex AI** to extract actionable insights from unstructured customer service data. This project demonstrates an end-to-end pipeline for processing audio calls, PDF documents, and chat logs using serverless LLM and ML functions directly within Snowflake.

![Snowflake Cortex Architecture Placeholder](https://via.placeholder.com/800x400?text=Snowflake+Cortex+AI+Architecture)

## 📋 Overview

This repository contains a full-stack AI solution designed to help businesses understand their customer interactions. It ingests raw files (Audio, PDFs, Logs) and transforms them into structured insights using Snowflake's native AI primitives—without requiring external API keys or complex infrastructure.

### Key Capabilities

* **🎧 Audio Intelligence:**
    * Automated transcription with speaker diarization (separating distinct speakers).
    * Sentiment analysis and zero-shot classification of call topics.
    * Automated summarization using **Claude 3.5 Sonnet**.
* **📄 Document Intelligence (RAG-Ready):**
    * Ingestion and layout-aware parsing of PDF documents (policies, manuals).
    * Chunking logic to prepare documents for downstream retrieval.
* **✅ Cross-Channel Validation:**
    * Compares Support Tickets vs. Chat Logs to identify inconsistencies using LLMs.
    * Validates human-reported sentiment against AI-detected sentiment.
* **💬 Interactive Assistant:**
    * A **Streamlit** application that allows users to "chat" with their data (Audio transcripts and PDFs) using natural language.

---

## 📂 Repository Structure
* **extracting_insights.ipynb:**
    * The primary ELT (Extract, Load, Transform) pipeline. This Jupyter Notebook runs inside Snowflake to ingest raw data, execute Cortex functions (AI_TRANSCRIBE, AI_PARSE_DOCUMENT), and populate the analytical tables.

* **streamlit_app.py:**
    * The user-facing application code. It connects to the processed tables and provides a chat interface for business users.
 
---

Based on the SQL code in the provided notebook, here is a summary of all the **Snowflake Cortex AI functions** used, organized by their role in the pipeline:

### 1. Ingestion & Transformation

* **`AI_TRANSCRIBE(file_reference, options)`**
* **Purpose:** Converts audio files into text.
* **Usage in Notebook:** It processes files from the `@MULTIMODAL...` stage.
* **Key Parameter:** `{'timestamp_granularity': 'speaker'}` was used to enable **diarization**, distinguishing between different speakers in the audio.


* **`AI_PARSE_DOCUMENT(file_reference, options)`**
* **Purpose:** Extracts text and structural information from PDF documents.
* **Usage in Notebook:** Ingests company policy documents.
* **Key Parameter:** `{'mode': 'LAYOUT', 'page_split': TRUE}` was used to preserve the visual layout (headers, tables) and split the output by page for better searchability.


* **`AI_TRANSLATE(text, source_lang, target_lang)`**
* **Purpose:** Translates text into a standard language for analysis.
* **Usage in Notebook:** Converts the stitched audio transcripts into English (`'en'`). The source language was set to `''` to let Cortex auto-detect it.



### 2. Analysis & Classification

* **`AI_SENTIMENT(text)`**
* **Purpose:** Detects the emotional tone of the text.
* **Usage in Notebook:** Applied to both audio transcripts and chat logs to label them as Positive, Negative, Neutral, or Mixed.


* **`AI_CLASSIFY(text, categories)`**
* **Purpose:** Categorizes text into a predefined list of labels without needing a custom trained model (Zero-Shot Classification).
* **Usage in Notebook:** It mapped calls to specific business issues like *"Fraud & Security Issues"* or *"Technical & System Errors"* based on provided descriptions.



### 3. Generative & Reasoning (LLM)

* **`AI_COMPLETE(model, prompt)`**
* **Purpose:** Calls a Large Language Model to generate text or perform complex reasoning.
* **Usage in Notebook:** Used in two distinct ways:
1. **Summarization:** Asked the model (`claude-sonnet-4-5`) to "Summarize this call in 50 words".
2. **Logic & Alignment:** Asked the model to compare a Support Ticket vs. a Chat Log to see if they were "aligned" or "misaligned," returning a JSON reasoning object.




* **`AI_EXTRACT(text, schema)`**
* **Purpose:** Extracts specific structured fields from unstructured text.
* **Usage in Notebook:** Pulled specific data points from chat logs, such as `issue_description`, `product_name`, `error_message`, and `urgency_level`.



### Summary Table

| Function | Type | Input Data | Output |
| --- | --- | --- | --- |
| **`AI_TRANSCRIBE`** | Audio | Audio File | JSON (Segments + Speakers) |
| **`AI_PARSE_DOCUMENT`** | Document | PDF File | JSON (Layout + Pages) |
| **`AI_TRANSLATE`** | Text | Transcript | English Text String |
| **`AI_SENTIMENT`** | ML | Transcript/Chat | Sentiment Score/Label |
| **`AI_CLASSIFY`** | ML | Transcript/Chat | Category Label |
| **`AI_EXTRACT`** | LLM | Chat Log | JSON (Structured Fields) |
| **`AI_COMPLETE`** | LLM | Transcript/Ticket | Summary or Reasoning JSON |
