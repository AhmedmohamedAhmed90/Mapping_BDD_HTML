
# from torch.nn.functional import cosine_similarity
# from shared import tokenizer, model
# import torch

# def map_bdd_to_html(bdd_scenarios, html_pages):
#     mappings = []
#     for scenario in bdd_scenarios:
#         best_matches = []
#         for page, page_data in html_pages.items():
#             # Match BDD context to HTML context
#             if scenario["context"] == page_data["context"]:
#                 # Match BDD scenario to HTML page based on semantic similarity
#                 scenario_embedding = scenario["embedding"]
#                 page_embedding = page_data["embedding"]
#                 similarity = cosine_similarity(scenario_embedding, page_embedding).item()
                
#                 if similarity > 0.7:  # Threshold for matching
#                     for element in page_data["elements"]:
#                         # Match BDD target to HTML element based on role and semantic similarity
#                         target_embedding = get_embedding(scenario["scenario"])
#                         element_embedding = element["embedding"]
#                         element_similarity = cosine_similarity(target_embedding, element_embedding).item()
                        
#                         if element_similarity > 0.7:  # Threshold for matching
#                             best_matches.append((page, element))
#         mappings.append({"scenario": scenario["scenario"], "matches": best_matches})
#     return mappings

# def get_embedding(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1)  # Average pooling


# from torch.nn.functional import cosine_similarity
# from shared import tokenizer, model
# import torch

# def map_bdd_to_html(bdd_scenarios, html_pages):
#     mappings = []
#     for scenario in bdd_scenarios:
#         best_matches = []
#         for page, page_data in html_pages.items():
#             # Match BDD context to HTML context
#             if scenario["context"] == page_data["context"]:
#                 # Match BDD scenario to HTML page based on semantic similarity
#                 scenario_embedding = scenario["embedding"]
#                 page_embedding = page_data["embedding"]
#                 similarity = cosine_similarity(scenario_embedding, page_embedding).item()
                
#                 if similarity > 0.8:  # Increased threshold for matching
#                     # Split the scenario into steps
#                     steps = scenario["scenario"].split("\n")
#                     for step in steps:
#                         step = step.strip()
#                         # Only include "When" and "And" steps (actions)
#                         if step.lower().startswith(("when", "and")):
#                             step_embedding = get_embedding(step)
#                             best_element = None
#                             best_similarity = -1  # Initialize with a low value
                            
#                             # Find the best matching element for the step
#                             for element in page_data["elements"]:
#                                 # Role-based filtering
#                                 if "select" in step.lower() and element["role"] not in ["select", "input"]:
#                                     continue  # Skip non-matching roles
#                                 if "enter" in step.lower() and element["role"] != "input":
#                                     continue  # Skip non-input elements
#                                 if "click" in step.lower() and element["role"] != "button":
#                                     continue  # Skip non-button elements
                                
#                                 element_embedding = element["embedding"]
#                                 element_similarity = cosine_similarity(step_embedding, element_embedding).item()
                                
#                                 # Update best element if this one is better
#                                 if element_similarity > best_similarity:
#                                     best_similarity = element_similarity
#                                     best_element = element
                            
#                             # Only include the match if similarity exceeds the threshold
#                             if best_similarity > 0.8:  # Increased threshold
#                                 best_matches.append({
#                                     "step": step,
#                                     "page": page,
#                                     "element": best_element
#                                 })
#         mappings.append({"scenario": scenario["scenario"], "matches": best_matches})
#     return mappings

# def get_embedding(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1)  # Average pooling


# from torch.nn.functional import cosine_similarity
# from shared import tokenizer, model
# import torch

# def map_bdd_to_html(bdd_scenarios, html_pages):
#     mappings = []
#     for scenario in bdd_scenarios:
#         best_matches = []
#         best_page = None
#         best_similarity = -1  # Initialize with a low value
        
#         # Find the best matching HTML page for the scenario
#         for page, page_data in html_pages.items():
#             scenario_embedding = scenario["embedding"]
#             page_embedding = page_data["embedding"]
#             similarity = cosine_similarity(scenario_embedding, page_embedding).item()
            
#             if similarity > best_similarity:
#                 best_similarity = similarity
#                 best_page = page
        
#         # Only proceed if a matching page is found
#         if best_page and best_similarity > 0.7:  # Threshold for matching
#             page_data = html_pages[best_page]
#             # Split the scenario into steps
#             steps = scenario["scenario"].split("\n")
#             for step in steps:
#                 step = step.strip()
#                 # Only include "When" and "And" steps (actions)
#                 if step.lower().startswith(("when", "and")):
#                     step_embedding = get_embedding(step)
#                     best_element = None
#                     best_element_similarity = -1  # Initialize with a low value
                    
#                     # Find the best matching element for the step
#                     for element in page_data["elements"]:
#                         # Strict role-based filtering
#                         if "color" in step.lower() and "select" in step.lower():
#                             element_type = element["attributes"].get("type")
#                             element_name = element["attributes"].get("name", "") or ""
#                             if element_type != "radio" or "color" not in element_name.lower():
#                                 continue  # Skip non-color radio buttons
                        
