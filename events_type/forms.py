from django import forms

from events_type import models as event_type_models


class CreateConference(forms.ModelForm):

    class Meta:
        """
        Класс мета-данных
        """

        # модель основания
        model = event_type_models.Conference
        # используемые поля
        fields = ["speakers"]


class CreateMeeting(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateMeeting, self).__init__(*args, **kwargs)
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
        model = event_type_models.Meeting
        # используемые поля
        fields = ["need_visit", "theme"]


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
