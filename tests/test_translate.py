from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import translate_colormaps


SOURCE_DIR = REPO_ROOT / "ScientificColourMaps8"


def selected_source_directories():
    return [
        path for path in sorted(SOURCE_DIR.iterdir(), key=lambda path: path.name)
        if translate_colormaps.should_generate(path)
    ]


def discrete_variants_for(colourmap_dir):
    discrete_dir = colourmap_dir / "DiscretePalettes"
    if not discrete_dir.exists():
        return []

    pattern = re.compile(rf"^{re.escape(colourmap_dir.name)}(\d+)\.txt$")
    variants = []

    for path in sorted(discrete_dir.glob("*.txt")):
        match = pattern.match(path.name)
        if match:
            variants.append(match.group(1))

    return variants


def test_generated_file_set_matches_selected_source_directories(tmp_path):
    translate_colormaps.generate_styles(SOURCE_DIR, tmp_path)

    expected = {path.name for path in selected_source_directories()}
    generated = {path.stem for path in tmp_path.glob("*.sty")}

    assert generated == expected

    for source_path in SOURCE_DIR.iterdir():
        if source_path.is_dir() and not translate_colormaps.should_generate(source_path):
            assert not (tmp_path / f"{source_path.name}.sty").exists()


def test_generated_styles_match_discrete_variants_in_source(tmp_path):
    translate_colormaps.generate_styles(SOURCE_DIR, tmp_path)

    for colourmap_dir in selected_source_directories():
        colourmap = colourmap_dir.name
        style_file = tmp_path / f"{colourmap}.sty"
        content = style_file.read_text(encoding="utf-8")

        assert style_file.stat().st_size > 0
        assert (
            f"% Generated from Scientific Colour Maps "
            f"{translate_colormaps.SCIENTIFIC_COLOUR_MAPS_VERSION} "
            f"(https://doi.org/{translate_colormaps.SCIENTIFIC_COLOUR_MAPS_VERSION_DOI})"
        ) in content
        assert (
            f"% Parent DOI: https://doi.org/"
            f"{translate_colormaps.SCIENTIFIC_COLOUR_MAPS_PARENT_DOI}"
        ) in content
        assert (
            f"\\ProvidesPackage{{{colourmap}}}"
            f"[{translate_colormaps.SCIENTIFIC_COLOUR_MAPS_DATE} "
            f"Scientific Colour Maps {translate_colormaps.SCIENTIFIC_COLOUR_MAPS_VERSION}]"
        ) in content
        assert "\\RequirePackage{xcolor}" in content
        assert "\\RequirePackage{pgfplots}" in content
        assert f"/pgfplots/colormap = {{{colourmap}}}" in content

        variants = discrete_variants_for(colourmap_dir)
        if variants:
            assert "samples of colormap" in content
            for variant in variants:
                assert f"/pgfplots/colormap = {{{colourmap}{variant}}}" in content
                assert f"samples of colormap = {{{variant} of {colourmap}, sample for=const}}" in content
        else:
            assert "samples of colormap" not in content


def test_generated_styles_match_categorical_variants_in_source(tmp_path):
    translate_colormaps.generate_styles(SOURCE_DIR, tmp_path)

    for colourmap_dir in selected_source_directories():
        colourmap = colourmap_dir.name
        content = (tmp_path / f"{colourmap}.sty").read_text(encoding="utf-8")
        categorical_source = colourmap_dir / "CategoricalPalettes" / f"{colourmap}S.txt"

        if categorical_source.exists():
            assert f"\\definecolorset{{rgb}}{{{colourmap}}}" in content
            assert f"\\pgfplotscreateplotcyclelist{{{colourmap}}}" in content
            assert f"\\pgfplotscreateplotcyclelist{{{colourmap} fill}}" in content
        else:
            assert "\\definecolorset" not in content
            assert "\\pgfplotscreateplotcyclelist" not in content