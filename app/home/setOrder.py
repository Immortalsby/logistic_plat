import requests
url = "https://wms.apex-oms.com/default/svc/web-service"

# python3字符串换行，在右边加个反斜杠
body = '''<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.example.org/Ec/">
        <SOAP-ENV:Body>
                <ns1:callService>
                        <paramsJson>
{"platform": "OTHER", "warehouse_code": "TESTHANSHOW", "shipping_method": "UPS_DELIVERY", "reference_no": "HS-QZCFH-2021-01-10-0061", "country_code": "FR", "province": "province", "name": "Bricoman Le mans", "address1": "Yvre Lieu Dit \uff07La Fani\u00e8re\uff0772530   YVRE", "zipcode": "12970", "items": [{"product_sku": "Stellar-S3TN@E31A", "product_name_en": "Electronic shelf Label", "quantity": 1500}]}
                        </paramsJson>
                        <appToken>7f27b5da0ed81105b98c35151b54637f</appToken>

                        <appKey>05b92060f873c3c7649339c052a637f5</appKey>
<service>createOrder</service></ns1:callService>
        </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''

# 遇到编码报错时候，对body进行encode
r = requests.post(url, data=body.encode("utf-8"))
print(r.text)