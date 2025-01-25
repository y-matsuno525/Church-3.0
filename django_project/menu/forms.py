from django import forms 

class AnnotationForm(forms.Form):

    content = forms.CharField(
        label="注釈内容",
        widget=forms.Textarea(attrs={
            'placeholder': '注釈を入力してください',
            'rows': 4,
            'class': 'form-control',
        }),
        empty_value=False,
    )
    public = forms.BooleanField(
        label="公開する",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )

class VerseQuestionForm(forms.Form):
    content = forms.CharField(
        label="質問内容",
        widget=forms.Textarea(attrs={
            'placeholder': '質問を入力してください',
            'rows': 4,
            'class': 'form-control',
        }),
        empty_value=False,
    )

class VerseAnswerForm(forms.Form):
    content = forms.CharField(
        label="回答内容",
        widget=forms.Textarea(attrs={
            'placeholder': '回答を入力してください',
            'rows': 4,
            'class': 'form-control',
        }),
        empty_value=False,
    )