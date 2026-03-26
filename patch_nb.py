import json, pathlib, textwrap
path=pathlib.Path('notebook/document.ipynb')
nb=json.loads(path.read_text(encoding='utf-8'))
cell13_src=textwrap.dedent('''
class VectorStore:
    '''Manages document embeddings in a ChromaDB vector store'''
    def __init__(self,collection_name:str = 'pdf_documents_cosine',persist_directory:str = '../data/vector_store'):
        '''Initialize the vector store
        Args:
            Collectoin_name : Name of the ChromaDB collection
            persist_director: Directory to persist the vector store
        '''
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()
    
    def _initialize_store(self):
        '''Initialize ChromaDB client and collection'''
        try:
                # Create persistent ChromaDB client
                os.makedirs(self.persist_directory,exist_ok= True)
                self.client = chromadb.PersistentClient(path=self.persist_directory)
                
                #Get or create collection with cosine distance
                self.collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine", "description":"PDF Document embeddings for RAG"}
                )
                print(f'Vector store inititalized. Collection: {self.collection_name}')
                print(f'Existing documents in Collection: {self.collection.count()}')
                
        except Exception as e :
            print(f"Error initializing vector store : {e}")
            raise
    def add_documents(self,documents: List[Any],embeddings:np.ndarray):
        '''Add documents and their embeddings to the vector store
        Args:
            documents: List of LangChain documents
            embeddings: Correspondingn embeddings for the documents
        '''
        if len(documents) != len(embeddings):
            raise ValueError('Number of documents must match number of embeddings')
        
        print(f'Adding {len(documents)} documents to vector store ... ')
        
        # Prepare data for ChromaDB
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []
        for i, (doc,embedding) in enumerate(zip(documents,embeddings)):
            
            #Generate unique ID
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
            
            #Prepare Meta Data
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)
            #Document content
            documents_text.append(doc.page_content)
            
            #Embedding
            embeddings_list.append(embedding.tolist())
        
        #Add to collection
        try:
            self.collection.add(
                ids = ids,
                embeddings= embeddings_list,
                metadatas = metadatas,
                documents = documents_text
            )
            print(f"Successfully added {len(documents)} documents to vector store")
            print(f"Total documents in collection : {self.collection.count()}")
            
        except Exception as e :
            print(f"Error adding documents to vector store : {e}")
            raise
        
vectorstore  = VectorStore()
vectorstore
''').splitlines(keepends=True)
nb['cells'][13]['source']=cell13_src
cell17_src=textwrap.dedent('''
class RAGRetriever:
    '''Handles query-based retrieval from the vector store'''
    def __init__(self,vector_store: VectorStore,embedding_manager = EmbeddingManager):
        '''
        Initializing the retriever
        
        Args:
            vector_store: Vector store containing document embeddings
            embedding_manager: Manager for generating query embeddings
        '''
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager
    
    def retrieval(self,query:str, top_k:int = 5, score_threshold :float = -1.0) -> List[Dict[str,Any]]:
        '''Retreive relevant documents for a query
        Args:
            query : The search query
            top_k : Number of top results to return
            score_threshold : Minimum similarity score threshold
        Returns:
            List of dictonaries containing retrieved documents and metadata
            
        '''
        print(f"Retreivig documents for query: {query}'")
        print(f"Top K : {top_k}, Score threshold: {score_threshold}")
        
        # Generate query embedding
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]
        
        # Search in vector store
        try:
            results = self.vector_store.collection.query(
                query_embeddings = [query_embedding.tolist()],
                n_results = top_k
                )
            retrieved_docs = []
            
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0]
                distances = results['distances'][0]
                ids = results['ids'][0]
                
                for i,(doc_id,document,metadata,distance) in enumerate(zip(ids,documents,metadatas,distances)):
                    # Convert distance to similarity score (ChromaDB uses cosine distance)
                    similarity_score = 1 - distance
                    
                    if similarity_score >= score_threshold:
                        retrieved_docs.append({
                            'id':doc_id,                                  
                            'content':document,
                            'metadata':metadata,
                            'similarity_score':similarity_score,
                            'distance':distance,
                            'rank': i+1
                            
                            })
                print (f'Retrieved {len(retrieved_docs)} documents (after filtering)')
            else:
                print(f'No documents found')
            return retrieved_docs
        except Exception as e:
            print(f'Error during retrieval : {e}')
            return [] 
rag_retriever = RAGRetriever(vectorstore,embedding_manager)
''').splitlines(keepends=True)
nb['cells'][17]['source']=cell17_src
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('patched')
