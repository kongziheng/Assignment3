class TupleSpace:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}

    def read(self, key):
        with self.lock:
            return self.data.get(key, None)

    def get(self, key):
        with self.lock:
            return self.data.pop(key, None)

    def put(self, key, value):
        with self.lock:
            if key in self.data:
                return False
            self.data[key] = value
            return True
class Statistics:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_clients = 0
        self.total_operations = 0
        self.read_count = 0
        self.get_count = 0
        self.put_count = 0
        self.errors = {'exists': 0, 'not_exists': 0}
        self.total_key_length = 0
        self.total_value_length = 0
        self.tuple_count = 0
 def increment_clients(self):
        with self.lock:
            self.total_clients += 1

    def increment_ops(self, op_type):
        with self.lock:
            self.total_operations += 1
            if op_type == 'READ':
                self.read_count += 1
            elif op_type == 'GET':
                self.get_count += 1
            elif op_type == 'PUT':
                self.put_count += 1

    def add_error(self, error_type):
        with self.lock:
            if error_type == 'exists':
                self.errors['exists'] += 1
            elif error_type == 'not_exists':
                self.errors['not_exists'] += 1

    def record_tuple_addition(self, key, value):
        with self.lock:
            self.total_key_length += len(key)
            self.total_value_length += len(value)
            self.tuple_count += 1

    def record_tuple_removal(self, key, value):
        with self.lock:
            self.total_key_length -= len(key)
            self.total_value_length -= len(value)
            self.tuple_count -= 1
            def handle_client(client_socket, tuple_space, stats):
    try:
        while True:
            # 接收头部长度
            header = b''
            while len(header) < 3:
                chunk = client_socket.recv(3 - len(header))
                if not chunk:
                    break
                header += chunk
            if len(header) != 3:
                break
            msg_length = int(header.decode())

            # 接收消息体
            message_body = b''
            remaining = msg_length
            while remaining > 0:
                chunk = client_socket.recv(remaining)
                if not chunk:
                    break
                message_body += chunk
                remaining -= len(chunk)
            if remaining > 0:
                break

            # 解析指令
            message_body = message_body.decode()
            parts = message_body.split(' ', 2)
            if len(parts) < 2:
                continue
            command = parts[0]
            key = parts[1] if len(parts) > 1 else ""
            value = parts[2] if len(parts) > 2 else ""

            response = ""
            if command == 'P':
                ...
            elif command == 'G':
                ...
            elif command == 'R':
                ...
            else:
                response = "ERR invalid command"

            response_length = f"{len(response):03d}"
            full_response = f"{response_length}{response}".encode()
            client_socket.sendall(full_response)
    except Exception as e:
        print(f"Client error: {e}")
    finally:
        client_socket.close()
def print_stats(stats, stop_event):
    while not stop_event.is_set():
        time.sleep(10)
        with stats.lock:
            print("\n=== Server Statistics ===")
            ...
            def main():
    port = 51234
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.listen(5)
        print(f"Server listening on port {port}")

        tuple_space = TupleSpace()
        stats = Statistics()
        stop_event = threading.Event()
        ...
        while True:
            client_socket, addr = server_socket.accept()
            stats.increment_clients()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, tuple_space, stats),
                daemon=True
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        stop_event.set()
    finally:
        if server_socket:
            server_socket.close()
        print("Server stopped. Exit code 0.")

