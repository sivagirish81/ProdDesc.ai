from bson import ObjectId

def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields in a dictionary to strings."""
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

def safe_text(text: str) -> str:
    return text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")

def sanitize_unicode(input_str: str) -> str:
    """Remove invalid Unicode characters from a string."""
    return input_str.encode("utf-8", "ignore").decode("utf-8")

def remove_invalid_unicode(text: str) -> str:
    return ''.join(c for c in text if not '\ud800' <= c <= '\udfff')