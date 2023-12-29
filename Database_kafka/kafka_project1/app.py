from flask import Flask, render_template, request, url_for
import datetime
import random
import config
from kafka_producer import init_kafka_producer, produce_message
from uuid import uuid4
from db_operations import get_highest_bid

# Initialize the Flask application
app = Flask(__name__)

# Database configuration settings
db_config = {
    'host': config.DB_HOST,
    'user': config.DB_USER,
    'passwd': config.DB_PASSWORD,
    'database': config.DB_NAME
}

# Initialize Kafka producer
producer = init_kafka_producer()
# Topic for Kafka messages
topic = 'bidding'

@app.route("/", methods=['GET','POST'])
def bid():
    # Retrieve the highest bid from the database
    highest_bid = get_highest_bid(db_config)

    # If the request is POST, process the bid data
    if request.method == 'POST':
        # Retrieve name and price from the form data
        name = request.form.get('name', '')
        price = request.form.get('price', '')
        # Timestamp for the bid
        bid_ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Generate a unique key for the message
        msg_key = str(uuid4())

        # Auto-generate name and price if empty (useful for testing)
        if not name or not price:
            name = random.choice(['James', 'Brown', 'Happy', 'Chill', 'Mask', 'Helpart', 'Pam', 'Scott'])
            price = round(random.random() * 1000)

        response = {
            'name': name,
            'price': int(price),
            'bid_ts': bid_ts
        }
        print(f"{msg_key}: {response}")

        # Send the bid data to Kafka
        produce_message(producer, topic, msg_key, response)

        # Update highest bid if the new bid is higher
        if int(price) > highest_bid:
            highest_bid = int(price)

    # Render the index.html template with bid data
    return render_template('index.html', bid_added=request.method == 'POST', highest_bid=highest_bid)

# Run the Flask app if this file is executed as the main program
if __name__ == '__main__':
    app.run(debug=True)
