import json

with open('accounts.json', 'w') as f:
  accs = json.dump([
  {
    "email": "fannana@pflznqwi.xyz",
    "api_key": "ee87d9916f02459c83bbbeb20c0e36bc"
  },
  {
    "email": "mfannana@pflznqwi.xyz",
    "api_key": "2fc6813342274d46a10497aaaaf6a609"
  },
  {
    "email": "mmfannana@pflznqwi.xyz",
    "api_key": "c3bb86e817f6470499a82f247b77cd08"
  },
  {
    "email": "mmmfannana@pflznqwi.xyz",
    "api_key": "5dfb13af443848eda9a7c81a6247981d"
  },
  {
    "email": "mmmmfannana@pflznqwi.xyz",
    "api_key": "a11599f9745a4b5b89a9df6098b31249"
  },
  {
    "email": "mmmmmfannana@pflznqwi.xyz",
    "api_key": "443f45dec6cd42158bacb27c860b1716"
  },
  {
    "email": "mmmmmmfannana@pflznqwi.xyz",
    "api_key": "59b315e15fd54b3eb4b5ce4651801560"
  },
  {
    "email": "mmmmmmmfannana@pflznqwi.xyz",
    "api_key": "11a95b1f766842be900dec9345107319"
  },
  {
    "email": "mmmmmmmmfannana@pflznqwi.xyz",
    "api_key": "d01abba24dd44dbbb4b992bcc56ba5ec"
  },
  {
    "email": "mmmmmmmmmfannana@pflznqwi.xyz",
    "api_key": "4742ba5ed324473db9a69b66233d27f2"
  },
  {
    "email": "riosonandoasies@clonemailsieure.click",
    "api_key": "99d99450733f40da913dba068f57123f"
  },
  {
    "email": "mfannan@kinitawowis.xyz",
    "api_key": "fa1d5dccf26a4a35aa2865bbd11c0717"
  },
  {
    "email": "mfannan@efundpro.com",
    "api_key": "2a69092f0be44cf3824aa51418751f3c"
  },
  {
    "email": "mfannan@pflznqwi.xyz",
    "api_key": "a474e6847be94f6ea1d8262709528682"
  },
  {
    "email": "pvducoewyf@mrando.tk",
    "api_key": "3dfdb13a83794ce78db03df663ef11dd"
  },
  {
    "email": "riosonandoasies@audrianaputri.com",
    "api_key": "fd4e73cc34bd47a7960ed4bdfa531596"
  },
  {
    "email": "qvvdflbjbi@sublimelimo.com",
    "api_key": "30107d77f2f34997bf83881deba6b695"
  }
], f, indent=2
)

# with open('accounts.json') as f:
#   t = [ln.strip() for ln in f.readlines() if ln.strip()]
#
# accounts = []
# acc = {}
# for i, line in enumerate(t):
#   if '@' in line:
#     acc['email'] = line
#   else:
#     acc['api_key'] = line
#     accounts.append(acc)
#     acc = {}
#
# print(accounts)