from django import forms

from events_type import models as event_type_models

from django.forms.models import BaseModelFormSet


class CreateConferenceFormSet(forms.models.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(CreateConferenceFormSet, self).__init__(*args, **kwargs)
        self.queryset = event_type_models.Themes.objects.none()
        self.fields["theme"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "height: 0px;",
                "id": "text_form_3",
            }
        )

    class Meta:
        """
        Класс мета-данных
        """

        # модель основания
        model = event_type_models.Themes
        # используемые поля
        fields = ["speaker", "theme"]


class CreateConference(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateConference, self).__init__(*args, **kwargs)
        self.fields["theme"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "height: 0px;",
                "id": "text_form_2",
            }
        )
        self.fields["speaker"].widget.attrs.update(
            {
                "class": "form-select",
                "id": "select_form_2",
            }
        )

    class Meta:
        """
        Класс мета-данных
        """

        # модель основания
        model = event_type_models.Themes
        # используемые поля
        fields = ["speaker", "theme"]


class CreateMeeting(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateMeeting, self).__init__(*args, **kwargs)
        self.fields["meeting_theme"].widget.attrs.update(
            {
                "class": "form-control",
                "style": "height: 0px;",
                "id": "text_form_3",
            }
        )

    class Meta:
        """
        Класс мета-данных
        """

        # модель основания
        model = event_type_models.Meeting
        # используемые поля
        fields = ["need_visit", "meeting_theme"]


class CreateConfCall(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateConfCall, self).__init__(*args, **kwargs)
        self.fields["call_url"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "text_form_1",
            }
        )

    class Meta:
        """
        Класс мета-данных
        """

        # модель основания
        model = event_type_models.ConfCall
        # используемые поля
        fields = ["call_url"]
