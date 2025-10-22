from .models import String
from rest_framework import serializers


class StringValueField(serializers.Field):
    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError('Invalid data type for "value" (must be string)')
        return data
    def to_representation(self, value):
        return value



class ValidateString(serializers.Serializer):
    value = StringValueField()
    
    def validate_value(self, value):
        if not isinstance (value, str):
            raise serializers.ValidationError('Invalid data type for "value" (must be string)')
        return value
        



class StringSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    class Meta:
        model = String
        fields = ['id', 'value', 'properties', 'created_at']
        read_only_fields = ['id', 'length', 'is_palindrome', 'unique_characters', 'word_count', 'sha256_hash', 'character_frequency_map', 'created_at']
        
        
    def get_properties(self, obj):
        return {
                            'length': obj.length,
                            'is_palindrome': obj.is_palindrome,
                            'unique_characters': obj.unique_characters,
                            'word_count': obj.word_count,
                            'sha256_hash': obj.sha256_hash,
                            'character_frequency_map': obj.character_frequency_map,
                        }
        
                        