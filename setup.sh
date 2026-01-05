#!/usr/bin/env bash
set -euo pipefail

# setup.sh - helper to install Chromedriver on Debian/Ubuntu and place it in /usr/local/bin
# Usage: sudo ./setup.sh   (script uses sudo where needed)

DEST=/usr/local/bin/chromedriver
TMP_ZIP=/tmp/chromedriver_linux64.zip

echo "==> Installing prerequisites (wget, curl, unzip)"
if command -v apt >/dev/null 2>&1; then
  sudo apt update
  sudo apt install -y wget curl unzip ca-certificates
else
  echo "Non-Debian system detected. Please ensure wget/curl/unzip are installed and run the script manually."
fi

# helper to install packaged chromium + chromedriver (quick fallback)
install_packaged_chromium() {
  echo "Attempting to install packaged chromium and chromedriver (may be out-of-date)..."
  sudo apt install -y chromium-browser chromium-chromedriver || {
    echo "Failed to install packaged chromium packages. You can install Chrome manually and re-run this script.";
    exit 1
  }
  echo "Packaged Chromium + Chromedriver installed. Chromedriver should be available on PATH." 
  exit 0
}

# Detect browser
if command -v google-chrome >/dev/null 2>&1; then
  CHROME_CMD=google-chrome
elif command -v google-chrome-stable >/dev/null 2>&1; then
  CHROME_CMD=google-chrome-stable
elif command -v chromium-browser >/dev/null 2>&1; then
  CHROME_CMD=chromium-browser
elif command -v chromium >/dev/null 2>&1; then
  CHROME_CMD=chromium
else
  echo "No Google Chrome or Chromium binary found."
  read -p "Install packaged Chromium and chromedriver via apt? [y/N]: " yn
  yn=${yn:-N}
  if [[ "$yn" =~ ^[Yy]$ ]]; then
    install_packaged_chromium
  else
    echo "Please install Chrome/Chromium and re-run this script. Exiting."; exit 1
  fi
fi

if [[ "$CHROME_CMD" == "chromium" || "$CHROME_CMD" == "chromium-browser" ]]; then
  echo "Chromium detected: $CHROME_CMD"
  echo "Trying to install a compatible chromedriver via packaged chromedriver if available."
  # If system provides chromedriver package, use it
  if dpkg -s chromium-chromedriver >/dev/null 2>&1; then
    echo "chromium-chromedriver package already installed. Exiting."
    exit 0
  fi
  echo "Installing packaged chromium-chromedriver..."
  sudo apt install -y chromium-chromedriver || {
    echo "Could not install packaged chromedriver. You may need to download a matching chromedriver manually."; exit 1
  }
  echo "Installed chromium-chromedriver package. Exiting."
  exit 0
fi

# At this point we have Google Chrome available (or Chromium variant covered above)
echo "Using browser: $CHROME_CMD"

# Get Chrome major version
CHROME_VERSION_RAW=$($CHROME_CMD --version 2>/dev/null || true)
if [[ -z "$CHROME_VERSION_RAW" ]]; then
  echo "Unable to get browser version from $CHROME_CMD"; exit 1
fi
CHROME_VERSION=$(echo "$CHROME_VERSION_RAW" | awk '{print $NF}')
CHROME_MAJOR=$(echo "$CHROME_VERSION" | cut -d. -f1)

if [[ -z "$CHROME_MAJOR" ]]; then
  echo "Could not determine Chrome major version. Version string: $CHROME_VERSION_RAW"; exit 1
fi

echo "Detected Chrome version: $CHROME_VERSION (major: $CHROME_MAJOR)"

# Find matching chromedriver
echo "Querying ChromeDriver releases for major version $CHROME_MAJOR..."
LATEST_RELEASE_URL="https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR}"
LATEST_VERSION=$(curl -fsSL "$LATEST_RELEASE_URL" || true)
if [[ -z "$LATEST_VERSION" ]]; then
  echo "Failed to fetch latest chromedriver version for $CHROME_MAJOR. Falling back to latest overall release."
  LATEST_VERSION=$(curl -fsSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
fi

if [[ -z "$LATEST_VERSION" ]]; then
  echo "Unable to determine a chromedriver release to download. Exiting."; exit 1
fi

DL_URL="https://chromedriver.storage.googleapis.com/${LATEST_VERSION}/chromedriver_linux64.zip"

echo "Downloading Chromedriver $LATEST_VERSION from $DL_URL"
wget -q -O "$TMP_ZIP" "$DL_URL" || { echo "Download failed"; exit 1; }

unzip -o "$TMP_ZIP" -d /tmp || { echo "Unzip failed"; exit 1; }

sudo mv -f /tmp/chromedriver "$DEST"
sudo chmod +x "$DEST"

echo "Chromedriver installed to $DEST"

# Optionally export CHROMEDRIVER_PATH in user's profile
PROFILE_FILE="$HOME/.profile"
EXPORT_LINE="export CHROMEDRIVER_PATH=$DEST"
if grep -qxF "$EXPORT_LINE" "$PROFILE_FILE" 2>/dev/null; then
  echo "CHROMEDRIVER_PATH already set in $PROFILE_FILE"
else
  echo "Adding CHROMEDRIVER_PATH to $PROFILE_FILE"
  echo "\n# Chromedriver path for movieScraper" >> "$PROFILE_FILE"
  echo "$EXPORT_LINE" >> "$PROFILE_FILE"
  echo "Added. Run: source $PROFILE_FILE or open a new shell to pick up the variable." 
fi

# cleanup
rm -f "$TMP_ZIP"

echo "Done. You can verify with:"
echo "  $DEST --version || which chromedriver && chromedriver --version"

echo "If you plan to run the scraper now in this session, export the var in the current shell with:"
echo "  export CHROMEDRIVER_PATH=$DEST"

echo "Setup complete."
