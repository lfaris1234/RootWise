import os
import gradio as gr
import shutil
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.nvidia import NVIDIAEmbedding
from llama_index.llms.nvidia import NVIDIA
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings
from openai import OpenAI

# Initialize global variables
query_engine = None
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)
rag_data = []  # Placeholder for dynamically updated RAG data, i think i want it written to a file actually
rag_store = './system_data'

def initialize_rag(file_path):
    global query_engine, rag_store

    # Step 1: Check if system_data directory exists
    if not os.path.exists(rag_store):
        return "Error: system_data directory not found."

    try:
        # Step 2: Load documents from the directory
        documents = []
        for file_name in os.listdir(rag_store):
            if file_name.endswith(".txt"):
                file_path = os.path.join(rag_store, file_name)
                documents.extend(SimpleDirectoryReader(input_files=[file_path]).load_data())

        # Step 3: If no documents are found
        if not documents:
            return "Error: No .txt files found in system_data."

        # Step 4: Attempt to load the index from the storage context
        vector_store = MilvusVectorStore(uri="http://your_gpu_ip:19530", dim=1536, overwrite=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        query_engine = index.as_query_engine()
        
        return "Query engine initialized successfully."

    except FileNotFoundError as fnf_error:
        return f"FileNotFoundError: {str(fnf_error)}"
    
    except Exception as e:
        # General Exception block with debug context
        print(f"\n\n {e} \n\n")
        return f"Failed to initialize query engine. Exception: {str(e)}"

# Function to handle file inputs for RAG
def get_files_from_input(file_objs):
    if not file_objs:
        return []
    if [file_obj.name for file_obj in file_objs] == []:
        return [file_objs.name]
    else:
        return [file_obj.name for file_obj in file_objs]

# PDF Helper function
def create_pdf(filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.output(filename)

# Function to load documents and create the index
def load_documents(file_objs):
    global index, query_engine, rag_store 

    try:
        if not file_objs:
            return "No files selected."
        
        file_paths = get_files_from_input(file_objs)

        documents = []
        print(f" \n\n file paths: {file_paths} \n\n")
        for file_path in file_paths:
            documents.extend(SimpleDirectoryReader(input_files=[file_path]).load_data())

        # Making a copy in ./system_data
            file_name = os.path.basename(file_path)
            destination_f = f"{os.path.dirname(rag_store)}/{rag_store}/{file_name}"
            if file_name.endswith(".pdf"):
                create_pdf(destination_f)
                shutil.copy(file_path, destination_f)
            if file_name.endswith(".txt"):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                shutil.copyfile(file_path, destination_f)

        if not documents:
            return f"No documents found in the selected files."

        vector_store = MilvusVectorStore(uri="http://your_gpu_ip:19530", dim=1536, overwrite=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        query_engine = index.as_query_engine()
        return "Documents loaded successfully!"
    
    except Exception as e:
        return f"Error loading documents: {str(e)}"
    

# Add user inputs to the RAG database
def add_to_rag(season, ingredients, restrictions):
    global rag_data, query_engine
    file_path = 'system_data/user_rag.txt'

    new_entry = {
        "season": season,
        "ingredients": ingredients.split(','),
        "restrictions": restrictions.split(',')
    }
    rag_data.append(new_entry) # rag_data may become obsolete, im storing it in a file
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Update file information
    with open(file_path, 'a') as file:
        file.write(
        f"Season: {new_entry['season']}, Ingredients: {', '.join(new_entry['ingredients'])}, Dietary Restrictions: {', '.join(new_entry['restrictions'])}"
    )

    # Update database
    documents = []
    documents.extend(SimpleDirectoryReader(input_files=[file_path]).load_data())

    if not documents:
            return f"No new data here." 
    
    try:
        vector_store = MilvusVectorStore(uri="http://your_gpu_ip:19530", dim=1536, overwrite=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        query_engine = index.as_query_engine()

        return "Input added to RAG database!"
    
    except Exception as e:
        return f"Error updating rag: {str(e)}"


# Chat function for interactive conversation, using nv-embedqa-e5-v5
def embed_query(text):
    response = client.embeddings.create(
        input=[text],
        model="nvidia/nv-embedqa-e5-v5",
        encoding_format="float",
        extra_body={"input_type": "query", "truncate": "NONE"}
    )
    return response.data[0].embedding

def chat(message, history):
    global query_engine

    embedding = embed_query(message)

    if query_engine is None:
        return history + [(message, "I don't have any documents to reference, but I'll try my best.")]

    try:
        response = query_engine.query(message)
        return history + [(message, response)]
    except Exception as e:
        return history + [(message, f"An error occurred: {str(e)}")]

# Function to stream responses 
def stream_response(message, history) :
    global query_engine, rag_store

    if query_engine is None:
        yield history + [(message, "Please load documents first.")] 
        return
    try:
        response = query_engine.query("You are a helpful, friendly farmers market employee that is responding to the user: \n" + message + 
                                " \n Your eventual goal is to offer the user the following: \n" +
                                " \n - **Recipes**: Cook time. Community notes and tips. \n" +
                                " \n DO NOT RECOMMEND RECIPES THAT INVOLVE FOODS THAT THE USER IS ALLERGIC TO!! \n\n" +
                                " \n - **Food Scrap Recommendations**: Composting tips. Freezing methods for future use (e.g., stir-fry mix, chopped fruit). Zero-waste cooking ideas (e.g., carrot top pesto).\n" +
                                " \n But you have these additional features: \n" +
                                " \n - Food donation resources, including Food Not Bombs drop-off locations. \n" +
                                " \n Food lifespan and storage tips (e.g., using paper towels to extend the life of greens).\n"
                                " Food as Medicine insights: Health benefits (e.g., turmeric for inflammation). Spiritual properties (e.g., calming effects of certain herbs).\n" +
                                " \n\n Be sure to remember to be brief, that the user is always right, and sustainability is extremely important.")  
        partial_response = ""
        partial_response += str(response)
        yield history + [(message, partial_response)]

    except Exception as e:
        yield history + [(message, f"Error processing query: {str(e)}")]

def show_pdf():
    file_path = "./about_us.pdf"
    return gr.update(visible=True), gr.update(visible=True)

def hide_pdf():
    return gr.update(visible=False), gr.update(visible=False)

# Gradio app setup
with gr.Blocks(css=".gradio-container {background-color: #8A9A5B;} h1 {text-align: center; font-family: 'Georgia', cursive, sans-serif;}") as demo:

    with gr.Row():
        gr.Image( type="filepath", value="./frontpage.png", visible=True)

    with gr.Row():
        with gr.Column():
            season_input = gr.Textbox(label="Season")
            ingredients_input = gr.Textbox(label="Ingredients (comma-separated)")
            restrictions_input = gr.Textbox(label="Dietary Restrictions (comma-separated)")

            add_rag_button = gr.Button("Add to RAG Database")
            add_rag_button.click(add_to_rag, inputs=[season_input, ingredients_input, restrictions_input], outputs=gr.Textbox(label="RAG Status"))

        with gr.Column():
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Enter your question", interactive=True)
            # A 'clear' button to clear the chat history
            clear = gr.Button("Clear")
            
            msg.submit(stream_response, inputs=[msg, chatbot], outputs=[chatbot], queue=True)
            msg.submit(lambda: "", outputs=[msg])
            clear.click(lambda: None, None, chatbot, queue=False)

    with gr.Column():
        file_upload = gr.File(label="Upload Documents", file_types=[".txt", ".pdf"])
        load_button = gr.Button("Load Documents")
        load_button.click(load_documents, inputs=[file_upload], outputs=gr.Textbox(label="Status"))

    # gr.Button("About Us").click(fn=view_pdf)

    #popup about-us

    with gr.Column():
        open_pdf_button = gr.Button("About Us")
        pdf_viewer = gr.Image(label="PDF Viewer", type="filepath", value="./about_us.png", visible=False)
        close_pdf_button = gr.Button("Close PDF", visible=False)

        # Show PDF
        open_pdf_button.click(
            show_pdf,
            inputs=[],
            outputs=[pdf_viewer, close_pdf_button],
            queue=False
        )

        # Close PDF
        close_pdf_button.click(
            hide_pdf,
            inputs=[],
            outputs=[pdf_viewer, close_pdf_button],
            queue=False
        )

__name__ = "__main__"
# Launching Gradio interface
if __name__ == "__main__":
  initialize_rag('./system_data')
  demo.queue()
  demo.launch()
  print("herelo")
