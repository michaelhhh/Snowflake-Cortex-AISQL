import streamlit as st
from snowflake.snowpark.context import get_active_session
import json

# 1. Get Session
session = get_active_session()

st.set_page_config(layout="wide")
st.title("🤖 Client Knowledge Base Assistant")
st.markdown("""
Welcome. This AI Assistant allows you to interact directly with our **Customer Service Audio** and **Company PDF Documents**. Select a resource below to start analyzing.
""")

# --- Sidebar: Navigation & Selection ---
with st.sidebar:
    st.header("🗂️ Data Source")
    source_type = st.radio("Select Content Type:", ["🎧 Customer Audio Calls", "📄 Company PDFs"])
    
    selected_file = None
    context_text = ""
    
    if source_type == "🎧 Customer Audio Calls":
        # Fetch list of processed audio files
        audio_files = session.sql("SELECT file_name FROM transcription_results").to_pandas()
        if not audio_files.empty:
            selected_file = st.selectbox("Select an Audio Record:", audio_files['FILE_NAME'])
        else:
            st.warning("No audio records found.")

    elif source_type == "📄 Company PDFs":
        # Fetch list of processed PDF files
        pdf_files = session.sql("SELECT file_name FROM parsed_documents_raw").to_pandas()
        if not pdf_files.empty:
            selected_file = st.selectbox("Select a Document:", pdf_files['FILE_NAME'])
        else:
            st.warning("No PDF documents found.")

# --- Main Content Area ---

if selected_file:
    st.divider()
    
    # 2. Retrieve Context based on selection
    if source_type == "🎧 Customer Audio Calls":
        # Get transcript and metadata
        df = session.sql(f"""
            SELECT translated_text, call_summary, sentiment_label, call_category 
            FROM transcription_results 
            WHERE file_name = '{selected_file}'
        """).to_pandas()
        
        if not df.empty:
            context_text = df.iloc[0]['TRANSLATED_TEXT']
            summary = df.iloc[0]['CALL_SUMMARY']
            sentiment = df.iloc[0]['SENTIMENT_LABEL']
            category = df.iloc[0]['CALL_CATEGORY']

            # Display "Executive Summary" Dashboard
            col1, col2, col3 = st.columns(3)
            col1.metric("Sentiment", sentiment, delta_color="inverse")
            col2.info(f"**Category:** {category}")
            col3.caption(f"**File:** {selected_file}")
            
            with st.expander("📄 View Full Summary"):
                st.write(summary)
            with st.expander("📝 View Full Transcript"):
                st.write(context_text)

    elif source_type == "📄 Company PDFs":
        # Get PDF text chunks 
        # FIX: Changed 'text' to 'content' to match the actual JSON structure
        df = session.sql(f"""
            SELECT 
                ARRAY_TO_STRING(ARRAY_AGG(page.value:content::VARCHAR), ' ') as full_text
            FROM parsed_documents_raw,
            LATERAL FLATTEN(input => parsed_result:pages) page
            WHERE file_name = '{selected_file}'
        """).to_pandas()
        
        if not df.empty:
            context_text = df.iloc[0]['FULL_TEXT']
            
            st.info(f"**Analyzing Document:** {selected_file}")
            
            # Simple check to see if we actually got text back this time
            if context_text:
                with st.expander("📖 View Document Content (Extracted Text)"):
                    st.write(context_text[:5000] + "...") 
            else:
                st.error("Text extraction returned empty. Please check the PDF content.")

    # 3. Chat Interface
    st.subheader("💬 Ask a Question")
    user_question = st.text_input("What would you like to know about this file?", placeholder="e.g., What was the customer's main complaint? or What is the refund policy?")

    if user_question and context_text:
        with st.spinner("Analyzing context..."):
            # Escape single quotes in text to prevent SQL errors
            clean_context = context_text.replace("'", "''")
            clean_question = user_question.replace("'", "''")
            
            # Construct Prompt
            prompt = f"""
            You are a helpful business assistant. Answer the question based ONLY on the context provided.
            
            Context: {clean_context}
            
            Question: {clean_question}
            
            Answer:
            """
            
            # Call Cortex AI (using specific model for best reasoning)
            query = f"SELECT AI_COMPLETE('claude-3-5-sonnet', '{prompt}') as response"
            result = session.sql(query).to_pandas()
            
            answer = result.iloc[0]['RESPONSE']
            
            # Display Result
            st.success("Analysis Result:")
            st.markdown(answer)

else:
    st.info("👈 Please select a file from the sidebar to begin.")
