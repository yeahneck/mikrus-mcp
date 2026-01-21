# 🚨 SZYBKA NAPRAWA - Aktualizuj Serwer na Mikrusie

## ⚡ Problem
Serwer ma błędy TypeScript i nie kompiluje się.

## ✅ Rozwiązanie (1 minuta)

### Zaloguj się na Mikrus:
```bash
ssh root@srv47.mikr.us -p 10121
```

### Uruchom aktualizację:
```bash
cd /opt/mikrus-mcp-server
git checkout production
git pull origin production
npm run build
pm2 delete mikrus-mcp-server
PORT=40231 HOST='::' NODE_ENV=production pm2 start dist/server.js --name mikrus-mcp-server
pm2 save
```

**LUB użyj skryptu:**
```bash
./UPDATE-SERVER.sh
```

### Sprawdź czy działa:
```bash
pm2 status
pm2 logs mikrus-mcp-server --lines 20
curl http://localhost:40231/health
```

Powinno pokazać:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  ...
}
```

## 🧪 Testuj połączenie

Z lokalnego komputera:
```bash
curl https://srv47-40231.wykr.es/health
```

## 🔗 Konfiguracja dla użytkowników

### Cursor IDE (`settings.json`):
```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://srv47-40231.wykr.es/sse"
    }
  }
}
```

### Claude Desktop (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://srv47-40231.wykr.es/sse"
    }
  }
}
```

## ⚠️ Ważne

- URL to `https://srv47-40231.wykr.es/sse` (NIE `.../mcp`)
- Używaj HTTPS, nie HTTP
- Port 40231 musi być otwarty
- Sprawdź czy nginx/firewall nie blokuje

## 🐛 Troubleshooting

### 404 Not Found
```bash
# Sprawdź czy endpoint istnieje
curl https://srv47-40231.wykr.es/

# Powinno zwrócić info o endpointach
```

### Connection refused
```bash
# Sprawdź czy serwer działa
pm2 status

# Sprawdź logi
pm2 logs mikrus-mcp-server
```

### Serwer restartuje się non-stop
```bash
# Zobacz pełne logi błędów
pm2 logs mikrus-mcp-server --err --lines 50
```

## ✨ Co zostało naprawione

- ✅ Usunięto błędy TypeScript (niewykorzystane zmienne)
- ✅ Dodano właściwe typy zwracane przez funkcje
- ✅ Naprawiono wszystkie ścieżki kodu
- ✅ Kompilacja przechodzi bez błędów

## 📊 Sprawdź dostępne endpointy

```bash
curl https://srv47-40231.wykr.es/
```

Powinno pokazać:
- `/health` - status serwera
- `/stats` - statystyki dokumentacji
- `/search` - wyszukiwanie
- `/docs` - lista wszystkich dokumentów
- `/sse` - endpoint MCP (dla AI)
- `/message` - endpoint MCP POST

---

**Potrzebujesz pomocy?** Zobacz pełną dokumentację w `DEPLOY.md`