#                         if "size" in step.lower() and "select" in step.lower():
#                             element_type = element["attributes"].get("type")
#                             element_name = element["attributes"].get("name", "") or ""
#                             if element_type != "select" and "size" not in element_name.lower():
#                                 continue  # Skip non-size dropdowns
                        
#                         if "quantity" in step.lower():
#                             element_type = element["attributes"].get("type")
#                             element_name = element["attributes"].get("name", "") or ""
#                             if element_type != "number" and "quantity" not in element_name.lower():
#                                 continue  # Skip non-quantity fields
                        
#                         if "click" in step.lower():
#                             if element["attributes"]["role"] != "button":
#                                 continue  # Skip non-button elements
                        
#                         element_embedding = element["embedding"]
#                         element_similarity = cosine_similarity(step_embedding, element_embedding).item()
                        
#                         # Update best element if this one is better
#                         if element_similarity > best_element_similarity:
#                             best_element_similarity = element_similarity
#                             best_element = element
                    
#                     # Only include the match if similarity exceeds the threshold
#                     if best_element_similarity > 0.7:  # Threshold for matching
#                         best_matches.append({
#                             "step": step,
#                             "page": best_page,
#                             "element": best_element
#                         })
#         mappings.append({"scenario": scenario["scenario"], "matches": best_matches})
#     return mappings

# def get_embedding(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1)  # Average pooling

from torch.nn.functional import cosine_similarity
from shared import tokenizer, model
import torch

def map_bdd_to_html(bdd_scenarios, html_pages):
    """
    Map BDD scenarios to HTML elements based on semantic similarity and context clustering.
    """
    mappings = []
    for scenario in bdd_scenarios:
        best_matches = []
        scenario_embedding = scenario["embedding"]
        scenario_cluster = scenario["context_cluster"]
        scenario_description = scenario["description"]

        print(f"\nProcessing BDD Scenario: {scenario['scenario']}")
        print(f"Inferred Context Cluster: {scenario_cluster}")
        print(f"Semantic Description: {scenario_description}")

        # Find the best matching HTML page based on context cluster and semantic similarity
        best_page = None
        best_similarity = -1
        for page, page_data in html_pages.items():
            # Only consider pages in the same context cluster
            if page_data["context_cluster"] != scenario_cluster:
                continue

            page_embedding = page_data["embedding"]
            page_description = page_data["description"]
            similarity = cosine_similarity(scenario_embedding, page_embedding).item()

            # Additional similarity check using semantic descriptions
            scenario_desc_embedding = get_embedding(scenario_description)
            page_desc_embedding = get_embedding(page_description)
            desc_similarity = cosine_similarity(scenario_desc_embedding, page_desc_embedding).item()

            # Combine both similarities (weighted average)
            combined_similarity = (similarity + desc_similarity) / 2

            print(f"  Comparing with Page: {page}, Similarity: {combined_similarity}")
            print(f"  Page Semantic Description: {page_description}")
            if combined_similarity > best_similarity:
                best_similarity = combined_similarity
                best_page = page

        # Only proceed if a matching page is found
        if best_page and best_similarity > 0.8:  # Increased threshold for matching
            print(f"  Best Matching Page: {best_page}, Similarity: {best_similarity}")
            page_data = html_pages[best_page]
            steps = scenario["scenario"].split("\n")
            for step in steps:
                step = step.strip()
                if step.lower().startswith(("when", "and")):
                    step_embedding = get_embedding(step)
                    best_element = None
                    best_element_similarity = -1

                    # Find the best matching element for the step
                    for element in page_data["elements"]:
                        # Generate a detailed text representation of the element
                        element_text = (
                            f"{element['attributes']['role']} "
                            f"id={element['attributes']['id']} "
                            f"name={element['attributes']['name']} "
                            f"type={element['attributes']['type']} "
                            f"value={element['attributes']['value']} "
                            f"text={element['attributes']['text']} "
                        )

                        # Generate embedding for the element text
                        element_embedding = get_embedding(element_text)

                        # Calculate similarity between step and element
                        element_similarity = cosine_similarity(step_embedding, element_embedding).item()

                        # Update best element if this one is better
                        if element_similarity > best_element_similarity:
                            best_element_similarity = element_similarity
                            best_element = element

                    # Only include the match if similarity exceeds the threshold
                    if best_element_similarity > 0.8:  # Increased threshold for matching
                        print(f"    Matching Step: {step}, Element ID: {best_element['attributes']['id']}, Similarity: {best_element_similarity}")
                        print(f"    Element Semantic Description: {best_element['description']}")
                        best_matches.append({
                            "step": step,
                            "page": best_page,
                            "element": best_element
                        })

        mappings.append({"scenario": scenario["scenario"], "matches": best_matches})
    return mappings

def get_embedding(text):
    """
    Generate embeddings for a given text using the E5 model.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)  # Average pooling