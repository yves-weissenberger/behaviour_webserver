from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text','pub_date','was_published_recently')   
#This shows what to display on the admin site where
#the questions are listed

    list_filter = ['pub_date']
    search_fields = ['question_text']



#The question admin is an object that is passed as the second 
#argument to the site.register method which modifies the way 
#the first argument is displayed.
admin.site.register(Question, QuestionAdmin)

#admin.site.register(Choice)
