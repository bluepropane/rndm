from pathlib import Path
import sys
import os
import json


def create_urls_py(app_dir):
    content = """from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]"""
    urls_py = app_dir / 'urls.py'
    urls_py.touch()
    urls_py.write_text(content)

def create_templates_dir(app_dir):
    templates_dir = app_dir / 'templates'
    templates_dir.mkdir()
    (templates_dir / app_dir.name).mkdir()

def system(cmd):
    print('====>', cmd)
    return os.system(cmd)

if __name__ == '__main__':
    config = json.loads(open('project_config.json').read())
    system(f'django-admin startproject {config["project_name"]}')
    project_root = Path(config['project_name']).absolute()
    os.chdir(project_root)
    print('====> cd to', os.getcwd())
    for app in config['apps']:
        system(f'python manage.py startapp {app["name"]}')
        app_root = project_root / app['name']
        create_urls_py(app_root)
