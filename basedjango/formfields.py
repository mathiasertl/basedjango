# -*- coding: utf-8 -*-
#
# This file is part of basedjango (https://github.com/mathiasertl/basedjango).
#
# basedjango is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# basedjango is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with basedjango. If not,
# see <http://www.gnu.org/licenses/>

from importlib import import_module

from django import forms
from django.conf import settings
from .widgets import TranslatedTextWidget


class TranslatedTextFormField(forms.MultiValueField):
    translated_field = forms.CharField
    translated_widget = forms.Textarea

    _TranslatedText = None

    def __init__(self, *args, **kwargs):
        language_chooser = forms.ChoiceField(choices=settings.LANGUAGES)

        fields = [
            language_chooser,
        ]

        translated_widget = kwargs.get('widget', self.translated_widget)
        self.widget = TranslatedTextWidget(translated_widget=translated_widget)

        field_kwargs = kwargs.copy()
        translations = field_kwargs.pop('initial')  # this is the dict
        field_kwargs['required'] = False

        for lang, _name in settings.LANGUAGES:
            fields.append(self.translated_field(
                initial=translations.get(lang, ''), **field_kwargs))
        super(TranslatedTextFormField, self).__init__(fields=fields, require_all_fields=False)

    @property
    def TranslatedText(self):
        # we cannot import this on the module level, because it would be a circular import
        if self._modelfields is None:
            mod = import_module('.modelfields')
            self._TranslatedText = mod.TranslatedText
        return self._TranslatedText

    def compress(self, data_list):
        data_list.pop()  # first value is the language
        translations = data_list[1:]
        languages = [l for l, _ in settings.LANGUAGES]

        return self.TranslatedText(**{k: v for k, v in zip(languages, translations) if v})
