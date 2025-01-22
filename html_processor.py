# from bs4 import BeautifulSoup
# import os

# def process_html(directory_path):
#     html_elements = {}
#     for file_name in os.listdir(directory_path):
#         if file_name.endswith(".html"):
#             with open(os.path.join(directory_path, file_name), "r", encoding="utf-8") as file:
#                 soup = BeautifulSoup(file, "html.parser")
            
#             # Extract elements of interest
#             elements = []
#             for tag in soup.find_all(["button", "input", "a", "div", "span"]):
#                 elements.append({
#                     "content": str(tag),
#                     "label": tag.get("id") or tag.get("name") or tag.text.strip()
#                 })
#             html_elements[file_name] = elements
#     return html_elements



# from bs4 import BeautifulSoup
# import os
# from shared import tokenizer, model
# import torch

# def extract_context(soup):
#     """
#     Extract context from an HTML page.
#     """
#     if "user-login-form" in str(soup):
#         return "user login"
#     elif "admin-login-form" in str(soup):
#         return "admin login"
#     else:
#         return "unknown"

# def process_html(directory_path):
#     html_pages = {}
#     for file_name in os.listdir(directory_path):
#         if file_name.endswith(".html"):
#             with open(os.path.join(directory_path, file_name), "r", encoding="utf-8") as file:
#                 soup = BeautifulSoup(file, "html.parser")
            
#             # Extract context
#             context = extract_context(soup)
            
#             # Extract elements of interest
#             elements = []
#             for tag in soup.find_all(["button", "input", "a", "div", "span"]):
#                 role = tag.name  # Role of the element (e.g., "button", "input")
#                 label = tag.get("id") or tag.get("name") or tag.text.strip()  # Label of the element
#                 embedding = get_embedding(label)  # Generate embedding for the element label
#                 elements.append({
#                     "content": str(tag),
#                     "role": role,
#                     "label": label,
#                     "embedding": embedding
#                 })
            
#             # Generate embedding for the entire HTML page
#             page_text = soup.get_text()
#             page_embedding = get_embedding(page_text)
#             html_pages[file_name] = {
#                 "context": context,
#                 "elements": elements,
#                 "embedding": page_embedding
#             }
#     return html_pages

# def get_embedding(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1)  # Average pooling

# from bs4 import BeautifulSoup
# import os
# from shared import tokenizer, model
# import torch

# def process_html(directory_path):
#     html_pages = {}
#     for file_name in os.listdir(directory_path):
#         if file_name.endswith(".html"):
#             with open(os.path.join(directory_path, file_name), "r", encoding="utf-8") as file:
#                 soup = BeautifulSoup(file, "html.parser")
            
#             # Extract elements of interest
#             elements = []
#             for tag in soup.find_all(["button", "input", "a", "div", "span"]):
#                 # Extract all attributes
#                 attributes = {
#                     "role": tag.name,  # Role of the element (e.g., "button", "input")
#                     "id": tag.get("id"),
#                     "name": tag.get("name"),
#                     "type": tag.get("type"),
#                     "value": tag.get("value"),  # Add value attribute
#                     "class": tag.get("class"),
#                     "text": tag.text.strip(),  # Visible text
#                     "parent": tag.parent.name if tag.parent else None,  # Parent element
#                     "siblings": [sibling.name for sibling in tag.find_previous_siblings()]  # Sibling elements
#                 }
                
#                 # Create a text representation of the element
#                 element_text = f"{attributes['role']} "
#                 if attributes["id"]:
#                     element_text += f"id={attributes['id']} "
#                 if attributes["name"]:
#                     element_text += f"name={attributes['name']} "
#                 if attributes["type"]:
#                     element_text += f"type={attributes['type']} "
#                 if attributes["value"]:
#                     element_text += f"value={attributes['value']} "
#                 if attributes["class"]:
#                     element_text += f"class={attributes['class']} "
#                 if attributes["text"]:
#                     element_text += f"text={attributes['text']} "
#                 if attributes["parent"]:
#                     element_text += f"parent={attributes['parent']} "
#                 if attributes["siblings"]:
#                     element_text += f"siblings={attributes['siblings']} "
                
