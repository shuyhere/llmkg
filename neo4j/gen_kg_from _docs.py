from langchain_community.graphs import Neo4jGraph
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from extract_kg import extract_and_store_graph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tqdm import tqdm
import os
import json


# Load the data
def load_data(input_file_path):
    _, file_extension = os.path.splitext(input_file_path)
    if file_extension == ".csv":
        return CSVLoader(input_file_path)
    elif file_extension == ".pdf":
        return UnstructuredPDFLoader(input_file_path,mode="elements")
    else:
        return DirectoryLoader(input_file_path)

def main(input_file_path, llm, graph,max_attempts=3):
    # Split the text into sentences
    loder = load_data(input_file_path)
    data = loder.load()
    text_splitter =CharacterTextSplitter.from_tiktoken_encoder(chunk_size=512, chunk_overlap=50)
    documents = text_splitter.split_documents(data)
    print(documents[0].page_content)
    # Load the checkpoint if it exists
    checkpoint_file = 'checkpoint.json'
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            start_index = json.load(f)['index']
    else:
        start_index = 0

    # Extract and store the knowledge graph
    for i, d in tqdm(enumerate(documents[start_index:]), total=len(documents), initial=start_index):
        for attempt in range(max_attempts):
            try:
                extract_and_store_graph(d,llm,graph)
                # Save the checkpoint
                with open(checkpoint_file, 'w') as f:
                    json.dump({'index': i+1}, f)
                break
            except Exception as e:
                print(f"Attempt {attempt+1} failed with error: {e}")
                if attempt+1 == max_attempts:
                    print("Max attempts reached. Stopping extraction.")
                    return

if __name__ == "__main__":

    # connect to the local graph client
    # also can use cloud: https://neo4j.com/cloud/platform/aura-graph-database/?ref=blog.langchain.dev

    url = "bolt://0.0.0.0:7687"
    username = "neo4j"
    password = "12345678"
    graph = Neo4jGraph(
        url=url,
        username=username,
        password=password
    )

    # optional
    # allowed_nodes = ["Person", "Company", "Location", "Event", "Movie", "Service", "Award"]
    # allowed_rels =[]

    # connect to your llm client
    load_dotenv()
    openai_api_base = os.getenv(" ")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.1, openai_api_base=openai_api_base,
                     openai_api_key=openai_api_key)


    input_file_path = "/Users/shuyang/Desktop/shucode/llmresearch/llmkg/test_data/专利分类.csv"

    main(input_file_path,llm,graph,max_attempts=3)





