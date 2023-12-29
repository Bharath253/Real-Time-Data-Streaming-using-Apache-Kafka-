from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
import config

def schema_config():
    ENDPOINT_SCHEMA_URL, SCHEMA_REGISTRY_API_KEY, SCHEMA_REGISTRY_API_SECRET = config.schema_registry_values()
    return {
        'url': ENDPOINT_SCHEMA_URL,
        'basic.auth.user.info': f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}"
    }

def create_deserializer(topic):
    schema_registry_client = SchemaRegistryClient(schema_config())
    my_schema = schema_registry_client.get_latest_version(topic + '-value').schema.schema_str
    return JSONDeserializer(my_schema, from_dict=None)
