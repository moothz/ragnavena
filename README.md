# Ragnavena - Projeto do Servidor de Ragnarok Online

Código fonte e configurações que rodam o servidor de RO (apenas um lobby/gather com mapas custom) da **ravenabot** ([site](https://ravena.moothz.win), [github](https://github.com/moothz/ravena-ai)).

Publiquei ele a pedidos dos membros que se interessaram em como foi feito - não é um repositório 'ready to use', mas sim para ser usado como consulta para quem busca fazer algo semelhante.

## Estrutura do Projeto

Este projeto utiliza Submódulos Git para os componentes principais para permitir atualizações fáceis do upstream enquanto mantém as configurações customizadas.

*   **`rAthena/`**: O servidor core do Ragnarok Online (Map, Char, Login)
*   **`robrowser-web/`**: Client web para RO (HTML/JS/CSS)
*   **`roBrowserLegacy-RemoteClient-JS/`**: Servidor de recursos (data/grf) do cliente remoto
*   **`robrowser-proxy/`**: Um proxy WebSocket que liga o cliente web ao servidor TCP do jogo *(desenvolvido com gemini-cli)*

### Configuração & Customização

*   **`config-files/`**: Configurações do servidor
    *   `rathena/`: Configurações customizadas do rAthena (`login_conf.txt`, `inter_conf.txt`, etc) e NPCs
    *   `robrowser/`: Configurações do robrowser e proxy
*   **`tools/`**: Scripts auxiliares para manutenção
    *   `setup_links.sh`: **CRÍTICO**. Script que cria os links simbólicos (symlinks) dos arquivos em `config-files/` para o local correto nos submódulos