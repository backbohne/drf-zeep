"""
Zeep WSDL/XSD type to Django Restframework converter.
"""

import decimal
from collections import OrderedDict
from zeep.xsd.types import builtins
from zeep.xsd import ComplexType
from rest_framework import serializers



__all__ = ['ZeepSerializer']


def debug(e, level=0):
    print "%s%s: cls:%s, type:%s"% (' ' * (level), e, e.__class__, type(e))
    for d in [d for d in sorted(dir(e)) if d.find('__') != 0]:
        try:
            x = getattr(e, d)
            if callable(x):
                try:
                    print "%s>>> %s(): %s" % (' ' * (level+4), d, x())
                except:
                    print "%s>>> %s(): ..." % (' ' * (level+4), d)
            else:
                print "%s>>> %s: %s (%s)" % (' ' * (level+4), d, x, x.__class__.__name__)
        except Exception as err:
            print "%s>>> %s err: %s" % (' ' * (level+4), d, err)


def extend_instance(instance, cls):
    instance.__class__ = type(
      '%sExtendedWith%s' % (instance.__class__.__name__, cls.__name__), 
      (instance.__class__, cls), {})


class ZeepBuildinMixin(object):
    _zeep_builtin_cls = None

    @property
    def _zeep_builtin(self):
        if getattr(self, '_zeep_builtin', None) is None:
            self._zeep_builtin = self._zeep_builtin_cls()
        return self._zeep_builtin

    def to_representation(self, obj):
        return self._zeep_builtin.xmlvalue(obj)

    def to_internal_value(self, data):
        try:
            return self._zeep_builtin.pythonvalue(data)
        except builtins.ParseError:
            raise serializers.ValidationError('invalid data')

class RequireAwareCharField(serializers.CharField):
    def __init__(self, **kwargs):
        if not kwargs.get('required', True):
            kwargs['allow_blank'] = True
            kwargs['allow_null'] = True
            kwargs['default'] = ''
        super(RequireAwareCharField, self).__init__(**kwargs)

class CharField(RequireAwareCharField):
    pass

class RequireAwareIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        if not kwargs.get('required', True):
            kwargs['allow_null'] = True
        super(RequireAwareIntegerField, self).__init__(**kwargs)

class IntegerField(RequireAwareIntegerField):
    pass

class gYearMonthField(ZeepBuildinMixin, serializers.Field):
    _zeep_builtin_cls = builtins.gYearMonth

class gYearField(ZeepBuildinMixin, serializers.Field):
    _zeep_builtin_cls = builtins.gYear

class gMonthDayField(ZeepBuildinMixin, serializers.Field):
    _zeep_builtin_cls = builtins.gMonthDay

class gDayField(ZeepBuildinMixin, serializers.Field):
    _zeep_builtin_cls = builtins.gDay

class gMonthField(ZeepBuildinMixin, serializers.Field):
    _zeep_builtin_cls = builtins.gMonth

class HexBinaryField(ZeepBuildinMixin, serializers.Field):
    _zeep_builtin_cls = builtins.HexBinary

class Base64BinaryField(ZeepBuildinMixin, serializers.Field):
    _zeep_builtin_cls = builtins.Base64Binary

class PositiveIntegerField(RequireAwareIntegerField):
    def __init__(self, **kwargs):
        kwargs['min_value'] = 0
        super(PositiveIntegerField, self).__init__(**kwargs)

class NegativeIntegerField(RequireAwareIntegerField):
    def __init__(self, **kwargs):
        kwargs['max_value'] = -1
        super(NegativeIntegerField, self).__init__(**kwargs)

class RequireAwareDecimalField(serializers.DecimalField):
    def __init__(self, **kwargs):
        if not kwargs.get('required', True):
            kwargs['allow_null'] = True
        kwargs['coerce_to_string'] = True
        super(RequireAwareDecimalField, self).__init__(max_digits=None, decimal_places=None, **kwargs)

class DecimalField(RequireAwareDecimalField):
    pass

class RequireAwareFloatField(serializers.FloatField):
    def __init__(self, **kwargs):
        if not kwargs.get('required', True):
            kwargs['allow_null'] = True
        super(RequireAwareFloatField, self).__init__(**kwargs)

