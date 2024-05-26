"""
Share link: https://www.cutout.pro?vsource=cutout_share-479129331241221

bot steps:
1. go to emailfake.com, enter generated email name.
2. go to the share link.
3. click the register button.
4. wait for email to arrive on emailfake.com
5. click the link in the email.
6. go to the api key page.
7. wait for api key to appear and copy it.
"""

import contextlib
import json
import logging
import time
import typing

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

executable_service = Service(ChromeDriverManager().install())
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s: %(message)s')


class Driver(webdriver.Chrome):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def recieve(self, selector: str, timeout: float = 10) -> WebElement:
    try:
      return WebDriverWait(self, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
      )
    except Exception as e:
      logging.error(f"recieving {selector} failed within {timeout}s")
      raise e

  def see_all(self, selector: str, timeout: float = 10) -> typing.List[WebElement]:
    time.sleep(1)
    # e = driver.find_element(By.CSS_SELECTOR, selector)
    # WebDriverWait(self, timeout).until(EC.element_to_be_clickable(e))
    return self.find_elements(By.CSS_SELECTOR, selector)

  def css(self, selector, source=None, noerr=False):
    if noerr:
      with contextlib.suppress(Exception):
        return (source or self).find_element(By.CSS_SELECTOR, selector)
    else:
      return (source or self).find_element(By.CSS_SELECTOR, selector)

  def css_many(self, selector, source=None):
    return (source or self).find_elements(By.CSS_SELECTOR, selector)


# import action keys

def main(bot: Driver, share_link, email_name):
  STEPS = [
    1,
    2
  ]

  # 1. go to emailfake.com, enter generated email name.
  bot.get('https://emailfake.com/')
  bot.switch_to.window(bot.window_handles[0])
  time.sleep(2)

  # select all input content and replace
  inp = bot.css('#userName')
  inp.clear()
  inp = bot.css('#userName')
  inp.send_keys(email_name)
  inp = bot.css('#userName')
  inp.send_keys('\n')  # enter

  time.sleep(1)

  bot.refresh()

  # select all input content and replace
  inp = bot.css('#userName')
  inp.clear()
  inp = bot.css('#userName')
  inp.send_keys(email_name)
  inp = bot.css('#userName')
  inp.send_keys('\n')  # enter



  email = email_name + '@' + bot.css('#domainName2').get_attribute('value')
  print(f'{email=}')

  # 2. go to the share link.
  # url in new tab
  bot.execute_script(f"window.open('{share_link}');")

  # 3. click the register button.
  # switch tab
  bot.switch_to.window(bot.window_handles[-1])

  time.sleep(5)
  bot.execute_script('document.querySelector("#modalMask").style = ""')

  # switch to sign up
  bot.execute_script('document.querySelector(".userContent span:nth-child(2)").click()')

  # enter details
  bot.css('#input-170').send_keys(email)
  bot.css('#input-173').send_keys(email)
  bot.css('#input-177').send_keys(email)
  bot.css('.loginPrimaryBtn').click()  # register

  time.sleep(3)

  # close the tab
  bot.close()

  # 4. wait for email to arrive on emailfake.com
  # switch tab
  bot.switch_to.window(bot.window_handles[0])

  # 5. click the link in the email.
  time.sleep(5)
  try:
    bot.get(bot.css('a[href^="https://www.cutout.pro"]').get_attribute('href'))
  except selenium.common.exceptions.NoSuchElementException:
    time.sleep(10)
    bot.refresh()
    bot.get(bot.css('a[href^="https://www.cutout.pro"]').get_attribute('href'))

  time.sleep(1)

  # 6. go to the api key page.
  bot.get('https://www.cutout.pro/user/secret-key')

  # 7. wait for api key to appear and copy it.
  time.sleep(3)
  api_key = bot.css('.Subscribe .cu').text.strip()

  print(f'{api_key=}')

  # sign out
  bot.execute_script('document.querySelector(".infoListItem").click()')
  time.sleep(2)

  return email, api_key



import string, random


def random_email_name():
  return "".join([random.choice(string.ascii_lowercase) for _ in range(10)])


if __name__ == '__main__':
  chrome_options = Options()
  chrome_options.add_experimental_option("detach", True)
  chrome_options.add_argument("--window-size=1224,768")
  chrome_options.add_argument(
    'load-extension=' + r'C:\Users\nirch\AppData\Local\Google\Chrome\User Data\Default\Extensions\cfhdojbkjhnklbpkdaibdccddilifddb\3.20_0')

  bot = Driver(service=executable_service, options=chrome_options)
  bot.get('https://google.com')

  # wait for adblock to load
  time.sleep(5)
  bot.close()  # close the adblock tab
  bot.switch_to.window(bot.window_handles[0])  # switch to the main tab


  for _ in range(40):
    email, api_key = main(
      bot=bot,
      share_link='https://www.cutout.pro?vsource=cutout_share-479129331241221',
      email_name=random_email_name()
    )

    with open('accounts.json') as f:
      accs = json.load(f)

    accs.append({
      'email': email,
      'api_key': api_key
    })

    with open('accounts.json', 'w') as f:
      json.dump(accs, f, indent=2)

    print('✅ Added', email, '(' + api_key + ')')

  bot.quit()
