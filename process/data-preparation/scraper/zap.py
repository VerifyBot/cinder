import json
import typing

import requests
from lxml import html

ENGLISH_INFO = dict(
  company='יצרן',
  category='קטגוריה',
  doors='מספר דלתות',
  seats='מספר מושבים',
  engineVolume="נפח מנוע (סמ''ק)",
  cylinders="מספר צילינדרים",
  valves='מספר שסתומים',
  fogLights='פנסי ערפל',
  trunkVolume='נפח תא מטען (ליטר)',
  maxPower="הספק מירבי (כ''ס)",
  maxMoment="מומנט מירבי (קג''מ)",
  maxSpeed="מהירות מירבית (קמ''ש)",
  maxAcceleration="תאוצה 0-100 קמ''ש (שניות)",
  airbags='מספר כריות אוויר',
  length="אורך (מ''מ)",
  width="רוחב (מ''מ)",
  height="גובה (מ''מ)",
  wheelbase="בסיס גלגלים (מ''מ)",
  weight="משקל עצמי (ק''ג)",
  fueltankCapacity='קיבולת מיכל דלק (ליטר)',
  frontTireWidth="רוחב צמיג קדמי (מ''מ)",
  frontTireWidthHeightRatio='יחס רוחב-גובה בצמיג קדמי',
  frontHoopDiameter="קוטר חישוק קדמי (מ''מ)",
  rearTireWidth="רוחב צמיג אחורי (מ''מ)",
  rearTireWidthHeightRatio='יחס רוחב-גובה בצמיג אחורי',
  rearHoopDiameter="קוטר חישוק אחורי (אינץ')",
  frontSuspensions='מתחיל קדמיים',
  windows='מספר חלונות חשמל',
  fuelConsumptionUrban="צריכת דלק עירונית (ליטרים ל- 100 ק''מ)",
  fuelConsumptionHighway="צריכת דלק בכביש מהיר (ליטרים ל- 100 ק''מ)",
  fuelConsumptionCombinedRow="צריכת דלק משולב (ליטרים ל- 100 ק''מ)",
  engineType='סוג המנוע',
  model='דגם',
  licensingGroup='קבוצת רישוי',
  warranty='אחריות',
  fuelInjection='סוג הזרקת דלק',
  turboAccent='מדגש טורבו',
  pollution='דרגת זיהום',
  ABS='מניעת נעילת גלגלים (ABS)',
  BAS='תגבור בלימת חירום (BAS)',
  EBD='חלוקת לחצי בלימה (EBD)',
  ESP='בקרת יציבות (ESP)',
  TCS='בקרת משיכה (TCS)',
  mobilizer='אימובילייזר',
  alarm='אזעקה',
  lightAlloyRims='חישוקי סגסוגת קלה',
  vehiclePropulsion='הנעת הרכב',
  gearbox='סוג תיבת הילוכים',
  changeWheelHeight='כוון גובה גלגל ההגה',
  changeWheelDepth='כוון עומק גלגל ההגה',
  frontBrakes='בלמים קדמיים',
  rearBrakes='בלמים אחוריים',
  rearRacks='מתחיל אחוריים',
  mirrors='מראות צד חשמליות',
  centralLock='נעילה מרכזית',
  airConditioningType='סוג מיזוג אויר',
  sunroof='חלון גג',
  smartscreen='מחשב דרך',
  cruiseControl='בקרת שיוט'
)

ENGLISH_INFO = dict(zip(ENGLISH_INFO.values(), ENGLISH_INFO.keys()))  # put value instead of key for easy access


def is_float(element) -> bool:
  # ref: https://stackoverflow.com/a/20929881/11854052
  try:
    float(element)
    return True
  except ValueError:
    return False


class ZapScraper:
  """
  ZapScraper is a scraper for the items in zap.co.il website.

  :param category: category of items to scrape
  :param sog: sog of items to scrape (go to the listing and copy the sog param from the url)
  :param lang_mapper: a dictionary mapping the hebrew attribute names to english attribute names
  """

  cookies = {
    'AccessibilityColorCookie': '',
    '.ASPXANONYMOUS': '1MPXUk4yx5b7ougZnnzcNgveMEh1cN88S__uk818PpUHwZGdb_ks5F6LYMcfy8sZG5aqB0RWzW3uCj52D4luy4o-OveoW8Zob4re92L0w-eJgJmPaWSOFXBvzVP4LldEDL_77g2',
    '_hjid': '12d06c59-c321-4da1-9880-0bf289da42a1',
    '_hjSessionUser_87878': 'eyJpZCI6ImFkNmRjNjlkLTk0NzAtNWEzYS1hZjExLTNiY2ExNjA3MDk2ZCIsImNyZWF0ZWQiOjE2NDUxMDU1OTM1NzgsImV4aXN0aW5nIjp0cnVlfQ==',
    'zapum_v1': '{"ZapId":"dummyZapId","GUID":"63b7b15a-2d30-0fb8-fbb2-f96a44880324","GAIDs":["544767528.1645105593"]}',
    'compID': '11172113',
    '_gac_UA-2875041-2': '1.1645106135.CjwKCAiAgbiQBhAHEiwAuQ6Bkjtae6Fh-e1aIYt7PUPxo9DoqfeqwRWpNr5QzXDXF5SMGX2aF9ZJwhoCy2wQAvD_BwE',
    '__utma': '230947348.544767528.1645105593.1645105594.1646501736.2',
    '__utmz': '230947348.1646501736.2.2.utmcsr=sso.zap.co.il|utmccn=(referral)|utmcmd=referral|utmcct=/',
    '_ga': 'GA1.1.544767528.1645105593',
    '_ga_BK21WVNL1Q': 'GS1.1.1646501734.2.1.1646501751.0',
    'ASP.NET_SessionId': '0hehy13cw1kleclq0kjmxjhn',
    'BIGipServerb3tacore.zap.co.il': '1358954506.47873.0000',
    'Ref': 'www.zap.co.il',
    'TS0145b983': '015d3c2c9bbc7b25ad446eedd3ed756db550ec18b8c7e6c14523c4833122a4326bf26e6d9762b3b31cf9dccc6c390de26805968256',
    'zap_push': 'null',
    'g_state': '{"i_p":1648038435226,"i_l":2}',
    'TS01920653': '015d3c2c9b706a74a11c5b969c8a518c535a9144cdee6320f8d4adec8ec49400dbd4192db28b236f57764556de7a132200cb681606',
    'SiteCookie': 'notloggedin',
    'TS782e9b34027': '0889aa580eab2000333ef2885b9845d14f2d8e59c5daed6d9da9f97ab75dd46ecc46f9b4a2aeb7b3083486938a11300036c96bd14e02730032a326b240791f939ea375b33e4f07101e18b85e5409939830f4680995907a4adb48e49c0b03d5ab',
  }
  headers = {
    'authority': 'www.zap.co.il',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.zap.co.il/',
    'accept-language': 'en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7,la;q=0.6,ru;q=0.5',
  }

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

  # BASIC DATA VALIDATION

  # with open('carsData.json', encoding='utf8') as fp:
  #   dt = json.load(fp)
  #
  # distinct_names = set()
  #
  # for car in dt:
  #   distinct_names.add(car['company']+' '+car['name'])
  #
  # print(f'{len(distinct_names)} distinct vs {len(dt)} data')
