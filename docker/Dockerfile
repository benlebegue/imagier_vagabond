FROM python:2-jessie

# Install packages for creating a sudo-enabled user
RUN apt-get update && apt-get install -y sudo mysql-client

# Create user 'site'
# uid and gid should match user in host
RUN addgroup site --gid=513 && \
    adduser site --system --uid=65814 --gid=513 --home=/home/site --shell=/bin/bash

# Make site a privileged user
RUN usermod site --append --groups=adm,sudo && echo site:ok | chpasswd

# Switch to user
USER site

WORKDIR /home/site
RUN virtualenv venv
RUN echo "source /home/site/venv/bin/activate" > .bashrc

# We need to run a command, or the container shuts down
CMD [ "/bin/bash" ]
