from dotenv import load_dotenv
import os 
from pinecone import Pinecone, ServerlessSpec
import tensorflow_hub as hub

load_dotenv()
pc_api = os.getenv('PINECONE_API')

# pinecone
def CreatePineConeIndex(pc, indexName, spec):
    pc.create_index(
        indexName,
        dimension=512,
        metric='dotproduct',
        spec=spec
    )
    print(f"create pinecone with index name {indexName}")

def PineConeConnect(pc, index_name):
    try:
        pc.Index(index_name)
        print(f"connected to pinecone with name : {index_name}")
        return pc.Index(index_name)
    except Exception as err:
        print(f"gagal : {err}")
        return None
        
def StoreVectorToPineCone(embedModel:TensorEmbed, fileName, PineConeIndex):
    # open the document
    # document = open(fileName, 'r')
    # textList_FromDocument = [i for i in document.read().split('\n') if i != '']

    try:
      with open(fileName, 'r', encoding='utf-8') as document:
        textList_FromDocument = [i for i in document.read().split('\n') if i != '']
    except UnicodeDecodeError:
      with open(fileName, 'r', encoding='windows-1252') as document:
        textList_FromDocument = [i for i in document.read().split('\n') if i != '']
    
    # embed the document with embed model
    embedDocument = embedModel.embed(textList_FromDocument)
    
    for i, embed in enumerate(embedDocument):
      sentence_id = f"{fileName.split('/')[-1].split('.')[0]}_{i}"
      metadata = {
          'text': textList_FromDocument[i],
          'source': fileName.split('/')[-1],
          'title': fileName.split('/')[-1].split('.')[0],
      }

      PineConeIndex.upsert(vectors=[(sentence_id, embed, metadata)])

    print(f"success to store vector in {fileName}")


# embeded model
class TensorEmbed:
    def __init__(self, modelPath='https://tfhub.dev/google/universal-sentence-encoder/4'):
        self.model = hub.load(modelPath)
    
    def embed(self, text):
        return self.model(text).numpy().tolist()
    
    def embedQuery(self, query):
        return self.model([query]).numpy().tolist()
    

# Embed = TensorEmbed()

# # pinecone connection
# pc = Pinecone(api_key=pc_api)
# spec = ServerlessSpec(
#     cloud='aws',
#     region='us-east-1'
# )

# pineIndex = 'coba-buat-pinecone'

# # create index vector database
# CreatePineConeIndex(
#     pc=pc,
#     indexName=pineIndex,
#     spec=spec
# )

# # connect to the pinecone index
# PineConeConnect(
#     pc=pc,
#     index_name=pineIndex
# )

# # store the information in pinecone index
# wikipedia = 'data/2024106205954braintumorwikipedia.txt'
# clevelandclinic = 'data/202410621034braintumorclevelandclinic.txt'
# aans = 'data/202410621213braintumoraans.txt'

# for name in [wikipedia, clevelandclinic, aans]:
#   StoreVectorToPineCone(Embed, name, index)