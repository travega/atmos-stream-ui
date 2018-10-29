from flask import Flask
from flask import render_templates
import os
import kafka_helper
import json
import asyncio
import websockets

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

topic = "{}temp".format(os.environ["KAFKA_PREFIX"])
consumer = kafka_helper.get_kafka_consumer(topic=topic)
print ("Connected")

async def echo(websocket, path):
    # async for message in websocket:
    for message in consumer:
        print (message)
        await websocket.send(json.dumps(message.value))

asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
