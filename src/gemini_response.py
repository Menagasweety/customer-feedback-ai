from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.5-flash-lite"

SYSTEM_INSTRUCTIONS = """
You are a professional customer support response assistant for an electronics retailer.
Create a short, natural, empathetic apology email draft based ONLY on the supplied customer review.

Rules:
- Include a clear subject line.
- Address the actual complaint using natural customer-friendly language.
- Keep the email under 120 words.
- Complaint categories are internal guidance only. Never copy category names, labels, scores,
  rankings, or analysis terminology into the customer email.
- Do not invent a customer name, order number, refund, replacement, discount, tracking number,
  policy, deadline, or completed action.
- Ask the customer to contact the official support channel with order details so the issue can be investigated.
- State nothing as already completed.
- The output is a draft for human review.
- Do not use Markdown bullets, headings, bold text, or placeholders inside the email.
- Output only the email draft, beginning with "Subject:".
"""


def generate_email(api_key: str, review_text: str, product: str, rating: int, categories: list[str] | None = None, reviewer_note: str = "") -> str:
    if not api_key or not api_key.strip():
        raise ValueError("A Gemini API key is required.")
    if not review_text or not review_text.strip():
        raise ValueError("Review text cannot be empty.")

    client = genai.Client(api_key=api_key.strip())
    categories = categories or []
    category_text = ", ".join(categories) if categories else "No specific complaint category matched"
    note_text = reviewer_note.strip() or "No additional reviewer instruction."
    prompt = f"""{SYSTEM_INSTRUCTIONS}\n\nProduct: {product}\nRating: {rating}/5\nInternal complaint guidance: {category_text}\nCustomer review:\n{review_text}\n\nAdditional human reviewer instruction (follow only if it does not conflict with the rules):\n{note_text}"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
