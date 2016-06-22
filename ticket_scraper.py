#!/usr/bin/env python

"""
ticket_scraper.py

Scrapes some data from given directory containing Deutsche Bahn Online-Tickets,
writes all of it to a single CSV file. Useful for evaluating travel expenses 
over time and maybe more. 
"""

import os
import sys
import glob
import pdfquery
import unicodecsv

try:
  directory_name = sys.argv[1]
  os.chdir(directory_name)
  print(os.getcwd())
except:
  print(os.getcwd())

result_csv = open('tickets.csv', 'ab')
csv_writer = unicodecsv.writer(result_csv, quoting=unicodecsv.QUOTE_ALL)

ticket_count = 0

for filename in glob.iglob('*.pdf'):
  print(filename)
  ticket_count += 1

  pdf = pdfquery.PDFQuery(filename)
  pdf.load()

  label_price = pdf.pq('LTTextLineHorizontal:contains("Summe")')

  result = pdf.extract([
     ('with_parent','LTPage[pageid=\'1\']'),
     ('with_formatter', 'text'),
     
     # scrape by absolute position, doesn't work with all kinds of tickets

     ('validity', 'LTTextLineHorizontal:overlaps_bbox("86,734,198,746")'),
     ('fare', 'LTTextLineHorizontal:overlaps_bbox("39,719,209,729")'),
     ('discount', 'LTTextLineHorizontal:overlaps_bbox("86,695,185,705")'),
     ('route', 'LTTextLineHorizontal:overlaps_bbox("86,682,345,694")'),
     ('price', 'LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (float(label_price.attr('x0'))+100, float(label_price.attr('y0')), float(label_price.attr('x0'))+150, float(label_price.attr('y0'))+15)),
     ('ticket_id', 'LTTextLineHorizontal:overlaps_bbox("504,533,548,543")')
  ])

  if ticket_count == 1:
    csv_writer.writerow(result.keys())
  csv_writer.writerow(result.values())

  print(result)

  #sys.exit(1);

