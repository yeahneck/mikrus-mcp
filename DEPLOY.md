# 🚀 Deployment na Mikrus

## 📋 Wymagania

- Mikrus VPS (2.0+)
- Node.js 18+
- PM2
- Git

## 🔧 Pierwsza instalacja

### 1. Zaloguj się na Mikrus

```bash
ssh root@srvXX.mikr.us -p 10XXX
```

### 2. Zainstaluj zależności

```bash
# Node.js (jeśli nie ma)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# PM2
npm install -g pm2

# Git
apt install -y git
```

### 3. Sklonuj repozytorium (branch production)

```bash
cd /opt
git clone -b production https://github.com/yeahneck/mikrus-mcp-server.git
cd mikrus-mcp-server
```

### 4. Zainstaluj pakiety

```bash
npm install
```

### 5. Skonfiguruj środowisko

```bash
cp .env.example .env
nano .env
```

Ustaw:
```env
PORT=40231
HOST=::
NODE_ENV=production
DOCS_UPDATE_INTERVAL=3600000
```

### 6. Zbuduj projekt

```bash
npm run build
```

### 7. Uruchom z PM2

```bash
PORT=40231 HOST='::' NODE_ENV=production pm2 start dist/server.js --name mikrus-mcp-server
pm2 save
pm2 startup
```

### 8. Sprawdź status

```bash
pm2 status
pm2 logs mikrus-mcp-server
curl http://localhost:40231/health
```

## 🔄 Aktualizacja

Skopiuj `UPDATE-SERVER.sh` na serwer i uruchom:

```bash
chmod +x UPDATE-SERVER.sh
./UPDATE-SERVER.sh
```

## 🌐 Dostęp publiczny

### Przez domenę (zalecane)

Skonfiguruj domenę wskazującą na:
- **Serwer:** `srvXX.mikr.us`
- **Port:** `40231`

Lub użyj darmowej subdomeny Mikrusa:
```bash
# Domyślnie dostępne pod:
srvXX-40231.wykr.es
```

### Testowanie

```bash
curl https://twoja-domena.pl/health
```

## 👥 Konfiguracja dla użytkowników

### Cursor IDE

Użytkownicy dodają do `settings.json`:

```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://twoja-domena.pl/sse"
    }
  }
}
```

### Claude Desktop

W `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://twoja-domena.pl/sse"
    }
  }
}
```

## 🔒 Bezpieczeństwo

### Rate Limiting

Serwer ma wbudowany rate limiting:
- 100 requestów / 15 minut na IP
- Endpointy MCP są wyłączone z limitu

### Opcjonalnie: Nginx reverse proxy

```nginx
server {
    listen [::]:80;
    server_name twoja-domena.pl;
    
    location / {
        proxy_pass http://localhost:40231;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        # SSE wymagania
        proxy_buffering off;
        proxy_read_timeout 86400s;
    }
}
```

## 📊 Monitoring

```bash
# Status PM2
pm2 status

# Logi real-time
pm2 logs mikrus-mcp-server

# Restart
pm2 restart mikrus-mcp-server

# Stop
pm2 stop mikrus-mcp-server

# Info
pm2 info mikrus-mcp-server
```

## 🐛 Troubleshooting

### Serwer nie startuje

```bash
# Sprawdź logi
pm2 logs mikrus-mcp-server --err

# Sprawdź port
netstat -tulpn | grep 40231
```

### Dokumentacja nie ładuje się

```bash
# Sprawdź czy katalog ~/docs istnieje
ls -la ~/docs

# Ręczna aktualizacja
cd /opt/mikrus-mcp-server
npm run update-docs
```

### Połączenie timeout

- Sprawdź firewall na Mikrusie
- Upewnij się że port 40231 jest otwarty
- Sprawdź czy domena wskazuje na poprawny serwer

## 📝 Notatki

- Port **40231** to przykład - możesz użyć dowolnego dostępnego portu
- Serwer używa IPv6 (`HOST='::'`)
- Dokumentacja aktualizuje się automatycznie co godzinę
- PM2 automatycznie restartuje serwer po crashu
