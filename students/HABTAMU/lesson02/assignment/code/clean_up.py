"""
this module clean the json source data,
when end rental date is ealier than start rental date.

    Args: take source.json as an input file.
    Return: correct_source.json as a cleaned output json file.

"""

import json
import datetime

with open('source.json', 'r') as input:
     data = json.load(input)
     for value in data.values():
             rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
             rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
             if (rental_end - rental_start).days < 0:
                     temp_value = value['rental_start']
                     value['rental_start'] = value['rental_end']
                     value['rental_end'] = temp_value

with open('correct_source.json', 'w', encoding='utf-8') as output:
     output.write(json.dumps(data, indent=4,ensure_ascii=False))
