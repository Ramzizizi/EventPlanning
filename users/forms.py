from django.forms import modelformset_factory

from users import models as user_models


SpeakerFormSet = modelformset_factory(
    user_models.Speaker, fields=("speaker", "theme"), extra=1
)
