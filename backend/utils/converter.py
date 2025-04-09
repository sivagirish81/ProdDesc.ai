import logging
from bson import ObjectId

logger = logging.getLogger(__name__)

def deep_safe_stringify(data):
    if isinstance(data, dict):
        return {k: deep_safe_stringify(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_safe_stringify(item) for item in data]
    elif isinstance(data, ObjectId):
        try:
            return str(data)
        except Exception:
            return None
    elif isinstance(data, bytes):
        return data.decode("utf-8", errors="replace")
    elif isinstance(data, str):
        return data.encode("utf-8", errors="surrogatepass").decode("utf-8", errors="surrogatepass")
    else:
        return data
    
def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields in a dictionary to strings."""
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        try:
            logger.info(f"Converting ObjectId to string: {data}")
            return str(data)
        except Exception as e:
            return deep_safe_stringify(data)
    return data

def safe_text(text: str) -> str:
    return text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")

def sanitize_unicode(input_str: str) -> str:
    """Remove invalid Unicode characters from a string."""
    return input_str.encode("utf-8", "ignore").decode("utf-8")

def remove_invalid_unicode(text: str) -> str:
    return ''.join(c for c in text if not '\ud800' <= c <= '\udfff')