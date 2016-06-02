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

from django.conf import settings
from django.utils.translation import get_language


class TranslatedText(dict):
    # might be useful for future extensions to have a subclass
    def code(self, code):
        if code not in self and '-' in code:
            code = code.split('-', 1)[0]

        return self.get(code, 'untranslated')

    def has_code(self, code):
        if self.get(code):
            return True
        if '-' in code:
            code = code.split('-', 1)[0]
            return bool(self.get(code))
        return False

    @property
    def has_default_language(self):
        return self.has_code(settings.LANGUAGE_CODE)

    def __str__(self):
        return self.code(get_language())
