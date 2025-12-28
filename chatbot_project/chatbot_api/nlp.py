from sentence_transformers import SentenceTransformer, util
from groq import Groq  # official Groq client

# Load embedding model once
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Groq client
client = Groq(api_key="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")

def get_best_answer(user_query, qa_list, threshold=0.9):
    if not qa_list:  # ✅ handle empty list
        # fallback to LLM directly
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Always answer in 2–4 full sentences, "
                        "forming a complete, coherent paragraph. Avoid bullet points or half sentences."
                    )
                },
                {"role": "user", "content": user_query},
            ],
            temperature=0.1,
            max_tokens=300
        )
        return completion.choices[0].message.content

    questions = [qa['question'] for qa in qa_list]
    answers = [qa['answer'] for qa in qa_list]

    question_embeddings = embedder.encode(questions, convert_to_tensor=True)
    query_embedding = embedder.encode(user_query, convert_to_tensor=True)

    similarity = util.cos_sim(query_embedding, question_embeddings)
    best_match_index = similarity.argmax().item()
    best_score = similarity[0][best_match_index].item()

    print(f"🔍 Best score: {best_score:.2f}")

    if best_score >= threshold:
        return answers[best_match_index]
    else:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Always answer in 2–4 full sentences, "
                        "forming a complete, coherent paragraph. Avoid bullet points or half sentences."
                    )
                },
                {"role": "user", "content": user_query},
            ],
            temperature=0.1,
            max_tokens=300
        )
        return completion.choices[0].message.content
