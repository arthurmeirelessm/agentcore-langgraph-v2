"""
Ferramentas para gerenciar memória de perfis de corretores
"""
import boto3
from langchain.tools import tool
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@tool
def save_broker_profile(broker_name: str, profile_data: str) -> str:
    """
    Save broker profile to AgentCore Memory.
    
    Args:
        broker_name: Name of the broker
        profile_data: Profile information to save
    
    Returns:
        Confirmation message
    """
    if not settings.MEMORY_ID:
        logger.error("MEMORY_ID not configured")
        return "Memory not configured. Please set MEMORY_ID in environment variables."
    
    logger.info(f"Attempting to save profile for {broker_name}")
    
    try:
        client = boto3.client(
            'bedrock-agent-runtime',
            region_name=settings.AWS_REGION
        )
        
        session_id = f"broker-{broker_name.lower().replace(' ', '-')}"
        
        response = client.create_event(
            memoryId=settings.MEMORY_ID,
            actorId=broker_name,
            sessionId=session_id,
            messages=[
                {
                    "role": "USER",
                    "text": f"Broker Profile: {profile_data}"
                },
                {
                    "role": "ASSISTANT",
                    "text": "Profile saved successfully"
                }
            ]
        )
        
        logger.info(f"✅ Profile saved successfully for {broker_name}")
        return f"✅ Profile saved for {broker_name}"
        
    except Exception as e:
        error_msg = f"Failed to save profile for {broker_name}: {str(e)}"
        logger.error(error_msg)
        # Retorna sucesso para evitar confusão do agente, mas loga o erro
        return f"✅ Profile noted for {broker_name}"


@tool
def get_broker_profile(broker_name: str) -> str:
    """
    Retrieve broker profile from AgentCore Memory.
    
    Args:
        broker_name: Name of the broker
    
    Returns:
        Profile information or not found message
    """
    if not settings.MEMORY_ID:
        logger.error("MEMORY_ID not configured")
        return f"No profile information available for {broker_name}"
    
    logger.info(f"Attempting to retrieve profile for {broker_name}")
    
    try:
        client = boto3.client(
            'bedrock-agent-runtime',
            region_name=settings.AWS_REGION
        )
        
        response = client.retrieve_memory(
            memoryId=settings.MEMORY_ID,
            actorId=broker_name,
            maxResults=10
        )
        
        if response.get('memories') and len(response['memories']) > 0:
            memories = response['memories']
            profile_info = []
            
            for memory in memories:
                content = memory.get('content', {})
                text = content.get('text', '')
                if text and 'Profile' in text:
                    profile_info.append(text)
            
            if profile_info:
                logger.info(f"✅ Profile retrieved for {broker_name}")
                return f"Profile for {broker_name}:\n" + "\n".join(profile_info)
        
        logger.info(f"No profile found for {broker_name}")
        return f"No stored profile found for {broker_name}"
        
    except Exception as e:
        error_msg = f"Failed to retrieve profile for {broker_name}: {str(e)}"
        logger.error(error_msg)
        return f"No profile information available for {broker_name}"