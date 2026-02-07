import uuid
import numpy as np
from src.utils.bedrock import get_embedding
from redis import Redis

redis_setup = Redis(
    host="localhost",
    port=6379,
    decode_responses=False  # precisa ser False por causa do vetor binário
)


SIMILARITY_THRESHOLD = 0.7

def save_to_semantic_cache(question: str, answer: str):
    embedding = get_embedding(question)
    vector_bytes = np.array(embedding, dtype=np.float32).tobytes()

    key = f"doc:{uuid.uuid4()}"

    redis_setup.hset(
        key,
        mapping={
            "question": question,
            "answer": answer,
            "vector_field": vector_bytes
        }
    )



def get_answer_from_cache(user_question: str):
    embedding = get_embedding(user_question)
    vector_bytes = np.array(embedding, dtype=np.float32).tobytes()

    results = redis_setup.execute_command(
        "FT.SEARCH",
        "myIndex",
        "*=>[KNN 1 @vector_field $vec AS score]",
        "PARAMS", "2", "vec", vector_bytes,
        "SORTBY", "score",
        "RETURN", "3", "answer", "question", "score",
        "DIALECT", "2"
    )

    if results[0] == 0:
        return None

    fields = results[2]
    data = {fields[i].decode(): fields[i+1] for i in range(0, len(fields), 2)}

    score = float(data["score"].decode())
    similarity = 1 - score

    print("Score:", score, "Similarity:", similarity)

    if similarity >= SIMILARITY_THRESHOLD:
        return data["answer"].decode()

    return None

