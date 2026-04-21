#!/usr/bin/env python3
"""Detect whether a new upstream Scientific Colour Maps release is available on Zenodo.

Writes step outputs to $GITHUB_OUTPUT (update_needed, latest_version, latest_doi,
latest_date_iso, latest_date_slash, latest_zip_url, latest_zip_filename,
latest_source_dir, citation_year, parent_doi).
"""

import json
import os
import re
import urllib.request
from pathlib import Path

CONCEPT_RECORD_ID = "1243862"
PARENT_DOI = "10.5281/zenodo.1243862"


def main():
    url = f"https://zenodo.org/api/records/{CONCEPT_RECORD_ID}/versions/latest"
    with urllib.request.urlopen(url, timeout=30) as resp:
        record = json.load(resp)

    metadata = record.get("metadata", {})
    latest_version = metadata.get("version", "")
    latest_doi = record.get("doi", "")
    publication_date = metadata.get("publication_date", "")

    if not latest_version or not latest_doi or not publication_date:
        raise SystemExit("Latest Zenodo record is missing version/doi/publication_date")

    if not re.match(r'^\d+(\.\d+)*$', latest_version):
        raise SystemExit(f"Unexpected version format: {latest_version!r}")

    record_id = record.get("id")
    major_version = latest_version.split(".")[0]
    zip_filename = f"ScientificColourMaps{major_version}.zip"
    source_dir = f"ScientificColourMaps{major_version}"
    zip_url = f"https://zenodo.org/records/{record_id}/files/{zip_filename}"

    text = Path("translate_colormaps.py").read_text(encoding="utf-8")
    match_version = re.search(r'SCIENTIFIC_COLOUR_MAPS_VERSION = "([^"]+)"', text)
    match_doi = re.search(r'SCIENTIFIC_COLOUR_MAPS_VERSION_DOI = "([^"]+)"', text)
    if not match_version or not match_doi:
        raise SystemExit("Could not parse current version/doi from translate_colormaps.py")
    current_version = match_version.group(1)
    current_doi = match_doi.group(1)

    update_needed = (latest_version != current_version) or (latest_doi != current_doi)

    year, month, day = publication_date.split("-")
    date_slash = f"{year}/{month}/{day}"
    citation_year = year

    output_path = os.environ["GITHUB_OUTPUT"]
    with open(output_path, "a", encoding="utf-8") as fh:
        fh.write(f"update_needed={'true' if update_needed else 'false'}\n")
        fh.write(f"latest_version={latest_version}\n")
        fh.write(f"latest_doi={latest_doi}\n")
        fh.write(f"latest_date_iso={publication_date}\n")
        fh.write(f"latest_date_slash={date_slash}\n")
        fh.write(f"latest_zip_url={zip_url}\n")
        fh.write(f"latest_zip_filename={zip_filename}\n")
        fh.write(f"latest_source_dir={source_dir}\n")
        fh.write(f"citation_year={citation_year}\n")
        fh.write(f"parent_doi={PARENT_DOI}\n")

    print(f"Current: version={current_version}, doi={current_doi}")
    print(f"Latest:  version={latest_version}, doi={latest_doi}, date={publication_date}")
    print(f"Update needed: {update_needed}")


if __name__ == "__main__":
    main()
