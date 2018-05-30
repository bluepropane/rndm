from pathlib import Path
import sys
import os
import json


def system(cmd):
    print('====>', cmd)
    return os.system(cmd)


class ProjectStarter(object):
    """docstring for ProjectStarter"""
    def __init__(self, executed_from):
        super(ProjectStarter, self).__init__()
        self.root_dir = Path(executed_from).parent
        self.project_dir = None
        self.config = {}
        self._load_config()
        self._configure_dirs()

    def _load_config(self):
        self.config = json.loads((self.root_dir / 'drmn_config.json').open().read())

    def _configure_dirs(self):
        self.project_dir = Path(self.config['project_name']).absolute()

    def create_urls_py(self, app_dir):
        content = """from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]"""
        urls_py = app_dir / 'urls.py'
        urls_py.touch()
        urls_py.write_text(content)

    def create_templates_dir(self, app_dir):
        templates_dir = app_dir / 'templates'
        templates_dir.mkdir()
        (templates_dir / app_dir.name).mkdir()

    def create_docker_scripts(self):
        print('====> Creating docker scripts')
        start_sh_content = f"""
#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
cd {self.config['project_name']}
exec gunicorn {self.config['project_name']}.wsgi:application \\
    --bind 0.0.0.0:8000 \\
    --workers 4
"""
        start_sh = self.root_dir / 'start.sh'
        start_sh.touch(mode=0o766, exist_ok=True)
        start_sh.write_text(start_sh_content)

    def create_app_dirs(self):
        for app in self.config['apps']:
            system(f'python manage.py startapp {app["name"]}')
            app_root = self.project_dir / app['name']
            self.create_urls_py(app_root)
            self.create_templates_dir(app_root)

    def run(self):
        system(f'django-admin startproject {self.config["project_name"]}')
        self.create_docker_scripts()
        os.chdir(self.project_dir)
        print('====> cd to', os.getcwd())
        self.create_app_dirs()

if __name__ == '__main__':
    ps = ProjectStarter(sys.argv[0])
    ps.run()
