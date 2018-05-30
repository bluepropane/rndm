from pathlib import Path
import sys
import os
import json


def system(cmd):
    print('====>', cmd)
    return os.system(cmd)


class ProjectStarter(object):
    """docstring for ProjectStarter"""
    def __init__(self, target_path):
        super(ProjectStarter, self).__init__()
        self.root_dir = Path('.').absolute()
        self.src_dir = Path(target_path).absolute()
        self.src_dir.mkdir()
        self.server_dir = None
        self.config = {}
        self._load_config()
        self._configure_dirs()

    def _load_config(self):
        self.config = json.loads((Path('.') / 'drmn_config.json').open().read())

    def _configure_dirs(self):
        self.server_dir = (self.src_dir / self.config['project_name']).absolute()
        self.tools_dir = (self.root_dir / 'tools').absolute()
        self.web_dir = (self.src_dir / f'web-{self.config["project_name"]}').absolute()

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

    def create_startup_scripts(self):
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
        start_sh = self.server_dir / 'start.sh'
        start_sh.touch(mode=0o766, exist_ok=True)
        start_sh.write_text(start_sh_content)

    def create_app_dirs(self):
        os.chdir(self.server_dir)
        for app in self.config['apps']:
            system(f'python manage.py startapp {app["name"]}')
            app_root = self.server_dir / app['name']
            self.create_urls_py(app_root)
            self.create_templates_dir(app_root)

    def create_react_app(self):
        self.web_dir.mkdir()
        os.chdir(self.tools_dir)
        system('docker build -t node-cra -f create-react-dockerfile .')
        system(f'docker run --rm -t -v {self.web_dir}:/cra node-cra ')
        system(f'docker rmi node-cra')

    def create_django_project(self):
        os.chdir(self.src_dir)
        system(f'django-admin startproject {self.config["project_name"]}')
        system(f'cp {self.root_dir / "requirements.txt"} {self.server_dir}')
        self.create_app_dirs()

    def eject_react_app(self):
        os.chdir(self.web_dir)
        system('npm run eject')

    def copy_docker_files(self):
        # system(f'cp {self.tools_dir / "Dockerfile-web"} {self.web_dir / "Dockerfile"}')
        # system(f'cp {self.tools_dir / "Dockerfile-server"} {self.server_dir / "Dockerfile"}')
        for file_type in ('', '.override', '.production'):
            print(f'====> copying docker-compose{file_type}.yml')
            compose_file = (self.tools_dir / f'docker-compose{file_type}.yml')
            content = compose_file.open().read().format(**{'config': self})
            target_file = self.src_dir / compose_file.name
            target_file.touch()
            target_file.write_text(content)

    def run(self):
        self.create_django_project()
        self.create_startup_scripts()
        self.create_react_app()
        self.copy_docker_files()
        # self.eject_react_app()

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print(f'Usage: python {sys.argv[0]} <target folder>')
    #     exit(1)
    ps = ProjectStarter('src')
    ps.run()
