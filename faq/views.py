from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import FAQ
from .serializers import FAQCreateSerializer, FAQSerializer
from django.core.cache import cache
from django.conf import settings

@api_view(['POST'])
def create_faq(request):
    """
    Create a new FAQ entry and return it with all translations.
    """
    if request.method == 'POST':
        serializer = FAQCreateSerializer(data=request.data)
        if serializer.is_valid():
            faq = serializer.save() 
            faq._translate_fields()  
            faq.save() 

            translated_faq = {
                'id': faq.id,
                'question_en': faq.question_en,
                'answer_en': faq.answer_en,
                'question_hi': faq.question_hi,
                'answer_hi': faq.answer_hi,
                'question_bn': faq.question_bn,
                'answer_bn': faq.answer_bn,
                'question_te': faq.question_te,
                'answer_te': faq.answer_te,
                'question_ta': faq.question_ta,
                'answer_ta': faq.answer_ta,
                'question_ml': faq.question_ml,
                'answer_ml': faq.answer_ml,
                'question_kn': faq.question_kn,
                'answer_kn': faq.answer_kn,
            }

            # Clear cache after creating new FAQ
            cache.clear()

            return Response(translated_faq, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_faq(request, id):
    """
    Update an existing FAQ entry by ID.
    """
    try:
        faq = FAQ.objects.get(id=id)
    except FAQ.DoesNotExist:
        return Response({'detail': 'FAQ not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        serializer = FAQSerializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            faq = serializer.save()
            faq._translate_fields()  
            faq.save()  
            translated_faq = faq.get_translated('en') 

            # Clear cache after updating FAQ
            cache.clear()

            return Response(translated_faq, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_faqs(request):
    """
    Get all FAQ entries.
    """
    cache_key = 'all_faqs'
    cached_faqs = cache.get(cache_key)

    if cached_faqs is None:
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        cached_faqs = serializer.data
        cache.set(cache_key, cached_faqs, timeout=3600)  # Cache for 1 hour

    return Response(cached_faqs)

@api_view(['GET'])
def get_faqs_by_language(request, lang):
    """
    Get all FAQ entries in a specific language.
    """
    if lang not in ['en', 'hi', 'bn', 'te', 'ta', 'ml', 'kn']:
        return Response({'detail': 'Language not supported.'}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f'faqs_{lang}'
    cached_faqs = cache.get(cache_key)

    if cached_faqs is None:
        faqs = FAQ.objects.all()
        translated_faqs = [faq.get_translated(lang) for faq in faqs]
        cache.set(cache_key, translated_faqs, timeout=3600)  # Cache for 1 hour
    else:
        translated_faqs = cached_faqs

    return Response(translated_faqs)

@api_view(['GET'])
def get_faq_by_language(request, id, lang):
    """
    Get a specific FAQ entry by ID and language.
    """
    if lang not in ['en', 'hi', 'bn', 'te', 'ta', 'ml', 'kn']:
        return Response({'detail': 'Language not supported.'}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f'faq_{id}_{lang}'
    cached_faq = cache.get(cache_key)

    if cached_faq is None:
        try:
            faq = FAQ.objects.get(id=id)
        except FAQ.DoesNotExist:
            return Response({'detail': 'FAQ not found.'}, status=status.HTTP_404_NOT_FOUND)

        translated_faq = faq.get_translated(lang) 
        cache.set(cache_key, translated_faq, timeout=3600) 
    else:
        translated_faq = cached_faq

    return Response(translated_faq)

@api_view(['DELETE'])
def delete_faq(request, id):
    """
    Delete a specific FAQ entry by ID.
    """
    try:
        faq = FAQ.objects.get(id=id)
    except FAQ.DoesNotExist:
        return Response({'detail': 'FAQ not found.'}, status=status.HTTP_404_NOT_FOUND)

    faq.delete()

    # Clear cache after deleting FAQ
    cache.clear()

    return Response({'detail': 'FAQ deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
