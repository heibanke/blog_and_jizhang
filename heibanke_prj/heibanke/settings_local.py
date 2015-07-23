

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
DATABASES = {
	'default':{
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'ijizhang',
		'USER': 'test',
		'PASSWORD':'123',
		'HOST':'localhost',
		'PORT':'3306',
	}
}
"""