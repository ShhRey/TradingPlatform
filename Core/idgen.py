import uuid, secrets

# Function for creating Unique UserIDs for Different Users
def useridgen():
    return 'TK-' + uuid.uuid4().hex[:6].upper()

# Function for creating Unique IDs for different Items
def itemidgen():
    return uuid.uuid4().hex[:8].upper()

# Function for creating Unique Tokens
def gentoken():
    return secrets.token_hex(10)

# Function to generate transaction id
def transid():
    return uuid.uuid4().hex[:10].upper()