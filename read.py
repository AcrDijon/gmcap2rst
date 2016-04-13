# coding: utf-8
import datetime
import csv
import os


page = u"""\
Foulées du Lac Kir 2016: Liste des Inscrits
===========================================

:date: 04/04/2016
:category: Foulées du Lac Kir
:location: Dijon
:eventdate: 16/04/2016

Liste mise à jour le %s

1250M
-----

%s

2200M
-----

%s


5KM
---

%s



10KM
----

%s
"""



def generate_sep(col_widths, char='-'):
    return '+' + '+'.join([char * (col_width + 2)
                         for col_width in col_widths]) + '+'

def generate_line(values, col_widths):
    l = []
    for i, value in enumerate(values):
        l.append(' ' + value.ljust(col_widths[i]) + ' ')
    return '|' + '+'.join(l) + '|'


def generateTable(headers, lines):
    # for each column, find the width
    col_widths = []

    for col in range(len(headers)):
        width = 0
        if len(headers[col]) > width:
            width = len(headers[col])
        for line in lines:
            if len(line[col]) > width:
                width = len(line[col])

        col_widths.append(width)

    # now we can generate the table
    table = [generate_sep(col_widths)]
    table.append(generate_line(headers, col_widths))
    table.append(generate_sep(col_widths, '='))

    for line in lines:
        table.append(generate_line(line, col_widths))
        table.append(generate_sep(col_widths))

    return '\n'.join(table)


filename = 'adultes.txt'
filename = os.path.join(os.path.dirname(__file__), filename)
header = (u'Nom', u'Prénom', u'Sexe', u'Dossard', u'Licence', u'Naissance',
          u'Catégorie', u'Club')
five = []
ten = []

with open(filename, 'rb') as csvfile:
    reader  = csv.reader(csvfile, delimiter='\t')
    for index, row in enumerate(reader):
        row = [unicode(col, 'iso8859-1') for col in row]
        if index == 0:
            continue

        line = row[0], row[1], row[9], row[10], row[11], row[13], row[15], row[18]
        if row[25] == u'5 km':
            five.append(line)
        else:
            ten.append(line)


five.sort()
ten.sort()

five = generateTable(header, five)
ten = generateTable(header, ten)


filename = 'enfants.txt'
filename = os.path.join(os.path.dirname(__file__), filename)
header = (u'Nom', u'Prénom', u'Sexe', u'Dossard', u'Licence', u'Naissance',
          u'Catégorie', u'Club')
one = []
two = []

with open(filename, 'rb') as csvfile:
    reader  = csv.reader(csvfile, delimiter='\t')
    for index, row in enumerate(reader):
        row = [unicode(col, 'iso8859-1') for col in row]
        if index == 0:
            continue

        line = row[0], row[1], row[9], row[10], row[11], row[13], row[15], row[18]
        if row[26] == u'1,220':
            one.append(line)
        else:
            two.append(line)


one.sort()
two.sort()

one = generateTable(header, one)
two = generateTable(header, two)


page = page % (datetime.datetime.now().strftime('%d/%m/%Y'), one, two, five, ten)


with open('inscrits.rst', 'w') as f:
    f.write(page.encode('utf8'))
