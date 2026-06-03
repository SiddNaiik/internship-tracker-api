import os
import subprocess
import sys


def main() -> None:
    port = os.getenv("PORT", "8000")

    # migrate
    result = subprocess.call([sys.executable, "-m", "alembic", "upgrade", "head"])
    if result != 0:
        raise SystemExit(result)

    # serve
    raise SystemExit(
        subprocess.call(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                port,
            ]
        )
    )


if __name__ == "__main__":
    main()