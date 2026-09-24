from urllib.parse import urlsplit, urlencode
u = urlsplit("https://lab.test:8443/help?q=hello")
print(u.scheme, u.hostname, u.port, u.path)
print(urlencode({"q": "hello lab", "page": 1}))
