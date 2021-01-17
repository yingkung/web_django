from django.contrib import admin
from .models import Question, Choice
# Register your models here.
from django.contrib import admin

# admin.site.register(Question)
# admin.site.register(Choice)

# class QuestionAdmin(admin.ModelAdmin):
#     """创建模型后台类"""
#     fields = ['pub_date', 'question_text']

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

""" 用字段集的方式将表单字段分类 """
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields':['pub_date']}),
    ]
    inlines = [ChoiceInline]  # 将choice的添加，与question的添加合并到一个页面中


admin.site.register(Question, QuestionAdmin)