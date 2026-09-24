import subprocess, sys
result = subprocess.run(
    [sys.executable, "-c", "print('synthetic lab result')"],
    capture_output=True, text=True, timeout=3, check=True
)
print(result.stdout.strip())
