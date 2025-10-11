from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_TOKEN") or "hf_your_token_here"
client = InferenceClient(token=HF_TOKEN)
MODEL = "OthmaneAbder2303/legalbert-cuad-clauses"

def classify_clause_api(clause_text):
    # Pass the text as first positional argument
    response = client.text_classification(clause_text, model=MODEL)
    result = response[0]
    return result["label"], result["score"]

# Example usage
clause = "The contractor shall maintain confidentiality of all proprietary information."
label, score = classify_clause_api(clause)
print("Predicted clause type:", label, "Score:", score)
