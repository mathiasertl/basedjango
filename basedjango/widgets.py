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
# see <http://www.gnu.org/licenses/

from django.conf import settings
from django import forms
from django.utils.translation import get_language


class TranslatedTextWidget(forms.MultiWidget):
    translated_widget = forms.TextInput

    def __init__(self, *args, **kwargs):
        widgets = [
            forms.Select(choices=settings.LANGUAGES),
        ]

        translated_widget = kwargs.pop('translated_widget', self.translated_widget)
        for code, lang in settings.LANGUAGES:
            widgets.append(translated_widget(attrs={'data-lang': code}))
        kwargs.setdefault('widgets', widgets)
        super(TranslatedTextWidget, self).__init__(*args, **kwargs)

    def decompress(self, value):
        lang = [get_language()]

        if not value:
            return lang + ['' for l in settings.LANGUAGES]
        return lang + [value.get(l, '') for l, _ in settings.LANGUAGES]
