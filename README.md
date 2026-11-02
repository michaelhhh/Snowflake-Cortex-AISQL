# Snowflake Cortex AISQL: Multimodal Customer Service Intelligence

An end-to-end analytics pipeline that turns unstructured customer-service data (call recordings, PDF policy documents and chat logs) into structured insights using Snowflake Cortex AI functions, with a Streamlit chat front end.

Built on the sample data from Snowflake's public quickstart, *Extracting Insights from Multimodal Customer Data*. No external API keys are needed: everything runs inside Snowflake.

## What it does

- **Audio:** transcribes calls with speaker separation (`AI_TRANSCRIBE`), translates transcripts to English (`AI_TRANSLATE`), scores sentiment (`AI_SENTIMENT`), classifies each call into business issues such as fraud or technical errors (`AI_CLASSIFY`), and summarises it (`AI_COMPLETE`).
- **Documents:** parses PDF policy documents with layout preserved and split by page (`AI_PARSE_DOCUMENT`), ready for retrieval.
- **Chat logs:** extracts structured fields such as issue, product, error message and urgency (`AI_EXTRACT`).
- **Cross-channel check:** asks an LLM to compare each support ticket with its chat log and return whether they are aligned, with reasoning as JSON.
- **Assistant:** a Streamlit app that lets a business user ask questions about the transcripts and documents in plain English.

## Files

| File | What it is |
| --- | --- |
| `env_setup.sql` | Creates the database, stages (pointing at the quickstart's public sample data) and tables. |
| `AISQL.ipynb.ipynb` | The pipeline notebook: ingestion, Cortex function calls and the analytical tables. |
| `streamlit_app.py` | The chat front end, run as Streamlit in Snowflake. |

## Running it

1. Run `env_setup.sql` in a Snowflake account with Cortex enabled (the script enables cross-region inference).
2. Import and run `AISQL.ipynb.ipynb` as a Snowflake Notebook.
3. Create a Streamlit in Snowflake app from `streamlit_app.py`.

## Cortex functions used

| Function | Input | Output |
| --- | --- | --- |
| `AI_TRANSCRIBE` | Audio file | Segments with speakers |
| `AI_PARSE_DOCUMENT` | PDF | Layout-aware text by page |
| `AI_TRANSLATE` | Transcript | English text |
| `AI_SENTIMENT` | Transcript or chat | Sentiment |
| `AI_CLASSIFY` | Transcript or chat | Category label |
| `AI_EXTRACT` | Chat log | Structured fields (JSON) |
| `AI_COMPLETE` | Transcript or ticket | Summary or reasoning (JSON) |
