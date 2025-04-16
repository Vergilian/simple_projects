import io

from rest_framework import serializers
from .models import Person

class PersonSerializers (serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('title', 'category_id')

class UserModel:
     def __init__(self, title, content):
        self.title = title
        self.content = content

class UserSerializers (serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=1000)

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
def encode():
    model = UserModel('Tom','hello, my friend')
    model_sr = UserSerializers(model)
    print(model_sr, type(model_sr))
    json = JSONRenderer().render(model_sr.data)
    print(json, type(json))

def decode():
    sr = io.BytesIO(b'{"title": "Tom", "content": "hello, my friend"}')
    data = JSONParser().parse(sr)
    serializer = UserSerializers(data=data)
    serializer.is_valid()
    print(serializer.validated_data)