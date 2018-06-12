from pathlib import Path
import sys
import os
import json


def system(cmd):
    print('====>', cmd)
    return os.system(cmd)

class FileFormatter(object):
    """docstring for FileFormatter"""
    def __init__(self, kv):
        super(FileFormatter, self).__init__()
        for k, v in kv.items():
            setattr(self, k, v)


class ProjectStarter(object):
    """docstring for ProjectStarter"""
    def __init__(self, target_path='src', rollback=True):
        super(ProjectStarter, self).__init__()
        self.dir = {'src': Path(target_path).absolute()}
        self.config = {}
        self.should_rollback = rollback
        self._load_config()
        self._configure_dirs()

    def _load_config(self):
        self.config = json.loads((Path('.') / 'rndm_conf.json').open().read())

    def _configure_dirs(self):
        self.dir['root'] = Path('.').absolute()
        self.dir['server'] = (self.dir['src'] / self.config['project_name']).absolute()
        self.dir['conf'] = (self.dir['root'] / 'conf').absolute()
        self.dir['dockerconf'] = (self.dir['root'] / 'dockerconf').absolute()
        self.dir['web'] = (self.dir['src'] / f'web-{self.config["project_name"]}').absolute()
        self.dir['boilerplate_cache'] = (self.dir['root'] / 'cached_boilerplates').absolute()

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
exec gunicorn {self.config['project_name']}.wsgi:application \\
    --bind 0.0.0.0:8000 \\
    --workers 4
"""
        start_sh = self.dir['server'] / 'start.sh'
        start_sh.touch(mode=0o766, exist_ok=True)
        start_sh.write_text(start_sh_content)

    def create_app_dirs(self):
        os.chdir(self.dir['server'])
        for app in self.config['django_apps']:
            app_root = self.dir['server'] / app['name']
            if not app_root.exists():
                system(f'python manage.py startapp {app["name"]}')
                self.create_urls_py(app_root)
                self.create_templates_dir(app_root)
            else:
                print(f'App folder "{app_root.name}" already exists, skipping...')

    def create_react_app(self, cached=True):
        if not self.dir['web'].exists():
            self.dir['web'].mkdir()
        if cached:
            print('Using cached react boilerplate') 
            system(f'cp -a {self.dir["boilerplate_cache"] / "web"}/ {self.dir["web"]}/')
            os.chdir(self.dir['web'])
            system(f'npm install')
        else:
            print('Building react boilerplate from create-react-app')
            os.chdir(self.dir['conf'])
            system('docker build -t node-cra -f create-react-dockerfile .')
            system(f'docker run --rm -t -v {self.dir["web"]}:/cra node-cra ')
            system(f'docker rmi node-cra')

    def create_django_project(self):
        os.chdir(self.dir['src'])
        system(f'django-admin startproject {self.config["project_name"]}')
        system(f'cp {self.dir["root"] / "requirements.txt"} {self.dir["server"]}')
        self.create_app_dirs()

    def eject_react_app(self):
        os.chdir(self.dir['web'])
        system('npm run eject')

    def copy_docker_files(self):
        system(f'cp {self.dir["dockerconf"] / "Dockerfile-web"} {self.dir["web"] / "Dockerfile"}')
        system(f'cp {self.dir["dockerconf"] / "Dockerfile-server"} {self.dir["server"] / "Dockerfile"}')
        for file_type in ('', '.override', '.production'):
            print(f'====> copying docker-compose{file_type}.yml')
            compose_file = (self.dir['dockerconf'] / f'docker-compose{file_type}.yml')
            content = compose_file.open().read()
            context = FileFormatter({
                'SERVER': f'./{self.dir["server"].relative_to(self.dir["src"])}',
                'WEB': f'./{self.dir["web"].relative_to(self.dir["src"])}',
                'PROJECT_NAME': self.config['project_name']
            })
            content = content.format(**{'conf': context})
            target_file = self.dir['src'] / compose_file.name
            target_file.touch()
            target_file.write_text(content)

    def rollback(self):
        print('Rolling back changes...')
        self.dir['src'].unlink()

    def copy_confs(self):
        system(f'cp -a {self.dir["conf"]} {self.dir["src"]}')

    def run(self):
        try:
            self.create_django_project()
            self.create_startup_scripts()
            self.create_react_app()
            self.copy_docker_files()
            self.copy_confs()
            # self.eject_react_app()
        except Exception:
            print('Error occured!')
            if self.should_rollback:
                self.rollback()
            raise
        return

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print(f'Usage: python {sys.argv[0]} <target folder>')
    #     exit(1)
    ps = ProjectStarter(rollback=False)
    ps.run()
    print ('\n' * 3, 'Success!', '\n' * 4)