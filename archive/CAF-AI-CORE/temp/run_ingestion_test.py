import subprocess
from pathlib import Path


def test_ingest_pages_json():
    path = Path("knowledge/insights/imu_pages_torino.json")
    assert path.exists(), f"Missing test file: {path}"

    result = subprocess.run(
        [
            "python",
            "knowledge_ingestion/run_ingestion_crew.py",
            "--file",
            str(path),
            "--topic",
            "imu",
            "--region",
            "torino",
            "--brand",
            "CAF",
        ],
        capture_output=True,
        text=True,
    )

    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    assert result.returncode == 0
    assert "✅" in result.stdout or "[✓]" in result.stdout
