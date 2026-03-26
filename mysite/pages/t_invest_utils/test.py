import http.client
import json

conn = http.client.HTTPSConnection("sandbox-invest-public-api.tbank.ru")
payload = json.dumps({
  "instrumentId": [
    "string"
  ],
  "lastPriceType": "LAST_PRICE_UNSPECIFIED",
  "instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED"
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer <TOKEN>'
}
conn.request("POST", "/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetLastPrices", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


