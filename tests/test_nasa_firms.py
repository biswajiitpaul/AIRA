from pathlib import Path
import csv


def test_nasa_firms_fixture():
    fixture = Path("fixtures/nasa_firms.csv")

    assert fixture.exists()

    with fixture.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        assert reader.fieldnames is not None
        assert "latitude" in reader.fieldnames
        assert "longitude" in reader.fieldnames
        assert "acq_date" in reader.fieldnames
        assert "acq_time" in reader.fieldnames