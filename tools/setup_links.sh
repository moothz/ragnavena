#!/bin/bash

# setup_links.sh
# Links custom configuration files from config-files/ to their respective locations.

ROOT_DIR=$(pwd)
CONFIG_DIR="$ROOT_DIR/config-files"

# Function to safely link a file
link_file() {
    local source="$1"
    local target="$2"

    if [ -f "$target" ] && [ ! -L "$target" ]; then
        echo "Backing up $target to $target.bak"
        mv "$target" "$target.bak"
    fi

    if [ -L "$target" ]; then
        echo "Updating link for $target"
        rm "$target"
    fi

    echo "Linking $source -> $target"
    ln -s "$source" "$target"
}

# --- rAthena ---
echo "--- Configuring rAthena ---"
# Conf
link_file "$CONFIG_DIR/rathena/conf/import/char_conf.txt" "rAthena/conf/import/char_conf.txt"
link_file "$CONFIG_DIR/rathena/conf/import/map_conf.txt" "rAthena/conf/import/map_conf.txt"
link_file "$CONFIG_DIR/rathena/conf/import/inter_conf.txt" "rAthena/conf/import/inter_conf.txt"
link_file "$CONFIG_DIR/rathena/conf/import/login_conf.txt" "rAthena/conf/import/login_conf.txt"

# Maps config (Handle .bak if it exists in source)
if [ -f "$CONFIG_DIR/rathena/conf/maps_athena.conf.bak" ]; then
    link_file "$CONFIG_DIR/rathena/conf/maps_athena.conf.bak" "rAthena/conf/maps_athena.conf"
elif [ -f "$CONFIG_DIR/rathena/conf/maps_athena.conf" ]; then
    link_file "$CONFIG_DIR/rathena/conf/maps_athena.conf" "rAthena/conf/maps_athena.conf"
fi

# SRC Config
link_file "$CONFIG_DIR/rathena/src/config/packets.hpp" "rAthena/src/config/packets.hpp"
link_file "$CONFIG_DIR/rathena/src/config/renewal.hpp" "rAthena/src/config/renewal.hpp"

# Custom NPCs
echo "--- Linking Custom NPCs ---"
for npc in "$CONFIG_DIR/rathena/npc/custom/"*.txt; do
    [ -e "$npc" ] || continue
    filename=$(basename "$npc")
    link_file "$npc" "rAthena/npc/custom/$filename"
done

# --- roBrowser Proxy ---
echo "--- Configuring roBrowser Proxy ---"
link_file "$CONFIG_DIR/robrowser/proxy.js" "robrowser-proxy/proxy.js"

# --- roBrowser Web ---
echo "--- Configuring roBrowser Web ---"
link_file "$CONFIG_DIR/robrowser/index.html" "robrowser-web/dist/index.html"

echo "Done. Remember to rebuild rAthena if you changed src files."
