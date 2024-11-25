import json
import logging
import mimetypes
import os
import threading
import time

import numpy as np
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# import the logging configuration & create a logger for module
import logging_config

logger = logging.getLogger(__name__)

def extract_features(file_path):
    file_type = mimetypes.guess_type(file_path)[0]
    
    if file_type is None:
        return "Unknown file type"

    if file_type.startswith('text'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    elif file_type.startswith('image'):
        return f"Image file: {os.path.basename(file_path)}"
    elif file_type == 'application/json':
        with open(file_path, 'r') as file:
            return json.dumps(json.load(file))
    else:
        return f"Unsupported file type: {file_type}"

# update dataset & recompute t-SNE
def update_data(file_path):
    global data, feature_matrix
    
    logger.info("Updating data for file: %s", file_path)
    features = extract_features(file_path)
    file_name = os.path.basename(file_path)
    
    rel_path = os.path.relpath(file_path, start='./data')

    data.append({
        'title': file_name,
        'path': rel_path,
        'features': features
    })
    
    logger.debug("Data after update: %s", data)
    
    # update feature matrix
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform([item['features'] for item in data])
    
    # recompute t-SNE
    n_samples = feature_matrix.shape[0]
    perplexity = min(30, n_samples - 1)
    
    if n_samples > 1:
        tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
        tsne_results = tsne.fit_transform(feature_matrix.toarray())
        
        for i, item in enumerate(data):
            item['x'] = float(tsne_results[i, 0])
            item['y'] = float(tsne_results[i, 1])
    else:
        data[0]['x'] = 0.0
        data[0]['y'] = 0.0
    
    logger.debug("Post t-SNE: %s", data)
    
    with open('data.json', 'w') as f:
        json.dump(data, f)
    
    logger.info("Data saved to data.json")

# file system event handler
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            update_data(event.src_path)
            socketio.emit('update', data)

# init data & start watching directory
data = []
feature_matrix = None
path_to_watch = "./data" 

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    logger.info("Index route accessed")
    return "File Mapping Backend @ 5000"

@app.route('/data')
def get_data():
    logger.info("Data route accessed")
    logger.debug("Current data: %s", data)
    return jsonify(data)

@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('./data', filename)

def background_task():
    global data, feature_matrix
    
    logger.info("Starting background task")
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    
    logger.info("Watching directory: %s", path_to_watch)
    
    # Process existing files
    try:
        existing_files = os.listdir(path_to_watch)
        logger.info("Found %d existing files", len(existing_files))
        for filename in existing_files:
            file_path = os.path.join(path_to_watch, filename)
            if os.path.isfile(file_path):
                logger.info("Processing existing file: %s", file_path)
                update_data(file_path)
    except Exception as e:
        logger.error("Error processing existing files: %s", e)
    
    logger.info("Finished processing existing files")
    logger.debug("Current data: %s", data)
    
    try:
        while True:
            sleeptime = 2000
            logger.debug(f"Background task running...(sleep{sleeptime})")
            time.sleep(2000)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Stopping observer.")
        observer.stop()
    except Exception as e:
        logger.error("Unexpected error in background task: %s", e)
    observer.join()

@socketio.on('connect')
def handle_connect():
    logger.info("WebSocket connection established")
    logger.debug("Emitting data: %s", data)
    socketio.emit('update', data)

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    socketio.start_background_task(background_task)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    logger.info("Flask server started.")
