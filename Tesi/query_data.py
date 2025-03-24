import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.llms import Ollama


from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an AI tutor you are designed to help students with their questions, you must respond with clear resopnses
only with the givven context, do not exceed it, use italian to reply.


{context}

---

Answer the question based on the above context, respond in italian: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    return query_rag(query_text)



def query_rag(query_text: str):
    #print("ciao\n")
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)
    #print("mistral\n")
    model = Ollama(model="llama3.2")
    print("domanda inviata\n")
    response_text = model.invoke(prompt)
    print("risposta ottenuta\n")
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f" {response_text}\n\nSources: {sources}"
    print(formatted_response)
    return formatted_response


if __name__ == "__main__":
    main()
