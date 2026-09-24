def valid_port(value):
    return type(value) is int and 1 <= value <= 65535

for value in [443, 0, "443", True]:
    print(repr(value), valid_port(value))
