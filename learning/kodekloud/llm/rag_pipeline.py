from langchain_text_splitters import RecursiveCharacterTextSplitter

# We want 500 characters per chunk
# We keep 50 characters from the previous chunk so sentences don't break
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Sample document text
large_document_string = """
LangChain is a robust framework for developing LLM-powered applications. It excels at managing context.

Retrieval-Augmented Generation (RAG) is a highly effective pattern. It injects relevant data right into the model prompt to minimize hallucinations.
"""

chunks = splitter.split_text(large_document_string)
print(f"Created {len(chunks)} chunks from the file.")
