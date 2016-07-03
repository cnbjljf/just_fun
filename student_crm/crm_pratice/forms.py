#!/usr/bin/env python
from django import forms
from django.core.exceptions import ValidationError
from crm_pratice import models
from django.forms import Form,ModelForm

'''
class Customer(forms.Form):
    course_type = forms.CharField(widget=forms.Select(choices=models.course_type_choices,
                                                      attrs={'class'"form-control"}))

    qq = forms.CharField(max_length=18,
                         min_length=4,
                         error_messages={'required':u'QQ号必须填写'},
                         widget=forms.TextInput())
    name = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(max_length=11,min_length=11,widget=forms.TextInput())
    course = forms.CharField(widget=forms.Select(choices=models.Course),
                             error_messages={
                                ''
                             })
'''

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ()

    def __init__(self,*args,**kwargs):
        #  继承父类，后重写自己的类
        super(CustomerModelForm,self).__init__(*args,**kwargs)

        print(self.base_fields)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})


class ClassModelForm(ModelForm):
    class Meta:
        model = models.ClassList
        exclude = ()

    def __init__(self,*args,**kwargs):
        super(ClassModelForm,self).__init__(*args,**kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})


class UserProfileModelForm(ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ()

    def __init__(self,*args,**kwargs):
        super(UserProfileModelForm,self).__init__(*args,**kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})



class StudyRecordModelForm(ModelForm):
    class Meta:
        model = models.StudyRecord
        exclude = ()

    def __init__(self,*args,**kwargs):
        super(StudyRecordModelForm,self).__init__(*args,**kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})


