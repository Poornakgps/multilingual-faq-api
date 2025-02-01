from rest_framework import serializers
from .models import FAQ

class FAQCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question_en', 'answer_en'] 

    def validate_question_en(self, value):
        if not value.strip():
            raise serializers.ValidationError("Question cannot be empty.")
        return value

    def validate_answer_en(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer cannot be empty.")
        return value

    def create(self, validated_data):
        faq = FAQ.objects.create(**validated_data)
        faq._translate_fields() 
        faq.save()
        return faq

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'id', 'question_en', 'answer_en',
            'question_hi', 'answer_hi',
            'question_bn', 'answer_bn',
            'question_te', 'answer_te',
            'question_ta', 'answer_ta',
            'question_ml', 'answer_ml',
            'question_kn', 'answer_kn',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']  

    def validate_question_en(self, value):
        if not value.strip():
            raise serializers.ValidationError("Question cannot be empty.")
        return value

    def validate_answer_en(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer cannot be empty.")
        return value

class FAQLanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for translating and displaying FAQs based on language.
    Used to return specific languages for a FAQ.
    """
    class Meta:
        model = FAQ
        fields = ['id', 'question_en', 'answer_en', 'question_hi', 'answer_hi', 'question_bn', 'answer_bn',
                  'question_te', 'answer_te', 'question_ta', 'answer_ta', 'question_ml', 'answer_ml', 'question_kn', 'answer_kn']
        read_only_fields = ['id']
