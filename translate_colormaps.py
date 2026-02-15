#! /usr/bin/python

import itertools
import numpy as np
from pathlib import Path

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET = list(''.join(word) for word in 
             itertools.chain.from_iterable(
                 itertools.product(ALPHABET, repeat = i)
                     for i in range(1, 3)))

org_path = Path("ScientificColourMaps8")
tikz_path = Path("ScientificColourMapsTikz")

tikz_path.mkdir(exist_ok=True)

for colourmap in org_path.iterdir():
  if colourmap.is_dir() and colourmap.stem[0] != "+" and colourmap.stem[-1] != "O":
    print(f"Processing {colourmap}...")

    tikz_sty = tikz_path.joinpath(colourmap.stem).with_suffix(".sty")

    with open(tikz_sty, "w") as f:
      f.write(f"% Generated from https://doi.org/10.5281/zenodo.1243862\n")
      f.write(f"% All credit for creating the colormaps to Fabio Crameri\n")

      f.write(f"\\ProvidesPackage{{{tikz_sty.stem}}}\n\n")

      f.write(f"\\RequirePackage{{xcolor}}\n")
      f.write(f"\\RequirePackage{{pgfplots}}\n\n")

      cmap_data = np.loadtxt(colourmap.joinpath(f"{colourmap.stem}.txt"))

      f.write(f"\\pgfplotsset{{\n")
      f.write(f"  /pgfplots/colormap = {{{colourmap.stem}}}{{\n")
      for row in cmap_data:
        f.write(f"      rgb=({row[0]},{row[1]},{row[2]})\n")
      f.write(f"  }}\n")
      f.write(f"}}\n\n")

      if colourmap.joinpath("DiscretePalettes").exists():
        f.write(f"\\pgfplotsset{{\n")
        for discrete_num in [10,25,50,100]:
          f.write(f"  /pgfplots/colormap = {{{colourmap.stem}{discrete_num}}}{{\n")
          f.write(f"    samples of colormap = {{{discrete_num} of {colourmap.stem}, sample for=const}}\n")
          f.write(f"  }},\n")
        f.write(f"}}\n\n")

      if colourmap.joinpath("CategoricalPalettes").exists():
        categorie_colours = np.loadtxt(colourmap.joinpath("CategoricalPalettes", f"{colourmap.stem}S.txt"))
        
        f.write(f"\\definecolorset{{rgb}}{{{colourmap.stem}}}{{}}{{\n")
        for i_row, row in enumerate(categorie_colours[:-1]):
          f.write(f"  {ALPHABET[i_row]},{row[0]},{row[1]},{row[2]};\n")
        f.write(f"  {ALPHABET[len(categorie_colours)-1]},{categorie_colours[-1][0]},{categorie_colours[-1][1]},{categorie_colours[-1][2]}\n")
        f.write(f"  }}\n\n")

        f.write(f"\\pgfplotscreateplotcyclelist{{{colourmap.stem}}}{{\n")
        for i_row, row in enumerate(categorie_colours[:-1]):
          f.write(f"  {colourmap.stem} {ALPHABET[i_row]},\n")
        f.write(f"  {colourmap.stem} {ALPHABET[len(categorie_colours)-1]}\n")
        f.write(f"}}\n\n")

        f.write(f"\\pgfplotscreateplotcyclelist{{{colourmap.stem} fill}}{{\n")
        for i_row, row in enumerate(categorie_colours[:-1]):
          f.write(f"  {{draw=none, fill={colourmap.stem} {ALPHABET[i_row]}}},\n")
        f.write(f"  {{draw=none, fill={colourmap.stem} {ALPHABET[len(categorie_colours)-1]}}}\n")
        f.write(f"}}\n\n")

        f.write(f"\\pgfplotsset{{\n")
        f.write(f"  every axis/.append style = {{\n")
        f.write(f"    cycle list name = {colourmap.stem}\n")
        f.write(f"  }},\n")
        f.write(f"  bar cycle list/.style = {{\n")
        f.write(f"    cycle list name= {colourmap.stem} fill\n")
        f.write(f"  }},\n")
        f.write(f"  area cycle list/.style = {{\n")
        f.write(f"    cycle list name= {colourmap.stem} fill\n")
        f.write(f"  }},\n")
        f.write(f"  area legend/.style = {{\n")
        f.write(f"    legend image code/.code = {{\n")
        f.write(f"      \\fill[##1] (0cm,-0.1cm) rectangle (0.6cm,0.1cm);\n")
        f.write(f"    }}\n")
        f.write(f"  }},\n")
        f.write(f"  bar legend/.style = {{\n")
        f.write(f"    legend image code/.code = {{\n")
        f.write(f"      \\fill[##1] (0cm,-0.1cm) rectangle (0.6cm,0.1cm);\n")
        f.write(f"    }}\n")
        f.write(f"  }},\n")
        f.write(f"}}\n\n")
        