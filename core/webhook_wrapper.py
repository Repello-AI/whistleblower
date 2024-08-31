# core/webhook_wrapper.py

import sys
import os
import time
import threading

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from AIChatAutomation import AIChatAutomation

class WebhookWrapper:
    def __init__(self, host):
        self.host = host
        self.automation = None
        self.response = None
        self.response_event = threading.Event()
        self.connection_lock = threading.Lock()
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.message_timeout = 50  # seconds

    def connect(self):
        with self.connection_lock:
            if self.automation is None or not self.automation.connected:
                for attempt in range(self.max_retries):
                    try:
                        self.automation = AIChatAutomation(self.host)
                        self.automation.wrapper = self  # Set the wrapper reference
                        if self.automation.connect():
                            print(f"Connected successfully on attempt {attempt + 1}")
                            return True
                    except Exception as e:
                        print(f"Connection attempt {attempt + 1} failed: {str(e)}")
                    
                    if attempt < self.max_retries - 1:
                        print(f"Retrying in {self.retry_delay} seconds...")
                        time.sleep(self.retry_delay)
                
                print("Failed to connect after multiple attempts")
                return False
            return True

    def send_message(self, message):
        if not self.connect():
            raise ConnectionError("Failed to establish a connection")

        for attempt in range(self.max_retries):
            self.response = None
            self.response_event.clear()

            try:
                self.automation.send_message(message)
                if self.response_event.wait(timeout=self.message_timeout):
                    return self.response
                else:
                    print(f"Response timeout on attempt {attempt + 1}")
            except Exception as e:
                print(f"Error sending message on attempt {attempt + 1}: {str(e)}")

            if attempt < self.max_retries - 1:
                print(f"Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                if not self.connect():
                    raise ConnectionError("Failed to re-establish connection")

        raise TimeoutError("Response timeout after multiple attempts")

    def handle_response(self, response):
        self.response = response
        self.response_event.set()

    def close(self):
        with self.connection_lock:
            if self.automation and self.automation.ws:
                self.automation.ws.close()
            self.automation = None

# Monkey-patch the AIChatAutomation class to handle responses
original_handle_event = AIChatAutomation.handle_event

def patched_handle_event(self, message):
    result = original_handle_event(self, message)
    if hasattr(self, 'wrapper') and self.wrapper:
        self.wrapper.handle_response(result)
    return result

AIChatAutomation.handle_event = patched_handle_event