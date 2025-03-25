from django import forms

from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

class EntryForm(forms.ModelForm):
    # Meta类指出了表单基于的模型以及要在表单中包含哪些字段
    class Meta: 
        model = Entry #表单基于的模型
        fields = ['text'] #表单字段
        labels = {'text':''} #字段标签
        widgets = {'text':forms.Textarea(attrs={'cols':80})}

