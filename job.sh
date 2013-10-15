#!/bin/bash
cd /home/aseba/AsanaSM; ./asm.py | /usr/local/bin/markdown_py | /usr/bin/mail developers@olapic.com -a "Content-type: text/html;" -s "Asana Tasks On $(date +'%d-%m-%Y %H:%M')"
