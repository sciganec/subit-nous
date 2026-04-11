import subprocess
import tempfile
from pathlib import Path

# Create temp file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
    f.write("I think logically about the east in spring")
    temp_file = f.name

print(f"Temp file: {temp_file}")

# Run analysis
result = subprocess.run(
    ["nous", "analyze", temp_file, "--output", "test_cli_out"],
    capture_output=True,
    text=True
)

print(f"Return code: {result.returncode}")
print(f"STDOUT:\n{result.stdout}")
print(f"STDERR:\n{result.stderr}")

# Cleanup
Path(temp_file).unlink()