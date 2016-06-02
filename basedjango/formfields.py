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
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.admin.widgets import AdminTextareaWidget

from .widgets import TranslatedTextWidget
from .widgets import TranslatedTextAdminWidget


class SingleLanguageCharField(forms.CharField):
    """A formfield that contains the text for a single translated language.

    This field returns a dictionary of the language, suitable e.g. for a
    :py:class:`models.TranslatedCharField`. Example::

        >>> from django.conf import settings
        >>> from basedjango.formfields import SingleLanguageCharField
        >>> settings.LANGUAGE_CODE
        'en-us'
        >>> f = SingleLanguageCharField()
        >>> f.clean('foo')
        {'en-us': 'foo'}


    Parameters
    ----------

    language : str, optional
        The language this field uses. The default is ``settings.LANGUAGE_CODE``.
    admin : bool, optional
        If True, the default widget is ``AdminTextInputWidget`` instead of just ``TextInput``. Use
        this parameter in admin forms.
    """
    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop('language', settings.LANGUAGE_CODE)
        if kwargs.pop('admin', False):
            kwargs.setdefault('widget', AdminTextInputWidget)

        super(SingleLanguageCharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return {self.language: value, }


class SingleLanguageTextField(SingleLanguageCharField):
    """Same as SingleLanguageCharField``, except it uses a Textarea by default."""

    def __init__(self, *args, **kwargs):
        if kwargs.pop('admin', False):
            kwargs.setdefault('widget', AdminTextareaWidget)
        else:
            kwargs.setdefault('widget', forms.Textarea)
        super(SingleLanguageTextField, self).__init__(*args, **kwargs)


class TranslatedTextFormField(forms.MultiValueField):
    translated_field = forms.CharField
    translated_widget = forms.TextInput

    _TranslatedText = None

    def __init__(self, *args, **kwargs):
        on_admin = kwargs.pop('on_admin', False)

        fields = []

        # add a language chooser if we currently support more then one language.
        if len(settings.LANGUAGES) > 1:
            fields.append(forms.ChoiceField(choices=settings.LANGUAGES))

        translated_widget = kwargs.get('widget', self.translated_widget)
        widget_cls = TranslatedTextWidget
        if on_admin is True:
            widget_cls = TranslatedTextAdminWidget

        self.widget = widget_cls(translated_widget=translated_widget)

        field_kwargs = kwargs.copy()
        field_kwargs.pop('initial')  # this is the dict
        field_kwargs['required'] = False

        for lang, _name in settings.LANGUAGES:
            fields.append(self.translated_field(**field_kwargs))
        super(TranslatedTextFormField, self).__init__(fields=fields, require_all_fields=False)

    @property
    def TranslatedText(self):
        # we cannot import this on the module level, because it would be a circular import
        if self._TranslatedText is None:
            mod = import_module('basedjango.modelfields')
            self._TranslatedText = mod.TranslatedText
        return self._TranslatedText

    def compress(self, data_list):
        data_list.pop()  # first value is the language
        translations = data_list[1:]
        languages = [l for l, _ in settings.LANGUAGES]

        return self.TranslatedText(**{k: v for k, v in zip(languages, translations) if v})
