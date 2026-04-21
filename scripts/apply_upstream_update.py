#!/usr/bin/env python3
"""Apply upstream Scientific Colour Maps metadata update to local files.

Reads new version data from environment variables and patches translate_colormaps.py,
Makefile, and README.md in-place.

Required environment variables:
  LATEST_VERSION, LATEST_DOI, LATEST_DATE_ISO, LATEST_DATE_SLASH,
  LATEST_ZIP_URL, LATEST_ZIP_FILENAME, LATEST_SOURCE_DIR, CITATION_YEAR
"""

import os
import re
from pathlib import Path


def main():
    latest_version = os.environ["LATEST_VERSION"]
    latest_doi = os.environ["LATEST_DOI"]
    latest_date_iso = os.environ["LATEST_DATE_ISO"]
    latest_date_slash = os.environ["LATEST_DATE_SLASH"]
    latest_zip_url = os.environ["LATEST_ZIP_URL"]
    latest_zip_filename = os.environ["LATEST_ZIP_FILENAME"]
    latest_source_dir = os.environ["LATEST_SOURCE_DIR"]
    citation_year = os.environ["CITATION_YEAR"]

    # --- translate_colormaps.py ---
    translate_path = Path("translate_colormaps.py")
    translate_text = translate_path.read_text(encoding="utf-8")
    translate_text = re.sub(
        r'SCIENTIFIC_COLOUR_MAPS_VERSION = "[^"]+"',
        f'SCIENTIFIC_COLOUR_MAPS_VERSION = "{latest_version}"',
        translate_text,
    )
    translate_text = re.sub(
        r'SCIENTIFIC_COLOUR_MAPS_DATE = "[^"]+"',
        f'SCIENTIFIC_COLOUR_MAPS_DATE = "{latest_date_slash}"',
        translate_text,
    )
    translate_text = re.sub(
        r'SCIENTIFIC_COLOUR_MAPS_VERSION_DOI = "[^"]+"',
        f'SCIENTIFIC_COLOUR_MAPS_VERSION_DOI = "{latest_doi}"',
        translate_text,
    )
    translate_path.write_text(translate_text, encoding="utf-8")

    # --- Makefile ---
    makefile_path = Path("Makefile")
    makefile_text = makefile_path.read_text(encoding="utf-8")
    makefile_text = re.sub(
        r'^ZENODO_URL\s*:=\s*.*$',
        f'ZENODO_URL  := {latest_zip_url}',
        makefile_text,
        flags=re.MULTILINE,
    )
    makefile_text = re.sub(
        r'^ZIP_FILE\s*:=\s*.*$',
        f'ZIP_FILE    := {latest_zip_filename}',
        makefile_text,
        flags=re.MULTILINE,
    )
    makefile_text = re.sub(
        r'^SOURCE_DIR\s*:=\s*.*$',
        f'SOURCE_DIR  := {latest_source_dir}',
        makefile_text,
        flags=re.MULTILINE,
    )
    makefile_path.write_text(makefile_text, encoding="utf-8")

    # --- README.md ---
    readme_path = Path("README.md")
    readme_text = readme_path.read_text(encoding="utf-8")
    readme_text = re.sub(
        r'\| Scientific Colour Maps \| [^|]+ \| [^|]+ \|',
        f'| Scientific Colour Maps | {latest_version} | {latest_date_iso} |',
        readme_text,
    )
    readme_text = re.sub(
        r'\| Zenodo DOI \| \[10\.5281/zenodo\.[0-9]+\]\(https://doi\.org/10\.5281/zenodo\.[0-9]+\) \| \|',
        f'| Zenodo DOI | [{latest_doi}](https://doi.org/{latest_doi}) | |',
        readme_text,
    )
    readme_text = re.sub(
        r'> Crameri, F\. \([0-9]{4}\)\. Scientific colour maps \([^)]+\)\. Zenodo\.',
        f'> Crameri, F. ({citation_year}). Scientific colour maps ({latest_version}). Zenodo.',
        readme_text,
    )
    readme_text = re.sub(
        r'> https://doi\.org/10\.5281/zenodo\.[0-9]+',
        f'> https://doi.org/{latest_doi}',
        readme_text,
    )
    readme_path.write_text(readme_text, encoding="utf-8")

    print(f"Updated files to version {latest_version} ({latest_doi})")


if __name__ == "__main__":
    main()
