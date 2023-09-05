# tradeapp_parser

# Mongo
MONGO_INITDB_ROOT_USERNAME=mongo_user
MONGO_INITDB_ROOT_PASSWORD=mongo_password
MONGO_INITDB_DATABASE=tradeapp_parser
DATABASE_URL=mongodb://mongo_user:mongo_password@localhost/tradeapp_parser?authSource=admin

# Binance
BINANCE_WEBSOCKET_URI=wss://stream.binance.com:443/stream?streams=!miniTicker@arr

# Alpha Vantage
ALPHA_VANTAGE_DEMO_API_KEY=demno
ALPHA_VANTAGE_API_KEY=no_key
ALPHA_VANTAGE_URL=https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}

# ZooKeeper
ZOOKEEPER_CLIENT_PORT=2181

# Kafka
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
KAFKA_BROKER_ID=1
KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181