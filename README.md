# drf-zeep
Zeep WSDL/XSD type to Django Restframework converter.

# Usage

```
from zeep import Client
from wsgserver.drf_zeep import ZeepSerializer

zeep_client = Client('http://my-endpoint.com/production.svc?wsdl')


class ConvertSpeedSerializer(ZeepSerializer):
    class Meta:
        fields = '__all__'
        client = zeep_client
        xsd_type = 'ns0:complexType'

serializer = ConvertSpeedSerializer()

print serializer
```

