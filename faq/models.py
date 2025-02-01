from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from django.utils import timezone

class FAQ(models.Model):
    question_en = models.TextField(blank=True)  
    answer_en = RichTextField(blank=True)  


    question_hi = models.TextField(blank=True)
    answer_hi = RichTextField(blank=True)

    question_bn = models.TextField(blank=True)
    answer_bn = RichTextField(blank=True)

    question_te = models.TextField(blank=True)
    answer_te = RichTextField(blank=True)

    question_ta = models.TextField(blank=True)
    answer_ta = RichTextField(blank=True)

    question_ml = models.TextField(blank=True)
    answer_ml = RichTextField(blank=True)
    
    question_kn = models.TextField(blank=True)
    answer_kn = RichTextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

    def get_translated(self, lang):
        lang = lang.lower()
        return {
            'question': getattr(self, f'question_{lang}', self.question_en),
            'answer': getattr(self, f'answer_{lang}', self.answer_en)
        }

    def save(self, *args, **kwargs):
        if not self.pk or self._has_english_changed():
            self._translate_fields()
        super().save(*args, **kwargs)

    def _has_english_changed(self):
        if not self.pk:
            return False
        original = FAQ.objects.get(pk=self.pk)
        return (self.question_en != original.question_en or 
                self.answer_en != original.answer_en)

    def _translate_fields(self):
        translator = Translator()
        for lang in ['hi', 'bn', 'te', 'ta', 'ml', 'kn']:
            self._translate_field(translator, 'question', lang)
            self._translate_field(translator, 'answer', lang)

    def _translate_field(self, translator, field, lang):
        value = getattr(self, f'{field}_en', None)
        if value:
            try:
                translated = translator.translate(value, dest=lang).text
                # print(f"Translated {field}_en to {field}_{lang}: {translated}") 
            except Exception as e:
                translated = value 
                print(f"Error during translation for {lang}: {e}")
        else:
            translated = "" 

        # Set the translated field
        setattr(self, f'{field}_{lang}', translated)
        # print(f"Set {field}_{lang}: {translated}") 

