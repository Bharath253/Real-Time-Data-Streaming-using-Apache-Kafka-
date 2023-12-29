# Configuration settings for Kafka and Database connections.

# Kafka API and Schema Registry Credentials
API_KEY = '3ZKDGXJS6UHNMPCC'
ENDPOINT_SCHEMA_URL  = 'https://psrc-wrp99.us-central1.gcp.confluent.cloud'
API_SECRET_KEY = 'iVu3UqFWioZHtff1YYhlryAMD5HNHyCTri4HJV2j0gCxaTaS49/dfmWF4qxB7lt0'
BOOTSTRAP_SERVER = 'pkc-lzvrd.us-west4.gcp.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MECHANISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = 'NG26XICQ73IGEZVZ'
SCHEMA_REGISTRY_API_SECRET = 'uVkP5ZTZrn69Uw1pkmsQMBWcd8JVd8dP7oM3YUBkLupHfBScbPMAqMeCldZgdA2c'

# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Bharath@253"
DB_NAME = "auction"
def config_values():
    """
    Returns Kafka connection configuration values.
    """
    return API_KEY, ENDPOINT_SCHEMA_URL, API_SECRET_KEY, BOOTSTRAP_SERVER, SECURITY_PROTOCOL, SSL_MECHANISM, SCHEMA_REGISTRY_API_KEY, SCHEMA_REGISTRY_API_SECRET

def schema_registry_values():
    """
    Returns Schema Registry connection configuration values.
    """
    return ENDPOINT_SCHEMA_URL, SCHEMA_REGISTRY_API_KEY, SCHEMA_REGISTRY_API_SECRET

def sasl_conf():
    """
    Returns SASL configuration for Kafka.
    Includes SSL mechanism, bootstrap servers, security protocol, and credentials.
    Also sets message size limits.
    """
    return  {
        'sasl.mechanism': SSL_MECHANISM,
        'bootstrap.servers': BOOTSTRAP_SERVER,
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.username': API_KEY,
        'sasl.password': API_SECRET_KEY,
		'receive.message.max.bytes': 50000000,  # Maximum bytes per message
    }

def db_values():
    """
    Returns database connection configuration values.
    """
    return DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def delivery_report(err, msg):
    """
    Callback function for reporting the success or failure of a Kafka message delivery.
    """
    if err is not None:
        print(f"Delivery failed for User record {msg.key()}: {err}")
    else:
        print(f"User record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Kafka Consumer Configuration
def consumer_conf():
    """
    Returns configuration for Kafka Consumer.
    Sets SASL mechanism, bootstrap servers, security protocol, credentials, group ID, and offset settings.
    Also configures message fetch size limits.
    """
    return {
        'sasl.mechanism': SSL_MECHANISM,
        'bootstrap.servers': BOOTSTRAP_SERVER,
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.username': API_KEY,
        'sasl.password': API_SECRET_KEY,
        'group.id': 'group1',
        'auto.offset.reset': "earliest",
    	'fetch.max.bytes': 1048576,  # Example value for maximum fetch bytes
    	'receive.message.max.bytes': 1048576 + 512  # Must be larger than fetch.max.bytes + 512
}

# Kafka Producer Configuration
def writer_conf():
    """
    Returns configuration for Kafka Producer.
    Similar to consumer_conf but with a different group ID.
    Configures SASL mechanism, bootstrap servers, security protocol, credentials, and message size limits.
    """
    return {
        'sasl.mechanism': SSL_MECHANISM,
        'bootstrap.servers': BOOTSTRAP_SERVER,
        'security.protocol': SECURITY_PROTOCOL,
        'sasl.username': API_KEY,
        'sasl.password': API_SECRET_KEY,
        'group.id': 'group2',
        'auto.offset.reset': "earliest",
    	'fetch.max.bytes': 1048576,  # Example value for maximum fetch bytes
    	'receive.message.max.bytes': 1048576 + 512  # Must be larger than fetch.max.bytes + 512
}