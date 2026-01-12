#!/bin/bash
echo "=== Ragnavena Restart ==="
sudo systemctl restart ragnavena-game
echo "------------------------"
sudo systemctl restart ragnavena-web
echo "------------------------"
sudo systemctl restart ragnavena-proxy
echo "------------------------"
sudo systemctl restart ragnavena-remote-client
echo "========================"
./debug.sh
