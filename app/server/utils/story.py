def create_story_for_nlp_embedding(car):
  story_template = """
  This is a {color} hex colored \"{company} {category}\" car called \"{company} {name}\".
  It is priced {price} USD. It has {doors} doors and {seats} seats.
  The engine volume is {engineVolume} cc and the trunk volume is {trunkVolume} l.
  The car has a maximum power of {maxPower} horsepower and a maximum moment of {maxMoment} kg/m.
  It can reach a maximum speed of {maxSpeed} km/h and accelerate from 0 to 100 km/h in {maxAcceleration} s.
  The car has {airbags} airbags and its dimensions are {length} x {width} x {height} mm.
  It weighs {weight} kg and has a fuel tank capacity of {fueltankCapacity} liters.
  There are {windows} windows and the fuel consumption in urban areas is {fuelConsumptionUrban} l/100km.
  The engine type is {engineType} and the model is {model}.
  The pollution level is {pollution}/15 and the gearbox is {gearbox}.
  The car {sunroof} a sunroof, {smartscreen} a smartscreen, and {cruiseControl} cruise control.
  The vehicle propulsion is {vehiclePropulsion}. The car's warranty is \"{warranty}\".
  """

  car['vehiclePropulsion'] = {"קדמית": "FWD", "אחורית": "RWD", "כפולה קבועה": "4X4", "אחורית + כפולה": "RWD & 4X4",
                              "קדמית + כפולה": "FWD & 4X4"}.get(car['vehiclePropulsion'], car['vehiclePropulsion'])
  car['gearbox'] = {"ידנית": "manual", "אוטומטית": "automatic", "רובוטית": "robotic", "רציפה": "CVT",
                    "תמסורת ישירה": "direct"}.get(car['gearbox'], car['gearbox'])
  car['engineType'] = {"בנזין": "gasoline", "דיזל": "diesel", "הייבריד בנזין": "hybrid", "הייבריד דיזל": "hybrid"}.get(
    car['engineType'], car['engineType'])

  car['sunroof'] = 'has' if car['sunroof'] else 'does not have'
  car['smartscreen'] = 'has' if car['smartscreen'] else 'does not have'
  car['cruiseControl'] = 'has' if car['cruiseControl'] else 'does not have'

  return story_template.format(**{k: car.get(k, 'N/A') for k in car.keys()}).strip().replace('\n  ', ' ')