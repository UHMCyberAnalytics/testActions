import anthropic
import chromadb
import json

# Chroma Client Setup
client = chromadb.PersistentClient(path=r"C:\Users\Ryder\Documents\GitHub\testActions\something")
collection = client.get_or_create_collection(name="my_collection")

# Anthropic Client Setup
anthropic_client = anthropic.Anthropic(
    api_key="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"
)

# Function to query Chroma and get relevant documents
def query_chroma(query, collection):
    results = collection.query(query_texts=[query], n_results=3)  # Get top 3 results
    return results['documents']

# Function to ask Claude using context from Chroma
def ask_claude(query, documents):
    # Ensure all documents are strings
    context = '\n'.join([str(doc) for doc in documents])

    # Generate answer using Claude
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ]
    )
    return message['choices'][0]['message']['content']

# Main process to query Chroma and ask Claude
def main(query):
    # Get the relevant documents from Chroma
    relevant_documents = query_chroma(query, collection)

    # Ask Claude with the context and query
    response = ask_claude(query, relevant_documents)
    print("Claude's response:", response)

# Example query
query = "Tell me about the properties of water."
main(query)
