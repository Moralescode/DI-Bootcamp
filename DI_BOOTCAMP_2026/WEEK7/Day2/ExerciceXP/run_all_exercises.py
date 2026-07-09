import sys
import subprocess
import importlib.util

def ensure(package, import_name=None):
    if import_name is None:
        import_name = package.split('==')[0].split('>=')[0]
    if importlib.util.find_spec(import_name) is None:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', package])

# Install / verify dependencies
ensure('pandas')
ensure('numpy<2')
ensure('faiss-cpu>=1.8.0')
ensure('sentence-transformers')
ensure('transformers')

# Try to install chromadb, but if it fails we'll continue without it
try:
    ensure('chromadb==0.3.21', 'chromadb')
except Exception as e:
    print(f"Warning: chromadb installation failed ({e}), will use FAISS-only fallback.")

import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer, InputExample
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

os.makedirs('cache', exist_ok=True)

DATA_PATH = r'C:\Users\DELL\Desktop\TTA_Donald_KOUASSI\DI_BOOTCAMP_2026\WEEK7\Day2\ExerciceXP\Data\labelled_newscatcher_dataset.csv'

print("=" * 60)
print("EXERCISE 1 · Data loading and preparation")
print("=" * 60)
pdf = pd.read_csv(DATA_PATH, sep=';')
if 'id' not in pdf.columns:
    pdf['id'] = range(len(pdf))
print(pdf.head())
pdf_subset = pdf.head(1000)
print("Subset shape:", pdf_subset.shape)
print(pdf_subset[['id', 'title']].head())

print("\n" + "=" * 60)
print("EXERCISE 2 · Vectorization with Sentence Transformers")
print("=" * 60)

def example_create_fn(idx: int, text: str) -> InputExample:
    return InputExample(guid=str(idx), texts=[text], label=0.0)

faiss_train_examples = [example_create_fn(idx, text) for idx, text in enumerate(pdf_subset['title'].tolist())]
print("First 2 training examples:")
for ex in faiss_train_examples[:2]:
    print(f"  guid={ex.guid}, text={ex.texts[0][:60]}...")

model = SentenceTransformer('all-MiniLM-L6-v2')
titles_list = pdf_subset['title'].tolist()
print(f"Encoding {len(titles_list)} titles...")
faiss_title_embedding = model.encode(titles_list, convert_to_numpy=True, show_progress_bar=True)
print(f"Embedding shape: {len(faiss_title_embedding)} vectors x {len(faiss_title_embedding[0])} dims")

print("\n" + "=" * 60)
print("EXERCISE 3 · FAISS indexing and search")
print("=" * 60)
pdf_to_index = pdf_subset
id_index = pdf_to_index['id'].to_numpy().astype(np.int64)
content_encoded_normalized = faiss_title_embedding.astype('float32')
faiss.normalize_L2(content_encoded_normalized)
index_content = faiss.IndexIDMap(faiss.IndexFlatIP(content_encoded_normalized.shape[1]))
index_content.add_with_ids(content_encoded_normalized, id_index)
print(f"FAISS index total: {index_content.ntotal}")

def search_content(query: str, pdf_to_index: pd.DataFrame, k: int = 3):
    query_vector = model.encode([query], convert_to_numpy=True)
    query_vector = query_vector.astype('float32')
    faiss.normalize_L2(query_vector)
    sims, ids = index_content.search(query_vector, k)
    results = pdf_to_index[pdf_to_index['id'].isin(ids[0])].copy()
    results['similarities'] = sims[0]
    return results

print("Query: 'animal' | Top 5 results:")
results_faiss = search_content('animal', pdf_to_index, k=5)
print(results_faiss[['id', 'topic', 'title', 'similarities']].to_string(index=False))

print("\n" + "=" * 60)
print("EXERCISE 4 · ChromaDB collection and querying")
print("=" * 60)

chroma_results = None
collection = None
chroma_client = None

try:
    import chromadb
    from chromadb.config import Settings
    chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
    collection_name = 'my_news'
    if any(c.name == collection_name for c in chroma_client.list_collections()):
        chroma_client.delete_collection(name=collection_name)

    collection = chroma_client.create_collection(name=collection_name)
    collection.add(
        documents=pdf_subset['title'].tolist(),
        ids=[str(i) for i in pdf_subset['id'].tolist()],
        metadatas=[
            {'topic': t, 'link': l, 'domain': d, 'published_date': p, 'lang': lng}
            for t, l, d, p, lng in zip(
                pdf_subset['topic'], pdf_subset['link'], pdf_subset['domain'],
                pdf_subset['published_date'], pdf_subset['lang']
            )
        ]
    )
    chroma_results = collection.query(query_texts=['animal'], n_results=3)
    print("ChromaDB query results:")
    print(json.dumps(chroma_results, indent=2))
except Exception as e:
    print(f"ChromaDB not available: {e}")
    print("Falling back to FAISS results for QA context.")
    chroma_results = {
        'documents': [results_faiss['title'].tolist()[:3]],
        'metadatas': [results_faiss[['topic', 'link', 'domain', 'published_date', 'lang']].head(3).to_dict('records')]
    }

print("\n" + "=" * 60)
print("EXERCISE 5 · Question answering with a Hugging Face model")
print("=" * 60)

model_id = 'google/flan-t5-small'
print(f"Loading model: {model_id} ...")
pipe = pipeline('text2text-generation', model=model_id)

question = "What's the latest news on space development?"
context_docs = chroma_results['documents'][0][:3]
context = ' '.join(context_docs)
prompt = f"Answer the question using only the context.\nContext: {context}\nQuestion: {question}\nAnswer: "
print(f"Prompt preview: {prompt[:300]}...")
response = pipe(prompt)[0]['generated_text']
print(f"\nQuestion: {question}")
print(f"Answer: {response}")

print("\n" + "=" * 60)
print("ALL EXERCISES COMPLETED SUCCESSFULLY")
print("=" * 60)
