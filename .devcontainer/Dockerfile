FROM fluxrm/flux-sched:focal

LABEL maintainer="Vanessasaurus <@vsoch>"

# Match the default user id for a single system so we aren't root
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000
ENV USERNAME=${USERNAME}
ENV USER_UID=${USER_UID}
ENV USER_GID=${USER_GID}

USER root
RUN apt-get update
COPY .github/requirements-dev.txt /dev-requirements.txt
# For easier Python development.
RUN python3 -m pip install IPython && \
    python3 -m pip install -r /dev-requirements.txt

# Assuming installing to /usr/local
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV PATH=/home/vscode/.local/bin:$PATH

# Add the group and user that match our ids
RUN groupadd -g ${USER_GID} ${USERNAME} && \
    adduser --disabled-password --uid ${USER_UID} --gid ${USER_GID} --gecos "" ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers
USER $USERNAME
