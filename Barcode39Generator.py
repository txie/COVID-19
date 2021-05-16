import uuid

for _ in range(30):
    x = str(uuid.uuid4()).upper().replace('-', '')
    print(x[:13])