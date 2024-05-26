from object_detection import Detector

d = Detector()
r = d.do_detect('../scraper/images/968372.png', '.')
print(r)