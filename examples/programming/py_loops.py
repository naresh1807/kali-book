statuses = [200, 404, 403, 200]
for code in statuses:
    if code >= 400:
        print("Review:", code)
