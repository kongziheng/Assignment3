import socket
import sys
import time

MAX_RETRIES = 3
RETRY_DELAY = 1  

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <request_file>")
        sys.exit(1)
    hostname, port, file_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(' ', 2) 
                if len(parts) < 2 or len(parts) > 3:
                    print(f"Invalid format: {line}")
                    continue
                cmd, key = parts[0], parts[1]
                value = parts[2] if len(parts) == 3 else None

                collated = f"{key} {value}" if value else key
                if len(collated) > 970:
                    print(f"Error: collated size exceeds 970 characters in {line}")
                    continue
                if cmd == 'PUT':
                    request = f"{len(f'P {key} {value}'):03d} P {key} {value}"
                elif cmd in ('READ', 'GET'):
                    request = f"{len(f'{cmd[0]} {key}'):03d} {cmd[0]} {key}"
                else:
                    print(f"Invalid command: {cmd} in {line}")
                    continue
                retries = 0
                while retries < MAX_RETRIES:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((hostname, port))
                            s.sendall(request.encode('utf-8'))

                            response = receive_full_response(s)
                            if not response:
                                print(f"Connection lost while processing {line}, retrying ({retries + 1}/{MAX_RETRIES})...")
                                retries += 1
                                time.sleep(RETRY_DELAY)
                                continue

                            print(f"{line}: {response[4:]}")
                            break
                    except Exception as e:
                        print(f"Client error while processing {line}: {e}, retrying ({retries + 1}/{MAX_RETRIES})...")
                        retries += 1
                        time.sleep(RETRY_DELAY)

                if retries == MAX_RETRIES:
                    print(f"Failed to process {line} after {MAX_RETRIES} retries.")
