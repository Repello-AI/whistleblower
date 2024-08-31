# AIChatAutomation.py
import websocket
import json
import ssl
import time
import threading

class AIChatAutomation:
    def __init__(self, host, port=443):
        self.host = host
        self.port = port
        self.ws = None
        self.connected = False
        self.sid = None
        self.user_id = "[HIDDEN]"
        self.client_id = "[HIDDEN]"
        self.access_token = "JWT [HIDDEN]"
        self.last_message_time = 0
        self.response_timeout = 50 
        self.response_received = threading.Event()
        self.last_response = None

    def handle_event(self, message):
        try:
            if message.startswith("/web-channel,"):
                message = message[len("/web-channel,"):]

            data = json.loads(message)
            event = data[0]
            payload = data[1] if len(data) > 1 else None

            if event == "bot.message.reply" and payload:
                if 'message' in payload and 'plainText' in payload['message']:
                    response_text = payload['message']['plainText']['text']
                    print(f"AI: {response_text}")
                    print("-" * 50)
                    self.last_response = response_text
                    self.response_received.set()
                    if hasattr(self, 'wrapper') and self.wrapper:
                        self.wrapper.handle_response(response_text)
                    return response_text
            elif event == "user.message.reply" and payload:
                print(f"You: {payload['messages'][0]['message']['text']}")
                print("-" * 50)

        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e} | Message: {message}")
        except Exception as e:
            print(f"Unexpected error in event handling: {e}")
        
        return None

    def send_message(self, message):
        if not self.ws or not self.connected:
            return None

        self.response_received.clear()
        self.last_response = None
        payload = {
            "userId": self.user_id,
            "clientId": self.client_id,
            "timestamp": self.get_timestamp(),
            "siteUrl": f"https://{self.host}/v2?clientId={self.client_id}",
            "initialUrl": f"https://{self.host}/v2?clientId={self.client_id}",
            "tzOffset": 330,
            "timezone": "Asia/Calcutta",
            "messages": [{
                "message": {
                    "text": message,
                    "autosuggest": {"q": "", "medium": ""}
                },
                "postback": {"text": ""},
                "files": [],
                "hidden": False
            }],
            "appVersion": "4.15.1-v2",
            "accessToken": self.access_token
        }
        self.send_event("user.message.reply", payload)
        if self.response_received.wait(timeout=self.response_timeout):
            return self.last_response
        else:
            print("Response timeout")
            return None

    def get_timestamp(self):
        return time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime())


    def send_event(self, event, payload):
        message = f"42/web-channel,{json.dumps([event, payload])}"
        self.ws.send(message)
        self.last_message_time = time.time()

    def on_message(self, ws, message):
        self.last_message_time = time.time()

        if message.startswith("0"):
            self.handle_handshake(message[1:])
        elif message.startswith("40"):
            self.handle_channel_connection(message[2:])
        elif message.startswith("42"):
            self.handle_event(message[2:])
        elif message == "2":
            self.handle_ping()

    def handle_handshake(self, message):
        try:
            data = json.loads(message)
            self.sid = data.get('sid')
            self.send_channel_connection()
        except json.JSONDecodeError:
            print(f"Failed to parse handshake message: {message}")

    def handle_channel_connection(self, message):
        self.connected = True
        self.send_init_socket()
        self.send_app_check_updates()

    def handle_ping(self):
        self.ws.send("3")

    def on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")
        self.connected = False

    def on_open(self, ws):
        print("WebSocket connection opened")

    def connect(self):
        url = f"wss://{self.host}/socket.io/?EIO=4&transport=websocket"

        self.ws = websocket.WebSocketApp(url,
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close,
                                        header={
                                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                                            "Origin": f"https://{self.host}",
                                            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"
                                        })

        wst = threading.Thread(target=self.ws.run_forever,
                            kwargs={
                                "sslopt": {"cert_reqs": ssl.CERT_NONE},
                                "ping_interval": 25,
                                "ping_timeout": 24  
                            })
        wst.daemon = True
        wst.start()

        timeout = 10
        start_time = time.time()
        while not self.connected and time.time() - start_time < timeout:
            time.sleep(0.1)

        if not self.connected:
            print("Failed to establish WebSocket connection")
            return False
        return True

    def send_channel_connection(self):
        self.ws.send("40/web-channel,")

    def send_init_socket(self):
        payload = {
            "userId": self.user_id,
            "clientId": self.client_id,
            "timestamp": self.get_timestamp(),
            "siteUrl": f"https://{self.host}/v2?clientId={self.client_id}",
            "initialUrl": f"https://{self.host}/v2?clientId={self.client_id}",
            "tzOffset": 330,
            "timezone": "Asia/Calcutta",
            "params": {},
            "attempt": 1,
            "referrer": "",
            "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "accessToken": self.access_token,
            "appVersion": "4.15.1-v2"
        }
        self.send_event("init.socket", payload)

    def send_app_check_updates(self):
        payload = {
            "appVersion": "4.15.1-v2",
            "accessToken": self.access_token
        }
        self.send_event("app.checkUpdates", payload)

if __name__ == "__main__":
    automation = AIChatAutomation("sandbox-chat.leena.ai")

    if automation.connect():
        try:
            while True:
                message = input("Prompt: ")
                if message.lower() == 'quit':
                    break
                automation.send_message(message)
        except KeyboardInterrupt:
            print("Interrupted by user, shutting down...")
        finally:
            if automation.ws:
                automation.ws.close()
    else:
        print("Failed to establish connection. Exiting.")