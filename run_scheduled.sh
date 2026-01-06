#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/movieScraper.py"
CONFIG_FILE="$SCRIPT_DIR/config.py"
PID_FILE="/tmp/movieScraper.pid"

# Extract Telegram config from config.py
TELEGRAM_TOKEN=$(grep "telegram_token" "$CONFIG_FILE" | cut -d"'" -f2 | cut -d'"' -f2)
CHAT_ID=$(grep "chat_id" "$CONFIG_FILE" | cut -d"'" -f2 | cut -d'"' -f2)

# Function to send Telegram notification
send_notification() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}&text=${message}" > /dev/null
}

# Function to start the scraper
start_scraper() {
    echo "Starting movie scraper at $(date)"
    send_notification "🎬 Movie scraper started at $(date '+%H:%M')"
    
    python3 "$PYTHON_SCRIPT" &
    echo $! > "$PID_FILE"
}

# Function to stop the scraper
stop_scraper() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "Stopping movie scraper at $(date)"
            send_notification "🛑 Movie scraper stopped at $(date '+%H:%M')"
            kill "$PID"
            rm "$PID_FILE"
        fi
    fi
}

# Main loop
while true; do
    CURRENT_HOUR=$(date +%H)
    CURRENT_MIN=$(date +%M)
    
    # Check if it's between 7:30 AM (07:30) and 11:00 PM (23:00)
    CURRENT_TIME=$(printf "%02d%02d" "$CURRENT_HOUR" "$CURRENT_MIN")
    START_TIME="0730"
    END_TIME="2300"
    
    if [ "$CURRENT_TIME" -ge "$START_TIME" ] && [ "$CURRENT_TIME" -lt "$END_TIME" ]; then
        # Should be running
        if [ ! -f "$PID_FILE" ] || ! kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            start_scraper
        fi
    else
        # Should not be running
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            stop_scraper
        fi
    fi
    
    # Check every minute
    sleep 60
done
