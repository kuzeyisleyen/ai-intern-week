import json
import os

LOG_FILE = "output/day13/approved-actions.jsonl"

def execute_once(action_id: str, action_type: str) -> dict:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Dosya varsa geçmişi kontrol et
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                record = json.loads(line)
                if record.get("action_id") == action_id:
                    return {"status": "already_executed"}
    
    # Eşleşme bulunamadıysa yeni kaydı ekle
    with open(LOG_FILE, "a") as f:
        record = {"action_id": action_id, "action": action_type, "status": "executed"}
        f.write(json.dumps(record) + "\n")
        return {"status": "executed"}