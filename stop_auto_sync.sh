#!/bin/bash

# Find the process ID of the auto_sync.sh script
PID=$(ps aux | grep '[a]uto_sync.sh' | awk '{print $2}')

# Check if the process is running
if [ -z "$PID" ]; then
    echo "No auto_sync.sh script is currently running."
else
    # Kill the process
    kill $PID
    echo "Stopped the auto_sync.sh script with PID $PID."
fi
