import json

# NEW USERS TO JSON
async def ToJson(user, path):
    with open(path, 'w') as file:
        json.dump(user, file)      
