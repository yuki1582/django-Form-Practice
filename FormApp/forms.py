from django import forms
from django.core import validators

from .models import Post

def check_name(value):
    if value == 'あああああ':
        raise validators.ValidationError('その名前は登録できない')

class UserInfo(forms.Form):
    name = forms.CharField(label='名前', min_length=5, max_length=10, validators=[check_name])
    age = forms.IntegerField(label='年齢', validators=[validators.MinValueValidator(20, message='20以上にしましょう')])
    mail = forms.EmailField(
        label='メールアドレス',
        widget=forms.TextInput(attrs={'class': 'mail-class', 'placeholder': 'sample@mail.com'}),    
    )
    verify_mail = forms.EmailField(
        label='メールアドレス再入力',
        widget=forms.TextInput(attrs={'class': 'mail-class', 'placeholder': 'sample@mail.com'}),    
    )
    is_married = forms.BooleanField(initial=True)
    birthday = forms.DateField(initial='1990-01-01')
    salary = forms.DecimalField()
    job = forms.ChoiceField(choices=(
        (1, '正社員'),
        (2, '自営業'),
        (3, '学生'),
        (4, '無職'),
    ), widget=forms.RadioSelect)
    hobbies = forms.MultipleChoiceField(choices=(
        (1, 'スポーツ'),
        (2, '読書'),
        (3, '映画鑑賞'),
        (4, 'その他'),
    ), widget=forms.CheckboxSelectMultiple)
    homepage = forms.URLField(required=False)
    memo = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(UserInfo, self).__init__(*args, **kwargs)
        self.fields['job'].widget.attrs['id'] = 'id_job'
        self.fields['hobbies'].widget.attrs['class'] = 'hobbies_class'

    def clean_homepage(self):
        homepage = self.cleaned_data['homepage']
        if not homepage.startswith('https'):
            raise forms.ValidationError('ホームページのURLはhttpsのみ!!')
    
    def clean(self):
        cleaned_data = super().clean()
        mail = cleaned_data['mail']
        verify_mail = cleaned_data['verify_mail']
        if mail != verify_mail:
            raise forms.ValidationError('メールアドレスが一致しません！')
        
class BaseForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        print(f'Form: {self.__class__.__name__}実行')
        return super(BaseForm, self).save(*args, **kwargs)
    
class PostModelForm(BaseForm):

    memo = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 30, 'cols': 20})
    )
    
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['name', 'title']
        # exclude = ['title']

    def save(self, *args, **kwargs):
        obj = super(PostModelForm, self).save(commit=False, *args, **kwargs)
        obj.name = obj.name.upper()
        print(type(obj))
        print('save実行')
        obj.save()
        return obj
    