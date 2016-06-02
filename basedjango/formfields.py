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

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.admin.widgets import AdminTextareaWidget

from .translated_text import TranslatedText
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

    def widget_attrs(self, widget):
        attrs = super(SingleLanguageCharField, self).widget_attrs(widget)
        attrs.setdefault('data-lang', self.language)
        return attrs

    def clean(self, value):
        return TranslatedText(**{self.language: value})


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

    def __init__(self, *args, **kwargs):
        on_admin = kwargs.pop('on_admin', False)
        self.languages = kwargs.pop('languages', settings.LANGUAGES)

        fields = []

        # add a language chooser if we currently support more then one language.
        if len(self.languages) > 1:
            fields.append(forms.ChoiceField(choices=self.languages))

        translated_widget = kwargs.get('widget', self.translated_widget)
        widget_cls = TranslatedTextWidget
        if on_admin is True:
            widget_cls = TranslatedTextAdminWidget

        self.widget = widget_cls(languages=self.languages, translated_widget=translated_widget)

        field_kwargs = kwargs.copy()
        field_kwargs.pop('initial', {})  # this is the dict
        field_kwargs['required'] = False

        for lang, _name in self.languages:
            fields.append(self.translated_field(**field_kwargs))

        super(TranslatedTextFormField, self).__init__(fields=fields, require_all_fields=False,
                                                      required=kwargs.get('required', True))

    def compress(self, data_list):
        if len(self.languages) > 1:
            data_list.pop(0)  # first value is the selected language
        languages = [l for l, _ in self.languages]

        # If we only have a single language and no input, data_list is an empty list and we
        # have to set an empty value for that language.
        #
        # TODO: This method is never called if require=True and we don't enter a value. This is
        #       checked somewhere further up in this case.
        if len(languages) == 1 and data_list == []:
            data_list = ['']

        return TranslatedText(**{k: v for k, v in zip(languages, data_list) if v})
