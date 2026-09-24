import hashlib
text = "lab evidence"
data = text.encode("utf-8")
print(data.decode("utf-8"))
print(hashlib.sha256(data).hexdigest())
