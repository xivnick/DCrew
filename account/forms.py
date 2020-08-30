from django.contrib.auth.models import User

from django import forms


class LoginForm(forms.ModelForm):

    class Meta:
        model = User

        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '아이디',
                'class': 'no-margin',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': '비밀번호',
            }),
        }


class SignUpForm(forms.ModelForm):

    password2 = forms.CharField(
        label='password2',
        widget=forms.PasswordInput(attrs={
            'placeholder': '비밀번호 확인',
            'class': 'no-margin',
        })
    )

    class Meta:
        model = User
        # fields 에는 해당 모델에 대해 입력받을 필드들을 나열한다.
        # + 추가 필드도 포함될수 있다 -> 위에서 설정한 필드도 추가되고 목록에서 겹치면 오버라이드 한다
        # fields에 써진 순서대로 출력된다.
        fields = ['username', 'password', 'password2', 'first_name', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '아이디',
                'class': 'no-margin',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': '비밀번호',
                'style': "margin-bottom: 10px",
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': '이름',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': '이메일',
            }),
        }

    # clean_필드명
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

        # 항상 해당 필드의 값을 리턴한다.
        return cd['password2']

