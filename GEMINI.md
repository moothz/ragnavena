# Gemini Context & Instructions for "Ragnavena"

**System Date:** 2026-01-05
**Project Root:** `/home/moothz/ragnavena`
**Project website:** https://ragnavena.moothz.win (Cloudflared tunneled to ragnavena-web service port)

## 1. Project Overview
This is a **Ragnarok Online Private Server** (Pre-Renewal, Ep 13.1) utilizing:
- **Server:** rAthena (Git clone) running on Linux.
- **Client:** roBrowser Legacy (Web-based client).
- **Middleware:** Node.js WebSocket Proxy (bridges Browser WS -> Server TCP). Has bem modified to overcome issues with encryption and character case
- **Remote-client:** Serves game files remotely, in domain ragnaveno.moothz.win

## 2. Critical Constraints (DO NOT CHANGE WITHOUT APPROVAL)
*   **Packet Version:** `20120410`. This is hardcoded in `rAthena/src/config/packets.hpp` and `robrowser-web/client/dist/index.html`. Changing this usually breaks the client connection.
*   **Packet Obfuscation:** **DISABLED**. roBrowser requires plain packets.
*   **Port Shift:** All standard ports are shifted by **+20000**.
    *   Login: `26900`
    *   Char: `26121`
    *   Map: `25121`
    *   Proxy: `25999`
    *   Web: `28000`
*   **Inter-Server Auth:** The account `s1` (ID: 1) uses the **plaintext** password `p1`. Do NOT hash this in the database or change it to something complex without verifying `inter_athena.conf` compatibility.
*   **Proxy Logic:** The proxy (`robrowser-proxy/proxy.js`) has custom logic to parse ports from the URL path (e.g., `/IP:Port`) to support roBrowser's connection method. Do not revert to standard query-param only logic.
- **Remote Client Logic**: in folder roBrowserLegacy-RemoteClient-JS (npm start) and as service ragnavena-remote-client

## 3. File Structure & Configuration Map

| Component | Directory | Key Config Files |
| :--- | :--- | :--- |
| **Game Server** | `./rAthena` | `conf/import/login_conf.txt` (Ports, Logs)<br>`conf/import/char_conf.txt` (Ports, New Char)<br>`conf/import/map_conf.txt` (Ports)<br>`conf/import/inter_conf.txt` (DB Creds)<br>`src/config/packets.hpp` (Version)<br>`src/config/renewal.hpp` (Pre-RE toggle) |
| **Web Client** | `./robrowser-web/client` | `dist/index.html` (Client Config, IP, Proxy URL) |
| **Proxy** | `./robrowser-proxy` | `proxy.js` (Port forwarding logic) |
| **Systemd** | `/etc/systemd/system` | `ragnavena-game.service`<br>`ragnavena-web.service`<br>`ragnavena-proxy.service` |

Game files are stores in `roBrowserLegacy-RemoteClient-JS/data` folder and inside GRF files (`roBrowserLegacy-RemoteClient-JS/resources/`), all served by ragnavena-remote-client service.

**Search API**: You should search for files using this API (example to search for anything named sprite that ends with spr (regex):
```bash
curl -X POST http://localhost:3338/search -H "Content-Type: application/json" -d '{"filter": "sprite.*\\.spr"}'
```

## 4. Operational Commands

### Service Management
Restart services after config changes or recompilation may be necessary most of the time:
They are all systemd services (use systemctl restart)

- ragnavena-game
- ragnavena-web
- ragnavena-proxy
- ragnavena-remote-client

### Compilation
When modifying rAthena source (`.cpp`, `.hpp`):
```bash
cd rAthena
./configure --enable-prerenewal
make clean server
```

### Database
- **User:** `ragnarok`
- **Pass:** `BatataRagnavenaServerRoque`
- **DB:** `ragnavena`
```bash
mysql -u ragnarok -pBatataRagnavenaServerRoque ragnavena
```

## 5. Ragnarok Server Info
It serves as a lobby for players to meet, mainly.
The server has very few maps enabled: (rAthena/conf/maps_athena.conf)
- darkmall: Main lobby
- cell_game: PvP Room
- haunt_e: mob room
- Not yet in use: ghosthunter, desert, fishingboat, garden, storehouse, haunt_h

One NPC in the server does "everything":
- rAthena/npc/custom/ravena_info.txt

## 6. Troubleshooting
- **Logs:** Use `sudo journalctl -u ragnavena-xxxxxx -f` to watch server output (substitute for service name).
- **Debug Script:** `./debug.sh` gives a quick status snapshot.

## 6. Current Status (as of Jan 5, 2026)
- **Login:** Works (Admin account: `admin` / `admin`).
- **Char Creation:** Works.
- **Map Loading:** Works.
- **Access:** Configured for LAN/Cloudflare. `index.html` points to local IP or Cloudflare domain depending on user testing context.

## 7. Scripting Guidelines
- **Encoding:** Script files (e.g., .txt NPCs) MUST use **ISO-8859-1 (Latin-1)** encoding for special characters (accents, ç, etc.) to display correctly in the client. Do NOT use UTF-8 for these characters.
Make sure to convert the NPC and MOTD files if they are modified/created:
```bash
iconv -f UTF-8 -t ISO-8859-1 input_file.txt -o output_file.txt
```

## 8. Custom NPCs
To add custom NPCs properly:
1.  **Location:** Place the script file in `rAthena/npc/custom/` (e.g., `rAthena/npc/custom/my_npc.txt`).
2.  **Configuration:** Register the file in `rAthena/npc/scripts_custom.conf`.
    *   Add the line: `npc: npc/custom/my_npc.txt`
3.  **Encoding:** Ensure the file is encoded in **ISO-8859-1 (Latin-1)**.
4.  **Reload:** Restart the server or reload scripts (`@reloadscript` in-game if authorized, but restart is safer for config changes).