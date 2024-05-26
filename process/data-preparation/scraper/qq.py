import json
import typing

import requests
from lxml import html

class ZapScraper:
  """
  ZapScraper is a scraper for the items in zap.co.il website.

  :param category: category of items to scrape
  :param sog: sog of items to scrape (go to the listing and copy the sog param from the url)
  :param lang_mapper: a dictionary mapping the hebrew attribute names to english attribute names
  """

  def __init__(self, category: str = 'cars', sog: str = 't-newcar', lang_mapper: dict = {}):
    assert category == 'cars', 'ZapScraper is only capable of scraping cars data at the moment.'

    self.base_listing_url = f'https://www.zap.co.il/{category}/models.aspx?sog={sog}'
    self.base_item_url = f'https://www.zap.co.il/cars/compmodels.aspx'

    self.lang_mapper = lang_mapper

  @staticmethod
  def normalize_value(value: str):
    """
    Standarization of car information data:
      כן/לא ==> True/False
      יעודכן בקרוב ==> None
      2,343 (סמ"ק/ליטר...) ==> int(2343)
      28.3 (כוח סוס/סמ"ק...) ==> float(28.3)

    :param value: value string
    """

    # booleans
    if value == 'כן':
      return True

    elif value == 'לא':
      return False

    # none
    if value == 'יעודכן בקרוב':
      return None

    # numbers
    if (n := value.replace(',', '').split(' ', 1)[0]).isdigit():
      return int(n)
    elif is_float(n):
      return float(n)

    return value

  def fetch_listing(self, page: int) -> typing.Generator:
    """
    Returns a generator of the items listed in the given page

    :param page: page number
    """

    url = f'{self.base_listing_url}&pageinfo={page}'

    # Get HTML page containing items list
    resp = requests.get(url, headers=self.headers, cookies=self.cookies)
    resp.encoding = resp.apparent_encoding

    tree: html.HtmlElement = html.fromstring(resp.text)

    listing_items = tree.cssselect(".ProductBox")

    for item in listing_items:
      item: html.HtmlElement

      yield self.fetch_item(model_id=item.attrib['data-model-id'])

  def fetch_item(self, model_id: int):
    """
    Returns a dictionary of the item's attributes

    :param model_id: item model id
    """
    url = f'{self.base_item_url}?modelid={model_id}'

    # Get HTML page containing car information
    url = f'{self.base_item_url}?modelid={model_id}'
    resp = requests.get(url, headers=self.headers, cookies=self.cookies)
    resp.encoding = resp.apparent_encoding

    # Parse car attributes from HTML page
    tree: html.HtmlElement = html.fromstring(resp.text)

    attrs_elements_list = tree.cssselect(".detailsRow")

    attrs = {}

    attrs['name'] = tree.cssselect(".ProdName")[0].text_content().strip().strip('\u200f').split(' ', 1)[1]
    attrs['price'] = int(tree.cssselect(".PricesTxt")[0].text_content().strip().replace(',', '').split(' ', 1)[0])

    for attr in attrs_elements_list:
      attr_title = attr.cssselect(".detailsRowTitletxt")[0].text_content().strip()

      # map to english and skip if not found (assuming there is a mapper in the first place)
      if self.lang_mapper and not (attr_title := self.lang_mapper.get(attr_title)):
        continue

      attr_value = attr.cssselect(".detailsRowTxt")[0].text_content().strip()

      attrs[attr_title] = ZapScraper.normalize_value(attr_value)

    # dont forget about the image
    attrs['image'] = tree.cssselect('[id^="ProdPi"] img')[0].attrib['src']
    attrs['extraImages'] = list({
      tree.cssselect("#carBigImg")[0].attrib["src"], *set(
        img.attrib['src'].replace('b.gif', 'c.gif') for img in tree.cssselect("#hl_img img"))
    })

    attrs['id'] = model_id

    return attrs


def update_json(fn: str, items):
  """
  Update json file with new items
  :param fn: filename
  :param items: data
  """
  with open(fn, 'w', encoding='utf8') as fp:
    json.dump(items, fp, ensure_ascii=False, indent=2)


if __name__ == '__main__':
  scraper = ZapScraper(
    category='cars',
    sog='t-newcar',
    lang_mapper=ENGLISH_INFO
  )

  save_filename = 'withimgs_carsData.json'

  pages_count = 54
  items = []
  for page in range(1, pages_count + 1):
    print(f'🔃 Fetching listing page: {page}/{pages_count}')

    for item in scraper.fetch_listing(page):
      items.append(item)

      print(f'\t\t[#{len(items)}] 👉 {item["name"]}')

    update_json(save_filename, items)