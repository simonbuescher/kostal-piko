# piko-homeassistant-integration - accessing older generation piko inverters in home assistant

**piko-homeassistant-integration** is a custom [Home Assistant](https://www.home-assistant.io/) 
integration for accessing data of older generation [Kostal](https://www.kostal-solar-electric.com/) 
Piko inverters that do not support the `/api/dxs.json` endpoint.

It works by simply scraping the html webserver for predefined values.
Currently supported values are:
- running (boolean, `true` if the inverter is currently running and feeding in electricity)
- current production in W, (float)
- today's total production in kWh, (float)
- total production of all time in kWh (float)

## Acknowledgements
This integration is inspired by [homeassistant-kostal-piko](https://github.com/scheidtdav/homeassistant-kostal-piko)
by [David Scheidt](https://github.com/scheidtdav) and largely used his project as a tutorial.

## Warning
This integration is unfinished, unstable and everything else. I did this in one evening
and stopped working on it as soon as the base values would work reliably.

**USE AT YOUR OWN RISK**
