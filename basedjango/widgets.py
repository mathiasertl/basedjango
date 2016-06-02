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
        self.languages = kwargs.pop('languages', settings.LANGUAGES)

        widgets = [
            forms.Select(choices=self.languages, attrs={'class': 'basedjango-lang-selector'}),
        ]

        translated_widget = kwargs.pop('translated_widget', self.translated_widget)
        for code, _lang in self.languages:
            attrs = {'data-lang': code}
            if code != self.lang:
                attrs['style'] = 'display: none;'

            widgets.append(translated_widget(attrs=attrs))
        kwargs.setdefault('widgets', widgets)
        super(TranslatedTextWidget, self).__init__(*args, **kwargs)

    @property
    def lang(self):
        """Returns the currently active language of this thread.

        If the current language is in a dialect that is not in settings.LANGUAGES, the main
        language is returned instead. This is important because the default installation uses
        settings.LANGUAGE_CODE = "en-us", which is not part of settings.LANGUAGES.
        """

        lang = get_language()
        supported = [k for k, v in self.languages]
        if lang not in supported and '-' in lang:
            # The default settings.LANGUAGE_CODE is 'en-us', which is not in settings.LANGUAGES, so
            # we fallback to just 'en' in this case.
            return lang.split('-', 1)[0]
        return lang

    def decompress(self, value):
        if not value:
            return [self.lang] + ['' for l in self.languages]
        return [self.lang] + [value.get(l, '') for l, _ in self.languages]

    def format_output(self, rendered_widgets):
        selector = rendered_widgets.pop(0)
        translations = super(TranslatedTextWidget, self).format_output(rendered_widgets)
        translations = '<div class="basedjango-translations">' + translations + '</div>'

        return '<div class="basedjango-lang-wrapper">' + selector + translations + '</div>'


class TranslatedTextAdminWidget(TranslatedTextWidget):
    class Media:
        extends = False
        js = (
            'basedjango/js/translatedtextwidget.js',
        )
        css = {
            'all': ('basedjango/css/translatedtextwidget.css', ),
        }
