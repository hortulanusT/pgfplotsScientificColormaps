# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [1.0.0] — 2026-04-12

### Added
- Initial tracked release.
- `translate_colormaps.py` generates 35 PGFplots `.sty` files from the
  upstream Scientific Colour Maps data.
- `arealegendstyle.sty` for enhanced PGFplots legend styling.
- `test.tex` demonstrating surface plots, discrete colormaps, line cycles,
  stacked area charts, and grouped bar charts.
- `LICENSE` (MIT) for the translation tooling.
- `requirements.txt` documenting the `numpy` dependency.
- `Makefile` with `download`, `generate`, and `test` targets.
- CLI arguments (`--input`, `--output`) for `translate_colormaps.py`.
- GitHub Actions CI: Python (pytest) and LaTeX (latexmk) jobs.

### Source data
- Scientific Colour Maps **8.0.1** by Fabio Crameri
  ([DOI 10.5281/zenodo.8409685](https://doi.org/10.5281/zenodo.8409685),
  released 2023-10-05).
- Cyclic/omnidirectional variants (`bamO`, `brocO`, `corkO`, `romaO`, `vikO`)
  are intentionally excluded from generation.
