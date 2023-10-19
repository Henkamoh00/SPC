from django import forms
from .models import Comment

# الخاص به label مع اخفاء Textarea توجد طريقتين لتعريف
# كل منهما به طريقة CommentUpdateForm و CommentForm النموذجين
# الطريقة الاولى أحدث

class CommentForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     self.fields['comment'].label = ""

    comment = forms.CharField(label=False, widget=forms.Textarea(attrs={'class':'commentTextArea', 'wrap':'hard', 'placeholder':'اضف تعليقًا...'}))
    class Meta:
        model = Comment
        fields = [ 'comment']
        widgets = {
            # 'comment':forms.Textarea(attrs={'class':'commentTextArea'}),
        }


class CommentUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = ""

    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment':forms.Textarea(attrs={'disabled':'','hidden':'', 'class':'commentTextArea commentUpdateTextArea'}),
        }
