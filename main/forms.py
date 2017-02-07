from django import forms
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from blog.models import Answer
from django.contrib import admin


def name_check(name):
    for i in range(len(name)):
        if not ((name[i] >= u'\u4e00' and name[i] <= u'\u9fa5')
                or (name[i] >= u'\u0041' and name[i] <= u'\u005a')
                or (name[i] >= u'\u0061' and name[i] <= u'\u007a')):
            raise ValidationError(u"请输入14个字符以上的用户名，只能包括中文和英文")

def password_check(password):
    for i in range(len(password)):
        if not ((password[i] >= u'\u0030' and password[i] <= u'\u0039')
                or (password[i] >= u'\u0041' and password[i] <= u'\u005a')
                or (password[i] >= u'\u0061' and password[i] <= u'\u007a')):
            raise ValidationError(u"请输入6个字符以上的密码，只能包括数字和英文")

def password_validator(password):
    if len(password) < 6:
        raise ValidationError(u"密码不少于6位")


def name_validator(name):
    if len(name) > 14:
        raise ValidationError(u"用户名不能大于14个字符")

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Answer
        fields = ("content",)

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": u'邮箱不能为空'})
    password = forms.CharField(error_messages={"required": u'密码不能为空'})


class RegisterForm(forms.Form):
    name = forms.CharField(error_messages={"required": u'用户名不能为空'}, validators=[
                           name_validator, name_check])
    email = forms.EmailField(error_messages={"required": u'邮箱不能为空'})
    password = forms.CharField(error_messages={"required": u'密码不能为空'}, validators=[
                               password_validator, password_check])

class AvatarForm(forms.Form):
    avatar = forms.ImageField()
class DescForm(forms.Form):
    desc = forms.CharField(max_length=14)


class QuestionForm(forms.Form):
    # 标题
    title = forms.CharField(required=True)

    # 问题描述
    desc = forms.CharField(required=True)

    # 主题描述
    topic = forms.CharField(required=True)

class AnswerForm(forms.Form):
    content = forms.CharField(required=True)

class VoteForm(forms.Form):
    vote = forms.CharField(required=True)


def title_validator(title):
    if len(title) > 50:
        raise ValidationError(u"请输入50个字符以内的问题")


def desc_validator(desc):
    if len(desc) > 1000:
        raise ValidationError(u"请输入1000个字符以内的问题")


def topics_validator(topics):
    if len(topics) > 14:
        raise ValidationError(u"请输入14个字符以内的话题")
