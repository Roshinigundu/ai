from transformers import BertTokenizer, BertForTokenClassification
import torch

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForTokenClassification.from_pretrained("bert-base-uncased")

# Text preprocessing and tokenization
text = "Text containing government and company entities."
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

# Entity extraction
with torch.no_grad():
    outputs = model(**inputs)
predictions = torch.argmax(outputs.logits, dim=2)

# Map predicted labels back to entities
entity_labels = [model.config.id2label[label_id] for label_id in predictions[0].tolist()]