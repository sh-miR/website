FROM centos

RUN rpm -Uhv http://ftp.pbone.net/pub/fedora/epel/7/x86_64/e/epel-release-7-2.noarch.rpm
RUN yum install -y python-pip python-devel postgresql-devel gcc

ADD . /opt/shmir-website

RUN pip install -r /opt/shmir-website/requirements.txt

WORKDIR /opt/shmir-website/shweb

#RUN python manage.py syncdb --noinput
RUN python manage.py collectstatic --noinput
