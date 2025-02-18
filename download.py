from anthropic import Anthropic
import chromadb

class RAGWithClaude:
    def __init__(self, api_key, chroma_path):
        self.client = Anthropic(api_key=api_key)
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")

    def query(self, user_question, n_results=5):
        # Query Chroma with valid include parameters
        results = self.collection.query(
            query_texts=[user_question],
            n_results=n_results,
            include=['documents', 'metadatas']
        )

        context = "\n\n".join(results['documents'][0])

        message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Here is some relevant context:
                    
{context}

Based on the context above, please answer this question: {user_question}

If the context doesn't contain enough information to answer the question fully, 
please say so and answer with what you know from the context only."""
                }
            ]
        )

        response_content = message.content
        text_response = response_content[0].text if hasattr(response_content[0], 'text') else response_content
        return text_response

# Usage
rag = RAGWithClaude(
    api_key="",
    chroma_path=r"C:\Users\Ryder\Documents\GitHub\testActions\something"
)

response = rag.query("What is the most recent article you have access to?")
print("\nClaude's Response:")
print(response)