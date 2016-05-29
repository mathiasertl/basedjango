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

import json

from django.conf import settings
from django.db import models

from .formfields import TranslatedTextFormField


class TranslatedText(dict):
    # might be useful for future extensions to have a subclass
    pass


class TranslatedTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = {k: '' for k, v in settings.LANGUAGES}
        super(TranslatedTextField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(TranslatedTextField, self).deconstruct()
        del kwargs['default']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return TranslatedText(**json.loads(value))

    def to_python(self, value):
        if isinstance(value, TranslatedText):
            return value

        if value is None:
            return value

        return TranslatedText(**json.loads(value))

    def get_prep_value(self, value):
        # convert python object to database represenation
        return json.dumps(value)

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', TranslatedTextFormField)
        return super(TranslatedTextField, self).formfield(**kwargs)
