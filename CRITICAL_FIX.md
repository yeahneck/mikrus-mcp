# 🚨 KRYTYCZNA NAPRAWA - Uruchom TERAZ!

## ⚡ Co jest nie tak?

1. ❌ **Zły port:** Serwer działa na 30121 zamiast 40231
2. ❌ **SSE nie działa:** Błąd "Cannot set headers after they are sent"

## ✅ NAPRAW TO (2 minuty):

### 🔧 Na Mikrusie uruchom:

```bash
ssh root@srv47.mikr.us -p 10121
```

Potem:
```bash
cd /opt/mikrus-mcp-server
git checkout production
git pull origin production
npm run build
pm2 delete mikrus-mcp-server
PORT=40231 HOST='::' NODE_ENV=production pm2 start dist/server.js --name mikrus-mcp-server
pm2 save
```

### ✅ Sprawdź czy działa:

```bash
pm2 logs mikrus-mcp-server --lines 10
curl http://localhost:40231/health
```

Powinno pokazać:
```
🚀 Mikrus MCP Server running on http://[::]:40231
📚 Documentation: 51 pages loaded
🔌 MCP endpoint: http://[::]:40231/sse
```

### 🌐 Test z zewnątrz:

```bash
curl https://srv47-40231.wykr.es/health
```

## 🎯 Co zostało naprawione:

✅ **Usunięto ręczne ustawienie nagłówków** w `/sse` endpoint  
✅ **PM2 teraz używa zmiennych środowiskowych** (PORT=40231)  
✅ **SSE działa bez błędów**  

## 🔗 Poprawna konfiguracja dla użytkowników:

### Cursor IDE:
```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://srv47-40231.wykr.es/sse"
    }
  }
}
```

### Claude Desktop:
```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://srv47-40231.wykr.es/sse"
    }
  }
}
```

---

## ⏭️ Następnym razem użyj:

Skopiuj `UPDATE-SERVER.sh` na serwer:
```bash
chmod +x UPDATE-SERVER.sh
./UPDATE-SERVER.sh
```

To automatycznie:
- Pobierze najnowszy kod
- Zbuduje projekt
- Zrestartuje z właściwymi ustawieniami

---

**🎉 Po tych krokach serwer będzie działał poprawnie!**
