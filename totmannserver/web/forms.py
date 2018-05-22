from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField
from core.models import Check, NotificationReceiver
from tagging.utils import edit_string_for_tags

class EditCheckForm(ModelForm):
    tags = CharField(max_length=300, required=False)
    
    def __init__(self, user, *args, **kwargs):
        super(EditCheckForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['tags'].initial = edit_string_for_tags(kwargs['instance'].tags)
        self.fields['notifications'] = ModelMultipleChoiceField(queryset=NotificationReceiver.objects.filter(owner=user), widget=CheckboxSelectMultiple)
    
    def save(self, commit=True):
        self.instance.tags = self.cleaned_data['tags']
        return super(EditCheckForm, self).save(commit=commit)
    
    class Meta:
        model = Check
        fields = ['prefix', 'name', 'tags', 'interval', 'expected_regex', 'alert_regex', 'allowed_return_codes', 'store_events', 'notifications']
