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
# see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup

setup(
    name = "basedjango",
    version = "0.0.1",
    author = "Mathias Ertl",
    author_email = "mati@er.tl",
    description = "A Django app with some reusable classes and templates.",
    license = 'GPLv3+',
    url = "https://github.com/mathiasertl/basedjango",
    packages=['basedjango'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Topic :: Utilities',
    ],
)
