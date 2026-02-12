#type: ignore
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

PROMPT = """
Classify the following customer support ticket into ONE category.

Categories:
- Billing & Payments
- Account Access Issues
- Technical Problems
- Feature Requests
- Product Usage Questions
- Security Concerns
- Cancellations & Refunds
- Other / Needs Review

Return ONLY the category name.

Ticket:
"""

def classify_ticket(ticket):
    inputs = tokenizer(PROMPT + ticket, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=10)
    category = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return category

ticket = "I think someone else logged into my account without my permission."

category = classify_ticket(ticket)

needs_human_review = category.lower() == "security concerns"

result = {
    "category": category,
    "ticket": ticket,
    "needs_human_review": needs_human_review
}

print(json.dumps(result, indent=2))
# FLAN-T5