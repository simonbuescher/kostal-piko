# pikoapi - accessing older generation piko inverters

**pikoapi** is a Python module for accessing data of older generation 
[Kostal](https://www.kostal-solar-electric.com/) piko inverters that 
do not support the `/api/dxs.json` endpoint.

It works by simply scraping the html webserver for predefined values.
Currently supported values are:
- running (boolean, `true` if the inverter is currently running and feeding in electricity)
- current production in W, (float)
- today's total production in kWh, (float)
- total production of all time in kWh (float)


## Usage
Example usage can be seen in the `example.py` script.
