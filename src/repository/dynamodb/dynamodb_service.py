# src/repository/episode_store.py
import boto3
from datetime import datetime
from typing import Optional, Dict
from uuid import uuid4

DYNAMO_TABLE = "agent_turn_sessions"  # nome da tabela no DynamoDB

class DynamoDbService:
    def __init__(self, region_name="us-east-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(DYNAMO_TABLE)

    def save_episode_in_dynamo(
        self,
        actor_id: str,
        session_id: str,
        goal: str,
        outcome: str,
        topic: Optional[str] = None,
        signals: Optional[Dict] = None
    ):
        episode_id = str(uuid4())
        item = {
            "actor_id": f"ACTOR#{actor_id}",
            "session_id": f"SESSION#{session_id}#EPISODE#{episode_id}",
            "goal": goal,
            "outcome": outcome,
            "topic": topic or "",
            "signals": signals or {},
            "created_at": datetime.utcnow().isoformat()
        }
        self.table.put_item(Item=item)
        return episode_id

    def load_last_episode(self, actor_id: str, session_id: str) -> Optional[Dict]:
        """
        Retorna o último episódio de uma sessão do usuário
        """
        # Ajuste: session_id deve incluir prefixo #EPISODE# ao consultar
        sk_prefix = f"SESSION#{session_id}#EPISODE#"
        pk_prefix = f"ACTOR#{actor_id}"

        response = self.table.query(
            KeyConditionExpression="actor_id = :actor_id AND begins_with(session_id, :sk_prefix)",
            ExpressionAttributeValues={
                ":actor_id": pk_prefix,
                ":sk_prefix": sk_prefix
            },
            ScanIndexForward=False,  # do mais recente para o mais antigo
            Limit=1
        )

        items = response.get("Items", [])
        return items[0] if items else None

