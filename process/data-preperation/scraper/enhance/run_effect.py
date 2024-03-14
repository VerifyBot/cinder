import json

import requests


"""
TODO:
- generate more credits (fix the looper... - it bugs on emailfake so fix it - just paste, refresh paste again i think)
"""


class InsufficientCredits(Exception):
  pass


class NoAccountsLeft(Exception):
  """Raised when all accounts are out of credits."""


with open('accounts.json') as f:
  accs = json.load(f)


def _enhance(img_bytes, api_key):
  """The main enhancement function. Doesn't handle insufficient credits."""
  # print(f'Running enhance on {len(img_bytes)} bytes with {api_key}')
  resp = requests.post(
    'https://www.cutout.pro/api/v1/photoEnhance',
    headers={'APIKEY': api_key},
    files={'file': img_bytes}
  )

  if "Insufficient credits" in resp.text:
    raise InsufficientCredits()

  # print(f"❤️‍🔥 Enhanced image (res increased by {len(resp.content) / len(img_bytes):.2f}%)")
  return resp.content


def get_api_key(current_is_over=False):
  """Returns a prolly valid api key"""
  if current_is_over:
    accs[next(i for i in range(len(accs)) if not accs[i].get('reached_limit', False))]['reached_limit'] = True

    with open('accounts.json', 'w') as f:
      json.dump(accs, f, indent=2)

  if all(acc.get('reached_limit', False) for acc in accs):
    raise NoAccountsLeft()

  return next(acc['api_key'] for acc in accs if not acc.get('reached_limit', False))


def enhance(img_bytes, api_key=None):
  """Uses the _enhance function to enhance an image. Handles insufficient credits
  by switching accounts."""
  try:
    return _enhance(img_bytes, api_key=api_key or get_api_key())
  except InsufficientCredits:
    print("⏭️ Insufficient credits, switching accounts")
    return enhance(img_bytes, api_key=get_api_key(current_is_over=True))
  except NoAccountsLeft:
    print("❌ No accounts left, exiting")
    raise NoAccountsLeft()


if __name__ == '__main__':
  enhance(open('../15476374030.png', 'rb'))
