import requests
from lxml import html
from lxml import etree
from io import StringIO, BytesIO
import pdb

res = requests.get('https://weather.gc.ca/city/pages/mb-38_metric_e.html')
parser = etree.HTMLParser()
html_tree = etree.parse(StringIO(res.text), parser)
result = etree.tostring(html_tree.getroot(), pretty_print=True, method="html")
tree = html.fromstring(res.content)
pdb.set_trace()

print("Done")
