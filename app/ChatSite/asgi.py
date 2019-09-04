import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatSite.settings')


from channels.routing import get_default_application

django.setup()
application = get_default_application()