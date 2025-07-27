import csv
from firebase_config import db
import os

def is_image_field(key, value):
    """
    Returns True if the field is likely to be an image/binary field.
    Checks for common keys and value types.
    """
    key_lower = key.lower()
    if any(x in key_lower for x in ['image', 'img', 'photo', 'picture', 'file', 'base64']):
        return True
    if isinstance(value, (bytes, bytearray)):
        return True
    # Exclude long base64-like strings
    if isinstance(value, str) and len(value) > 200 and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in value[:100]):
        return True
    return False

def flatten_dict(d, parent_key='', sep='.'):
    """Recursively flattens a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif not is_image_field(new_key, v):
            items.append((new_key, v))
    return dict(items)

def export_all_collections_to_csv(output_dir='firestore_exports'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    collections = db.collections()
    for collection in collections:
        collection_name = collection.id
        docs = collection.stream()
        rows = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            flat = flatten_dict(data)
            rows.append(flat)
        if not rows:
            continue
        fieldnames = sorted({k for row in rows for k in row})
        csv_path = os.path.join(output_dir, f'{collection_name}.csv')
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Exported {len(rows)} docs from collection '{collection_name}' to {csv_path}")

def append_to_csv(collection_name, data_dict, output_dir='firestore_exports'):
    """
    Appends a new row to the collection's CSV, excluding image/binary fields.
    Creates the CSV with headers if it does not exist.
    """
    import os
    import csv
    flat = {k: v for k, v in flatten_dict(data_dict).items() if not is_image_field(k, v)}
    csv_path = os.path.join(output_dir, f'{collection_name}.csv')
    os.makedirs(output_dir, exist_ok=True)
    file_exists = os.path.isfile(csv_path)
    fieldnames = list(flat.keys())
    if file_exists:
        # Read existing fieldnames from file header
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            existing_fields = next(reader, [])
        # Merge new fields if any
        all_fields = list(dict.fromkeys(existing_fields + fieldnames))
        if set(all_fields) != set(existing_fields):
            # Rewrite file with new headers if new fields found
            import pandas as pd
            df = pd.read_csv(csv_path)
            for fn in fieldnames:
                if fn not in df.columns:
                    df[fn] = ''
            df = df[all_fields]
            df.to_csv(csv_path, index=False)
        fieldnames = all_fields
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(flat)
    print(f"Appended new row to {csv_path}")

if __name__ == '__main__':
    export_all_collections_to_csv()
