
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")


from models import cursos



python = cursos('python','curso de python','curso-python')

python.save()