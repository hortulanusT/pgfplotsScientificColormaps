ZENODO_URL  := https://zenodo.org/records/8409685/files/ScientificColourMaps8.zip
ZIP_FILE    := ScientificColourMaps8.zip
SOURCE_DIR  := ScientificColourMaps8
OUTPUT_DIR  := ScientificColourMapsTikz
SCRIPT      := translate_colormaps.py
PREVIEW_DIR := docs

.PHONY: all download generate test preview-images clean

all: download generate

## Download and extract the upstream Scientific Colour Maps data from Zenodo
download: $(SOURCE_DIR)

$(ZIP_FILE):
	curl -fSL --progress-bar -o $(ZIP_FILE) $(ZENODO_URL)

$(SOURCE_DIR): $(ZIP_FILE)
	unzip -q -o $(ZIP_FILE) -d $(SOURCE_DIR)

## Generate PGFplots .sty files from the source data
generate: $(SOURCE_DIR)
	python $(SCRIPT) --input $(SOURCE_DIR) --output $(OUTPUT_DIR)

## Run the Python test suite
test:
	pytest tests/ -v

## Build test.pdf and regenerate all README preview images from test.tex
preview-images: test.pdf
	mkdir -p $(PREVIEW_DIR)
	pdftoppm -png -singlefile -f 1 -l 1 -scale-to 1800 test.pdf $(PREVIEW_DIR)/test-preview-continuous
	pdftoppm -png -singlefile -f 2 -l 2 -scale-to 1800 test.pdf $(PREVIEW_DIR)/test-preview-discrete
	pdftoppm -png -singlefile -f 3 -l 3 -scale-to 1800 test.pdf $(PREVIEW_DIR)/test-preview-line
	pdftoppm -png -singlefile -f 4 -l 4 -scale-to 1800 test.pdf $(PREVIEW_DIR)/test-preview-area
	pdftoppm -png -singlefile -f 5 -l 5 -scale-to 1800 test.pdf $(PREVIEW_DIR)/test-preview-bar

test.pdf: test.tex
	latexmk -pdf -interaction=nonstopmode -halt-on-error test.tex

## Remove downloaded source data and zip (generated .sty files are kept)
clean:
	rm -rf $(SOURCE_DIR) $(ZIP_FILE)
