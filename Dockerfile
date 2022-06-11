FROM dudekw/siu-base

ARG BOARD_FILENAME
COPY ./board/${BOARD_FILENAME} /roads.png

WORKDIR /root
COPY ./routes/* ./routes/
COPY ./source/* ./source/

RUN ["/bin/bash", "-c", "apt install python3-pip -y"]
RUN ["/bin/bash", "-c", "pip3 install --upgrade pip"]
RUN ["/bin/bash", "-c", "pip3 install tensorflow"]
