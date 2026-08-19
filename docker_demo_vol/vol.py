from pathlib import Path
from datetime import datetime

out = Path("hello.txt")

with out.open("a") as f:
    f.write(f"Hello doctor volume [{datetime.now()}]\n")