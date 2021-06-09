import requests

BASE = "http://127.0.0.1:8080"

data = [{"wasteType": "Clothes", "description": "Clothes are the things that people wear, such as shirts , coats , trousers , and dresses."}]

dataContent = [{"id":1, "title":"Battery Recycling'", "wasteType":"Battery","imageUrl":"https://media.istockphoto.com/photos/trash-batteries-with-oxidation-rechargeable-accumulators-and-old-picture-id1165711632","content":"Single-use batteries contain a number of materials that are recyclable. You can recycle them by dropping them off at a local facility or by participating in the many mail-in or take-back programs that are available.\r\n\r\nRecycling batteries through mail in programs works particularly well for office buildings. We have several buckets in our office which, once full, we mail to the location to get recycled. If you have questions about recycling single-use batteries continue reading below.\r\n\r\nFind a drop-off location for single-use batteries near you using the Recycling Locator."},
{"id":2, "title":"Biological Waste'", "wasteType":"Biological","imageUrl":"https://www.untha-america.com/images/example/biologische-abfaelle/bioabfaelle.jpg","content":"Biological waste must be managed separately from chemical waste. The most common example where chemical waste is mistaken for biological waste is agarose gel contaminated with ethidium bromide or heavy metals (i.e. arsenic, chromium). This type of material should always be managed as chemical waste. When both chemical and biological waste types exist, the biological agent(s) should be treated first. Once the biological agents have been deactivated by either autoclave or chemical disinfection, the remaining chemical waste should be submitted on a Hazardous Materials Pickup Request Form."}]


for i in range(len(data)):
    response = requests.put(BASE + "api/content", dataContent[i])
    print(response.json())

input()
response = requests.get(BASE + "/api/waste/2")
print(response.json())
