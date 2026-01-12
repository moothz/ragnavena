#!/bin/bash
echo "=== Ragnavena Status ==="
sudo systemctl status ragnavena-game --no-pager
echo "------------------------"
sudo systemctl status ragnavena-web --no-pager
echo "------------------------"
sudo systemctl status ragnavena-proxy --no-pager
echo "------------------------"
sudo systemctl status ragnavena-remote-client --no-pager
echo "========================"