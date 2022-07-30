"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# html socket -> django server로 옮기기 위해 python-socketio 라이브러리 설치
import socketio
# from post.socketioserver import sio
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
# django_app = get_wsgi_application()
# application = socketio.WSGIApp(sio, django_app)
