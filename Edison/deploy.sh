#! /bin/bash

cp start-script.sh /etc/init.d/
cd /etc/init.d/
chmod +x start-script.sh
update-rc.d start-script.sh defaults
