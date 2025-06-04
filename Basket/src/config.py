import os
from dotenv import load_dotenv
from src.message.kafka_bus import KafkaMessageBus
from src.message.rabbitmq_bus import RabbitMQMessageBus

load_dotenv()

BACKEND = os.getenv("MESSAGE_BUS_BACKEND", "kafka")

def get_message_bus():
    if BACKEND == "kafka":
        return KafkaMessageBus(os.getenv("KAFKA_BOOTSTRAP"))
    elif BACKEND == "rabbitmq":
        return RabbitMQMessageBus(os.getenv("RABBITMQ_URL"))
    else:
        raise ValueError(f"Unsupported MESSAGE_BUS_BACKEND: {BACKEND}")
    
message_bus = get_message_bus()
