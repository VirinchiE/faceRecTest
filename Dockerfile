FROM python:3.9-buster
ENV PATH /usr/local/bin:$PATH

RUN apt-get update && apt-get -y install sudo
RUN apt-get install -y --no-install-recommends \
    gcc telnet cmake unzip git wget tar curl dpkg qtbase5-dev libgtk-3-dev ffmpeg libopenexr-dev libwebp-dev freeglut3-dev libdc1394-22-dev libboost-all-dev python3-pip tmux net-tools\
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m admin && echo "admin:admin" | chpasswd && adduser admin sudo
RUN echo "%admin ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER admin
RUN chmod -R 775 /home/admin
WORKDIR /home/admin/
RUN sudo ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime

RUN mkdir attendance-app
COPY ./ ./attendance-app

RUN pip install -r /home/admin/attendance-app/requirements.txt
RUN pip install cmake
RUN pip install dlib==19.24.0
RUN rm -rf /home/admin/.cache

WORKDIR /home/admin/attendance-app/

RUN sudo mkdir -p /home/admin/attendance-app/Logs/ /home/admin/attendance-app/known_faces/
RUN sudo chmod -R 777 /home/admin/attendance-app/Logs/ /home/admin/attendance-app/known_faces/
RUN sudo chmod -R 777 /home/admin/attendance-app/known_faces/
RUN sudo chmod 777 /home/admin/attendance-app/startup.sh

EXPOSE 8045
ENTRYPOINT ["/home/admin/attendance-app/startup.sh"]
