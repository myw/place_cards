# Place Cards Utility

Given a template SVG file (like `place_cards/template.svg`), and a CSV spreadsheet
of names, tables, and food choices (like `example_data/guests.csv`), automatically
generate a pdf of place cards for everyone in the spreadsheet that is ready to be
printed and cut.

## Installation

- Make sure you have [Inkscape](https://inkscape.org/) installed on your system
- `pip` should take care of the other dependencies

## Usage

See `place_cards.py --help`. Can also use as a library: `import place_cards`, then
call `place_cards.make_place_cards(...)`.

## Extension

The template can be edited in Inkscape without any issues. The syntax is
`{{ thing.n }}` to replace the text with the _n_th card's thing: name, table, or
food color (as a hex-value).
Just be sure to maintain the color-code mappings by position. Anything you want
colored by food preference should be set as the appropriate position's color:
red for position 0, green for position 1, etc.

To see the full color mapping values, look at `food_colors` in
`_process_spreadsheet`, and `template_colors` in `_preprocess_template`.

