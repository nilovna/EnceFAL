# -*- encoding: utf-8 -*-
from django.forms import ModelForm
from project.encefal.models import Exemplaire

class ExemplaireForm(ModelForm):
    class Meta:
        model = Exemplaire
