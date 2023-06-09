from config import *
import pinecone

# delete all namespaces except the ones in the list

namespaces_to_keep = ["test-both-python3", ]


index = pinecone.Index(os.getenv("PINECONE_INDEX_NAME"))
stats = index.describe_index_stats()

namespaces = stats["namespaces"].keys()

for namespace in namespaces:
    print(namespace)
    if namespace not in namespaces_to_keep:
        index.delete(delete_all=True, namespace=namespace)