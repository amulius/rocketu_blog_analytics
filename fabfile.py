from fabric.colors import green, red, yellow, cyan
from fabric.contrib.files import upload_template
from fabric.decorators import task
from fabric.operations import local
from fabric.api import *

env.hosts = ['54.191.121.196']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/blog_analytics.pem'
env.shell = "/bin/bash -l -i -c"


def restart_app():
    sudo("service supervisor restart")
    sudo("service nginx restart")

# @task
# def hello():
#     print(green("I'm alive!"))
#
#
# def test():
#     print(red("I should not work"))
#
#
# @task
# def create_file(file_name):
#     local("touch ~/Desktop/{}.txt".format(file_name))
#
#
# @task
# def create_dir(dir_name):
#     local("mkdir ~/Desktop/{}".format(dir_name))
#
#
# @task
# def create_special_dir(location, dir_name):
#     local("mkdir ~/{}/{}".format(location, dir_name))


@task
def ubuntu_hello():
    with hide("stdout"):
        output = run("lsb_release -a")
        print(yellow(output))


# @task
# def deploy():
#     with prefix("workon blog_analytics"):
#         with cd("/home/ubuntu/rocketu_blog_analytics"):
#             with hide("stdout"):
#                 output = run("git pull origin master")
#                 print(cyan(output))
#                 output = run("pip install -r requirements.txt")
#                 print(cyan(output))


@task
def deploy():
    with prefix("workon blog_analytics"):
        with cd("/home/ubuntu/rocketu_blog_analytics"):
            run("git pull origin master")
            run("pip install -r requirements.txt")
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")

    restart_app()


@task
def setup_postgres(database_name, password):
    sudo("adduser {}".format(database_name))
    sudo("apt-get install postgresql postgresql-contrib libpq-dev")

    with settings(sudo_user='postgres'):
        sudo("createuser {}".format(database_name))
        sudo("createdb {}".format(database_name))
        alter_user_statement = "ALTER USER {} WITH PASSWORD '{}';".format(database_name, password)
        sudo('psql -c "{}"'.format(alter_user_statement))


@task
def setup_nginx(project_name, server_name):
    upload_template("./deploy/nginx.conf",
                    "/etc/nginx/sites-enabled/{}.conf".format(project_name),
                    {'server_name': server_name},
                    use_sudo=True,
                    backup=False)

    restart_app()


@task
def setup_supervisor(project_name, vir_env):
    upload_template("./deploy/supervisor.conf",
                    "/etc/supervisor/conf.d/{}.conf".format(project_name),
                    {'project_name': project_name,
                     'vir_env': vir_env},
                    use_sudo=True,
                    backup=False)

    restart_app()


@task
def setup_gunicorn(project_name):
    upload_template("./deploy/gunicorn.conf",
                    "~/{}/gunicorn.conf.py".format(project_name),
                    {'project_name': project_name},
                    use_sudo=True,
                    backup=False)

    restart_app()