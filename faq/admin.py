from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_en', 'question_hi', 'question_bn', 'created_at', 'updated_at') 
    search_fields = ('question_en', 'answer_en', 'question_hi', 'answer_hi') 
    list_filter = ('created_at', 'updated_at')  
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at') 

    fieldsets = (
        ("English (Default)", {'fields': ('question_en', 'answer_en')}),
        ("Hindi", {'fields': ('question_hi', 'answer_hi')}),
        ("Bengali", {'fields': ('question_bn', 'answer_bn')}),
        ("Telugu", {'fields': ('question_te', 'answer_te')}),
        ("Tamil", {'fields': ('question_ta', 'answer_ta')}),
        ("Malayalam", {'fields': ('question_ml', 'answer_ml')}),
        ("Kannada", {'fields': ('question_kn', 'answer_kn')}),
        ("Metadata", {'fields': ('created_at', 'updated_at')}),
    )
