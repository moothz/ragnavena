# Ragnavena Server Setup

**Project:** Ragnavena
**Type:** Ragnarok Online Private Server (Pre-Renewal, Episode 13.1)
**Stack:** rAthena + roBrowser Legacy + Node.js WebSocket Proxy

## 1. Services & Architecture

The system runs on 3 primary systemd services:

| Service Name | Description | Port | Path |
| :--- | :--- | :--- | :--- |
| **ragnavena-game** | rAthena Game Server (Login/Char/Map) | 26900, 26121, 25121 | `/home/moothz/ragnavena/rAthena` |
| **ragnavena-web** | Python HTTP Server (roBrowser Web Client) | 28000 | `/home/moothz/ragnavena/robrowser-web/client` |
| **ragnavena-proxy**| Node.js WebSocket -> TCP Bridge | 25999 | `/home/moothz/ragnavena/robrowser-proxy` |

## 2. Ports Configuration

We have shifted all standard RO ports by +20000.

| Server Component | Standard Port | **Ragnavena Port** |
| :--- | :--- | :--- |
| **Login Server** | 6900 | **26900** |
| **Char Server** | 6121 | **26121** |
| **Map Server** | 5121 | **25121** |
| **Web Client** | 8000 | **28000** |
| **WS Proxy** | 5999 | **25999** |

## 3. Database

- **Engine:** MariaDB
- **Database:** `ragnavena`
- **User:** `ragnarok`
- **Password:** `BatataRagnavenaServerRoque`

### Important Accounts
- **Inter-Server Communication:**
  - User: `s1`
  - Pass: `p1` (Plaintext)
  - ID: `1`
  - *Note: Critical for Char<->Login communication.*

- **Admin / Player Account:**
  - User: `admin`
  - Pass: `admin` (Plaintext)
  - ID: `2000000`

## 4. Configuration Files

This folder (`config-files/`) contains backups of all modified files.

### rAthena (Game Server)
- **Login Config:** `rathena/conf/import/login_conf.txt`
  - *Setting ports, disabling MD5 packet check, allowing new accounts.*
- **Char Config:** `rathena/conf/import/char_conf.txt`
  - *Setting ports, disabling pincode.*
- **Map Config:** `rathena/conf/import/map_conf.txt`
  - *Setting ports.*
- **Inter Config:** `rathena/conf/import/inter_conf.txt`
  - *Database credentials.*
- **Packet Version:** `rathena/src/config/packets.hpp`
  - *PACKETVER set to 20120410. Obfuscation Disabled.*
- **Renewal Mode:** `rathena/src/config/renewal.hpp`
  - *PRERE defined (Pre-Renewal).*

**Original Path:** `/home/moothz/ragnavena/rAthena/...`

### roBrowser (Web Client)
- **Client Config:** `robrowser/index.html`
  - *Configures connection IP, ports, packetver (20120410), remote client (grf.robrowser.com) and socket proxy.*
- **Location:** `/home/moothz/ragnavena/robrowser-web/client/dist/index.html`

### WebSocket Proxy
- **Script:** `robrowser/proxy.js`
  - *Node.js script that bridges WebSocket (Browser) to TCP (Game Server). Handles path-based routing (e.g., /IP:Port).*
- **Location:** `/home/moothz/ragnavena/robrowser-proxy/proxy.js`

### Systemd Services
- **Files:** `systemd/*.service`
- **Location:** `/etc/systemd/system/`

## 5. Access

- **Web Client:** https://ragnavena.moothz.win (Forwarded to localhost:28000)
- **WebSocket:** wss://wsrag.moothz.win (Forwarded to localhost:25999)
- **Local LAN:** http://192.168.3.10:28000 (Configured to use ws://192.168.3.10:25999)

## 6. How to Run/Debug

**Check Status:**
```bash
./debug.sh
# OR
sudo systemctl status ragnavena-game
sudo systemctl status ragnavena-web
sudo systemctl status ragnavena-proxy
```

**Restart Services:**
```bash
sudo systemctl restart ragnavena-game ragnavena-web ragnavena-proxy
```

**Logs:**
```bash
sudo journalctl -u ragnavena-game -f
sudo journalctl -u ragnavena-proxy -f
```
