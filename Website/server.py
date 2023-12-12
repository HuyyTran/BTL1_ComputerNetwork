import threading
from flask import jsonify

# Server class that encapsulates the server operations
class FileServer:
    def __init__(self):
        self.running = False
        self.server_thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.server_thread = threading.Thread(target=self.run)
            self.server_thread.start()
            return jsonify({"message": "Server is starting..."}), 200
        else:
            return jsonify({"message": "Server is already running."}), 300

    def stop(self):
        if self.running:
            self.running = False
            self.server_thread.join()
            return jsonify({"message": "Server is stopping..."}), 200
        else:
            return jsonify({"message": "Server is not running."}), 300

    def run(self):
        while self.running:
            # This is where the server would listen for connections and handle requests
            pass  # Replace with actual server logic

# Create a global server instance
file_server = FileServer()