#                 # Generate embedding for the element
#                 embedding = get_embedding(element_text)
#                 elements.append({
#                     "content": str(tag),
#                     "attributes": attributes,
#                     "embedding": embedding
#                 })
            
#             # Generate embedding for the entire HTML page
#             page_text = soup.get_text()
#             page_embedding = get_embedding(page_text)
#             html_pages[file_name] = {
#                 "elements": elements,
#                 "embedding": page_embedding
#             }
#     return html_pages

# def get_embedding(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1)  # Average pooling


from bs4 import BeautifulSoup
import os
from shared import tokenizer, model
import torch
from sklearn.cluster import DBSCAN
import numpy as np
from transformers import pipeline
from sklearn.preprocessing import normalize

def process_html(directory_path):
    """
    Process HTML files in a directory, extract elements, and generate embeddings and semantic descriptions.
    """
    html_pages = {}
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        print(f"Failed to load summarization model: {e}")
        summarizer = None  # Fallback to no summarization

    for file_name in os.listdir(directory_path):
        if file_name.endswith(".html"):
            with open(os.path.join(directory_path, file_name), "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
            
            # Extract elements of interest
            elements = []
            for tag in soup.find_all(["button", "input", "a", "div", "span"]):
                # Extract attributes
                attributes = {
                    "role": tag.name,
                    "id": tag.get("id"),
                    "name": tag.get("name"),
                    "type": tag.get("type"),
                    "value": tag.get("value"),
                    "class": tag.get("class"),
                    "text": tag.text.strip(),
                    "parent": tag.parent.name if tag.parent else None,
                    "siblings": [sibling.name for sibling in tag.find_previous_siblings()]
                }
                
                # Create a text representation of the element
                element_text = f"{attributes['role']} "
                if attributes["id"]:
                    element_text += f"id={attributes['id']} "
                if attributes["name"]:
                    element_text += f"name={attributes['name']} "
                if attributes["type"]:
                    element_text += f"type={attributes['type']} "
                if attributes["value"]:
                    element_text += f"value={attributes['value']} "
                if attributes["class"]:
                    element_text += f"class={attributes['class']} "
                if attributes["text"]:
                    element_text += f"text={attributes['text']} "
                if attributes["parent"]:
                    element_text += f"parent={attributes['parent']} "
                if attributes["siblings"]:
                    element_text += f"siblings={attributes['siblings']} "
                
                # Generate embedding for the element
                embedding = get_embedding(element_text)
                description = generate_semantic_description(element_text, summarizer)  # Generate semantic description
                elements.append({
                    "content": str(tag),
                    "attributes": attributes,
                    "embedding": embedding,
                    "description": description
                })
            
            # Generate embedding for the entire HTML page
            page_text = soup.get_text()
            page_embedding = get_embedding(page_text)
            page_description = generate_semantic_description(page_text, summarizer)  # Generate semantic description
            html_pages[file_name] = {
                "elements": elements,
                "embedding": page_embedding,
                "description": page_description
            }
    
    # Cluster HTML pages into contexts
    html_embeddings = [page_data["embedding"].numpy() for page_data in html_pages.values()]
    html_embeddings = np.vstack(html_embeddings)  # Stack embeddings into a 2D array
    html_embeddings = normalize(html_embeddings)  # Normalize embeddings
    clusters = cluster_contexts(html_embeddings)  # Use DBSCAN for clustering
    for i, (file_name, page_data) in enumerate(html_pages.items()):
        page_data["context_cluster"] = clusters[i]
    
    return html_pages

def get_embedding(text):
    """
    Generate embeddings for a given text using the E5 model.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Average pooling

def generate_semantic_description(text, summarizer):
    """
    Generate a semantic description of a text using a summarization model.
    """
    if summarizer:
        input_length = len(text.split())
        max_length = min(50, input_length)
        min_length = min(25, max_length // 2)
        description = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return description
    else:
        return "No description available"

def cluster_contexts(embeddings):
    """
    Cluster embeddings into contexts using DBSCAN.
    """
    dbscan = DBSCAN(eps=0.5, min_samples=2)  # Adjust eps and min_samples as needed
    clusters = dbscan.fit_predict(embeddings)
    return clusters