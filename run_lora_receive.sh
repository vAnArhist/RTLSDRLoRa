#!/bin/sh

DIR="$( cd "$( dirname "$0" )" && pwd )"

docker run -it --rm --privileged \
--net=host \
-v $DIR/lora_receive_nogui.py:/apps/lora_receive_nogui.py \
-v /dev/bus/usb:/dev/bus/usb \
--entrypoint /bin/bash rpp0/gr-lora:latest \
-c "chmod u+x /apps/lora_receive_nogui.py && /apps/lora_receive_nogui.py"
