#!/bin/bash

# run websocket chat server in the background
python3 Programs/chat_websocket_server.py &

# Run Apache in the foreground to keep container alive
apache2ctl start
tail -f /dev/null
