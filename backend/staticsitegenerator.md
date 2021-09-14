# Simple Static Site Generator

The simple static site generator recursively finds and replaces all of the specified variables in a given document with their specified values.

## Identifiers

Identifiers are variables bookended by double % signs. In the below example %%myName%% is replaced with "Alex".

Input: {"myName":"Alex"}

Template: Hi, my name is %%myName%%.

Output: Hi, my name is Alex.

## Templates

## Content

Content files paths must match the template file paths

## Data

### Battery data

### Weather data

### Page Size

On disk page size is determined by identifying all of the assets that page includes (css & media) and adding up the size of the html page itself and those assets. 

Transferred data:
External API call have been measure in advance and are added to that total.

## Automation

`sudo crontab -e`
`*/15 * * * * /use/bin/python3 /home/pi/local/www/lowcarbonresearchmethods/backend/lowcarbonmethods.py`

## Future Development

* CSS Minifier - a script to generate individual CCS pages per html page so only the necessary amount of CSS is transferred to the client
* Content via content pages i.e. markdown CMS???