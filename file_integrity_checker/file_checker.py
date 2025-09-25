
import hashlib
import os
import json

HASH_FILE = "hash_records.json"

def calculate_hash(file_path, algo="sha256"):
    hash_func = hashlib.new(algo)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def load_hash_records():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hash_records(records):
    with open(HASH_FILE, "w") as f:
        json.dump(records, f, indent=4)

def check_files(directory, algo="sha256"):
    records = load_hash_records()
    changes = {"modified": [], "new": [], "deleted": []}

    current_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            current_files[path] = calculate_hash(path, algo)

    for path, hash_val in current_files.items():
        if path in records:
            if records[path] != hash_val:
                changes["modified"].append(path)
        else:
            changes["new"].append(path)

    for path in records:
        if path not in current_files:
            changes["deleted"].append(path)

    save_hash_records(current_files)
    return changes

def main():
    directory = input("Enter directory to monitor: ")
    algo = input("Enter hash algorithm (md5/sha1/sha256): ").lower()

    print(f"Checking files in {directory} using {algo}...")
    changes = check_files(directory, algo)

    if not any(changes.values()):
        print("No changes detected.")
    else:
        for change_type, files in changes.items():
            if files:
                print(f"\n{change_type.upper()}:")
                for file in files:
                    print(f" - {file}")

if __name__ == "__main__":
    main()