class FloatField(RequireAwareFloatField):
    pass

serializer_field_mapping = {
    '{http://www.w3.org/2001/XMLSchema}string': CharField,
    '{http://www.w3.org/2001/XMLSchema}boolean': serializers.NullBooleanField, # ToDo: write own class
    '{http://www.w3.org/2001/XMLSchema}decimal': DecimalField,
    '{http://www.w3.org/2001/XMLSchema}float': FloatField,
    '{http://www.w3.org/2001/XMLSchema}double': FloatField,
    '{http://www.w3.org/2001/XMLSchema}duration': serializers.DurationField,
    '{http://www.w3.org/2001/XMLSchema}dateTime': serializers.DateTimeField,
    '{http://www.w3.org/2001/XMLSchema}time': serializers.TimeField,
    '{http://www.w3.org/2001/XMLSchema}date': serializers.DateField,
    '{http://www.w3.org/2001/XMLSchema}gYearMonth': gYearMonthField,
    '{http://www.w3.org/2001/XMLSchema}gYear': gYearField,
    '{http://www.w3.org/2001/XMLSchema}gMonthDay': gMonthDayField,
    '{http://www.w3.org/2001/XMLSchema}gDay': gDayField,
    '{http://www.w3.org/2001/XMLSchema}gMonth': gMonthField,
    '{http://www.w3.org/2001/XMLSchema}hexBinary': HexBinaryField,
    '{http://www.w3.org/2001/XMLSchema}base64Binary': Base64BinaryField,
    '{http://www.w3.org/2001/XMLSchema}anyURI': CharField,
    '{http://www.w3.org/2001/XMLSchema}QName': CharField,
    '{http://www.w3.org/2001/XMLSchema}NOTATION': CharField,
    '{http://www.w3.org/2001/XMLSchema}normalizedString': CharField,
    '{http://www.w3.org/2001/XMLSchema}token': CharField,
    '{http://www.w3.org/2001/XMLSchema}language': CharField,
    '{http://www.w3.org/2001/XMLSchema}NMTOKEN': CharField,
    '{http://www.w3.org/2001/XMLSchema}NMTOKENS': CharField,
    '{http://www.w3.org/2001/XMLSchema}Name': CharField,
    '{http://www.w3.org/2001/XMLSchema}NCName': CharField,
    '{http://www.w3.org/2001/XMLSchema}ID': CharField,
    '{http://www.w3.org/2001/XMLSchema}IDREF': CharField,
    '{http://www.w3.org/2001/XMLSchema}IDREFS': CharField,
    '{http://www.w3.org/2001/XMLSchema}ENTITY': CharField,
    '{http://www.w3.org/2001/XMLSchema}ENTITIES': CharField,
    '{http://www.w3.org/2001/XMLSchema}int': IntegerField,
    '{http://www.w3.org/2001/XMLSchema}integer': IntegerField,
    '{http://www.w3.org/2001/XMLSchema}positiveInteger': PositiveIntegerField,
    '{http://www.w3.org/2001/XMLSchema}nonPositiveInteger': PositiveIntegerField,
    '{http://www.w3.org/2001/XMLSchema}negativeInteger': NegativeIntegerField,
    '{http://www.w3.org/2001/XMLSchema}nonNegativeInteger': NegativeIntegerField,
    '{http://www.w3.org/2001/XMLSchema}long': IntegerField,
    '{http://www.w3.org/2001/XMLSchema}short': IntegerField,
    '{http://www.w3.org/2001/XMLSchema}byte': IntegerField,
    '{http://www.w3.org/2001/XMLSchema}unsignedByte': PositiveIntegerField,
    '{http://www.w3.org/2001/XMLSchema}unsignedInt': PositiveIntegerField,
    '{http://www.w3.org/2001/XMLSchema}unsignedLong': PositiveIntegerField,
    '{http://www.w3.org/2001/XMLSchema}unsignedShort': PositiveIntegerField,
    '{http://www.w3.org/2001/XMLSchema}anyType': CharField,
    '{http://www.w3.org/2001/XMLSchema}anySimpleType': None, # not implemented
}


class ZeepSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        meta = getattr(self.__class__, 'Meta', None)
        self.client = kwargs.pop('client', getattr(meta, 'client', None))
        self.xsd_type = kwargs.pop('xsd_type', getattr(meta, 'xsd_type', None))
        self.extend_cls = kwargs.pop('extend_cls', getattr(meta, 'extend_cls', None))
        self.xsd_overwrites = kwargs.pop('xsd_overwrites', getattr(meta, 'xsd_overwrites', {}))

        if isinstance(self.xsd_type, basestring):
            self.xsd_type = self.client.get_type(self.xsd_type)

        super(ZeepSerializer, self).__init__(**kwargs)

        if self.extend_cls:
            extend_instance(self, self.extend_cls)

    def get_fields(self):
        assert isinstance(self.xsd_type, ComplexType), (
            '{xsd_type} needs to be a zeep.xsd.ComplexType'.format(xsd_type=self.xsd_type)
        )

        assert hasattr(self.xsd_type, 'elements'), (
            '{xsd_type} has no elements attribute'.format(xsd_type=self.xsd_type)
        )

        assert len(self.xsd_type.elements) > 0, (
            '{xsd_type} has no elements'.format(xsd_type=self.xsd_type)
        )
        
        fields = OrderedDict()
        for name, e in self.xsd_type.elements:
            kwargs = {}
            xsd_overwrites = {}

            # overwrite XSD definition
            if name in self.xsd_overwrites:
                xsd_overwrites = self.xsd_overwrites[name]
            for k, v in xsd_overwrites.items():
                if k.find('_') == 0:
                    continue

                assert hasattr(e, k) and not callable(getattr(e, k)), (
                    'can not overwrite {name}.{attr} because it doesn\'t '
                    'exists or is callable'.format(name=name, attr=k)
                )
                setattr(e, k, v)
             
            if e.is_optional:
                kwargs['required'] = False
            elif e.default_value is not None and not e.accepts_multiple:
                kwargs['initial'] = e.default_value
                kwargs['default'] = e.default_value

            if e.nillable:
                kwargs['allow_null'] = True

            if isinstance(e.type, ComplexType):
                # add XSD overwrites
                kwargs['xsd_overwrites'] = xsd_overwrites.get('_xsd_overwrites', {})

                if e.accepts_multiple:
                    field = ZeepSerializer(client=self.client, xsd_type=e.type, many=True, **kwargs)
                else:
                    field = ZeepSerializer(client=self.client, xsd_type=e.type, **kwargs)

            else:
                qname = xsd_overwrites['_xsd_qname'] if '_xsd_qname' in xsd_overwrites else  str(e.type._default_qname)
                assert qname in serializer_field_mapping, (
                    '{qname} missing in serializer_field_mapping'.format(qname=qname)
                )

                if e.accepts_multiple:
                    field = serializers.ListField(
                        child=serializer_field_mapping[qname](),
                        allow_empty=e.min_occurs == 0,
                        **kwargs
                     )
                else:
                    field = serializer_field_mapping[qname](**kwargs)

            #print "\n%s = %s" % (name, field)
            #debug(e)
            #debug(e.type, level=4)

            fields[name] = field

        return fields



if __name__ == '__main__':
    import argparse
    from wsg import test_api

    parser = argparse.ArgumentParser(description='Zeep to DRF Converter')
    parser.add_argument(
        '-a', '--api', action="store", default='bb', dest="api", help='API')
    parser.add_argument(
        '-d', '--debug', action="store_true", default=False, dest="debug", help='debug mode')
    parser.add_argument(
        '-t', '--xsd_type', action="store", dest="xsd_type", help='global complex XSD type')

    opts = parser.parse_args()

    if hasattr(test_api, opts.api):
        api = getattr(test_api, opts.api)
    else:
        raise Exception("WSG API %s does not exists" % opts.api)

    xsd_type = api.client.get_type(opts.xsd_type)

    if opts.debug:
        for name, e in xsd_type.elements:
            print "%s:" % name
            debug(e)
            print "%s type:" % name
            debug(e.type, level=4)
            print ""

    else:
        s = ZeepSerializer(client=api.client, xsd_type=xsd_type)
        print s
