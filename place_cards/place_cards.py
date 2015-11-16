#!/usr/bin/env python

from __future__ import division

from argparse import ArgumentParser
import csv
import itertools
import os
import re
import shutil
import subprocess
import tempfile

import jinja2
from PyPDF2 import PdfFileMerger


def make_place_cards(spreadsheet_path, template_path, output_path,
                     keep_output=False, output_dir=None, inkscape_path='inkscape'):
  """ Main entry point """
  if output_dir is None:
    output_dir = tempfile.mkdtemp()

  if output_path is None:
    output_path = _default_output_path(spreadsheet_path)

  with open(spreadsheet_path) as spreadsheet, open(template_path) as template:
   guest_info = _process_spreadsheet(spreadsheet)
   _write_place_cards(guest_info, jinja2.Template(_preprocess_template(template.read())),
                      output_path, output_dir, inkscape_path)
   if not keep_output:
     shutil.rmtree(output_dir)


def _default_output_path(spreadsheet_path):
  name, ext = os.path.splitext(spreadsheet_path)
  return name + '.pdf'


def _process_spreadsheet(spreadsheet):
  cards_per_sheet = 6

  # http://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python
  def grouper(n, iterable):
    """ Group an iterable into chunks of n """
    it = iter(iterable)
    while True:
      chunk = list(itertools.islice(it, n))

      if not chunk:
        return

      if len(chunk) < n:
        # Repeat the last value to fill the last chunk
        chunk.extend([chunk[-1]] * (n - len(chunk)))

      yield tuple(chunk)

  food_colors = {
    'salmon': '#ffaaaa',
    'pork': '#5f8dd3',
    'kids': '#ddafe9',
    'veggie': '#5fd38d',
  }

  return [
    # Standardize the guest info here
    {
      'names': [guest['Name'] for guest in sheet],
      'tables': [guest['Table'] for guest in sheet],
      'colors': [food_colors[guest['Food'].lower()] for guest in sheet],
    }
    for sheet in grouper(cards_per_sheet, csv.DictReader(spreadsheet))
  ]


def _write_place_cards(guest_info, template, output_path, output_dir, inkscape_path):

  dirnames = {}
  for filetype in ('svg', 'pdf'):
    dirnames[filetype] = os.path.join(output_dir, filetype)
    try:
      os.makedirs(dirnames[filetype])
    except OSError:
      pass

  merger = PdfFileMerger()
  for ix, sheet in enumerate(guest_info, start=1):
    filename_base = 'place_cards-{0}.'.format(ix)

    filenames = {}
    for filetype in ('svg', 'pdf'):
      filenames[filetype] = os.path.join(dirnames[filetype], filename_base + filetype)

    with open(filenames['svg'], 'w+') as svg:
      svg.write(template.render(sheet))

    _convert_to_pdf(inkscape_path, filenames['svg'], filenames['pdf'])
    merger.append(filenames['pdf'])

  merger.write(output_path)


def _convert_to_pdf(inkscape_path, svg_filename, pdf_filename):
  subprocess.call([inkscape_path,
                   '--export-pdf=' + os.path.abspath(pdf_filename),
                   os.path.abspath(svg_filename)])


def _preprocess_template(template_string):
  """
  Manipulate the template file before rendering the template, returning a new
  string.

  This allows us to replace colors with Jinja variable names, for example.
  """
  template_colors = ('#ff0000', '#00ff00', '#0000ff',
                     '#800000', '#008000', '#000080')

  for index, color in enumerate(template_colors):
    template_string = re.sub(color, '{{{{ colors.{0} }}}}'.format(index), template_string)

  return template_string


if __name__ == '__main__':
  parser = ArgumentParser(
    description='Process a template svg file to make place cards for everyone',
  )
  parser.add_argument('spreadsheet_path',
                      help='a .csv file of names, food choices, and table numbers for all guests')
  parser.add_argument('-t', '--template', dest='template_path', default='template.svg',
                      help="the template filename; defaults to 'template.svg'")
  parser.add_argument('-o', '--output', dest='output_path', default=None,
                      help='the name of the final, merged output file; '
                           + 'defaults to the same name as the .csv')
  parser.add_argument('--keep', dest='keep_output', action='store_true',
                      help='keep the files in the output directory')
  parser.add_argument('--output_dir', default=None,
                      help='the directory to place generated svgs; defaults to a tmp directory')
  parser.add_argument('--inkscape', dest='inkscape_path', default='inkscape',
                      help="path to the Inkscape executable; defaults to 'inkscape'")

  args = parser.parse_args()
  make_place_cards(**args.__dict__)