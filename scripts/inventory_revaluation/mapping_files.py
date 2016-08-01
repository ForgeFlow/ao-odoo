# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
import csv


def mapping(file):
    with open('mapping_files/'+file) as csvfile:
        reader = csv.DictReader(csvfile)
        output = {}
        for row in reader:
            output[row['Extract']] = row['Transform']
        csvfile.close()
    return output
