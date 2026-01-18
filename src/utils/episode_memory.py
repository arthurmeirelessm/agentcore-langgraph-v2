# src/repository/infer_outcome.py

def infer_outcome(result: dict) -> str:
    if result.get("error"):
        return "failed"
    if result.get("final_response"):
        return "goal_completed"
    return "unknown"
