import uuid

def get_next_id():
    return str(uuid.uuid4()).replace("-", "")