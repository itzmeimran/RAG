# RAG Python

This project is a simple Retrieval-Augmented Generation (RAG) demo that:

- loads text or PDF documents
- splits them into smaller chunks
- converts those chunks into embeddings
- stores them in ChromaDB
- retrieves relevant chunks for a user question
- sends the retrieved context to OpenAI to generate an answer

The current workflow is built in [document.ipynb](d:\WEB-DEV\RAG\RAG-Python\notebook\document.ipynb).

## Requirements

Before you start, make sure you have:

- Python 3.11 or newer
- `pip`
- an OpenAI API key

## Project Structure

```text
RAG-Python/
|-- data/
|   |-- pdf_files/
|   |-- text_files/
|   `-- vector_store/
|-- notebook/
|   `-- document.ipynb
|-- main.py
|-- requirements.txt
`-- README.md
```

## Step-by-Step Installation

### 1. Clone the project

```powershell
git clone <your-repo-url>
cd RAG-Python
```

If you already have the folder locally, just open it in your editor.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

On PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Command Prompt:

```bat
.venv\Scripts\activate
```

### 4. Install dependencies

```powershell
uv pip install -r requirements.txt
```

If you want to run the notebook and Jupyter is not already installed, also run:

```powershell
uv pip install notebook ipykernel
```

### 5. Add your OpenAI API key

Create a `.env` file in the project root and add:

```env
OPENAI_API_KEY="your_openai_api_key_here"
```

Important:

- keep the `.env` file private
- do not commit your API key to GitHub
- if a real key was exposed before, rotate it from your OpenAI account

### 6. Create the data folders

If these folders do not already exist, create them:

```powershell
mkdir data\pdf_files
mkdir data\text_files
mkdir data\vector_store
```

### 7. Add your documents

Put your PDF files inside:

```text
data/pdf_files/
```

You can also place `.txt` files inside:

```text
data/text_files/
```

### 8. Start Jupyter Notebook

```powershell
jupyter notebook
```

Then open:

```text
notebook/document.ipynb
```

## How to Run the RAG Pipeline

Open [document.ipynb](d:\WEB-DEV\RAG\RAG-Python\notebook\document.ipynb) and run the cells in order.

### Recommended execution order

1. Load the required libraries
2. Load `.txt` files or PDF files
3. Split documents into chunks
4. Initialize the embedding model
5. Initialize the Chroma vector store
6. Generate embeddings from the chunks
7. Store the embeddings in ChromaDB
8. Create the retriever
9. Run `rag_simple(...)` with your question

## Example Flow

After your PDF is placed in `data/pdf_files/`, the notebook will:

1. read the PDF
2. split the content into smaller pieces
3. turn each piece into embeddings
4. save embeddings in ChromaDB
5. retrieve the most relevant chunks for a question
6. send those chunks to OpenAI for the final answer

## Notes

- if retrieval says `No relevant content found to answer the question`, rebuild the vector store by rerunning the ingestion cells
- if you change chunking logic, embedding model, or collection settings, re-ingest the documents
- the current notebook uses a Chroma collection named `pdf_documents_cosine`

## Troubleshooting

### API key issues

If OpenAI calls fail:

- confirm `.env` exists in the project root
- confirm the key is valid
- restart the notebook kernel after updating `.env`

### PDF loaded but no answer returned

Check that:

- the PDF was placed in `data/pdf_files/`
- the ingestion cells were rerun after code changes
- embeddings were successfully added to the vector store
- the retriever returns results before calling the LLM

### Dependency issues

If `pip install -r requirements.txt` fails, upgrade pip first:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Next Improvements

You can extend this project by:

- moving notebook logic into `main.py`
- adding a simple Streamlit or Flask UI
- supporting multiple PDFs with upload
- adding collection reset and rebuild commands
- adding citation-style responses from retrieved chunks
