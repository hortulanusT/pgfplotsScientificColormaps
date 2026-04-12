ZENODO_URL  := https://zenodo.org/records/8409685/files/ScientificColourMaps8.zip
ZIP_FILE    := ScientificColourMaps8.zip
SOURCE_DIR  := ScientificColourMaps8
OUTPUT_DIR  := ScientificColourMapsTikz
SCRIPT      := translate_colormaps.py

.PHONY: all download generate test clean

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

## Remove downloaded source data and zip (generated .sty files are kept)
clean:
	rm -rf $(SOURCE_DIR) $(ZIP_FILE)
