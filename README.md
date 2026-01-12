# Ragnavena - Ragnarok Online Private Server Project

This repository serves as the main orchestration root for the Ragnavena project. It manages the configuration, tools, and sub-services required to run the server and web client.

## Project Structure

This project uses Git Submodules for the core components to allow for easy upstream updates while maintaining custom configurations.

*   **`rAthena/`** (Submodule): The core Ragnarok Online server (Map, Char, Login).
*   **`robrowser-web/`** (Submodule): The web-based client interface (HTML/JS/CSS).
*   **`robrowser-proxy/`** (Submodule): A WebSocket proxy bridging the web client and the TCP game server.
*   **`roBrowserLegacy-RemoteClient-JS/`** (Submodule): Remote client resource server.

### Configuration & Customization

*   **`config-files/`**: Contains the "source of truth" for all custom configurations.
    *   `rathena/`: Custom rAthena confs (`login_conf.txt`, `inter_conf.txt`, etc.) and NPCs.
    *   `robrowser/`: Custom configurations for the web client and proxy.
    *   `systemd/`: Service files for managing the application processes.
*   **`tools/`**: Helper scripts for maintenance.
    *   `setup_links.sh`: **CRITICAL**. Run this to symlink files from `config-files/` to their active locations in the submodules.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone --recursive <repo-url>
    cd ragnavena
    ```

2.  **Initialize Links:**
    Apply the custom configurations to the submodules.
    ```bash
    ./tools/setup_links.sh
    ```

3.  **Build rAthena:**
    ```bash
    cd rAthena
    ./configure --enable-prerenewal
    make clean server
    cd ..
    ```

4.  **Install Proxy Dependencies:**
    ```bash
    cd robrowser-proxy
    npm install
    cd ..
    ```

## Daily Operations

*   **Restart Services:** Use `systemctl restart ragnavena-<service>` (requires sudo).
*   **Logs:** Check `journalctl -u ragnavena-game -f`.

## Directory Cleanup
Old/Unused files have been moved to `old/`.
Scripts were moved to `tools/`.
