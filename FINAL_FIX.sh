#!/bin/bash
# ⚡ OSTATECZNA NAPRAWA - Skopiuj i uruchom na Mikrusie

echo "🔄 Aktualizacja Mikrus MCP Server..."

# Przejdź do katalogu
cd /opt/mikrus-mcp-server || exit 1

# Pobierz najnowszy kod
echo "📥 Pobieranie najnowszego kodu..."
git checkout production
git pull origin production

# Zbuduj
echo "🏗️  Budowanie..."
npm run build

# Usuń stary proces
echo "🗑️  Usuwanie starego procesu..."
pm2 delete mikrus-mcp-server 2>/dev/null || true

# Uruchom z poprawnymi ustawieniami
echo "🚀 Uruchamianie serwera..."
PORT=40231 HOST='::' NODE_ENV=production pm2 start dist/server.js --name mikrus-mcp-server

# Zapisz konfigurację PM2
pm2 save

# Poczekaj na start
sleep 3

# Sprawdź status
echo ""
echo "✅ Sprawdzanie statusu..."
pm2 status

# Pokaż logi
echo ""
echo "📋 Ostatnie logi:"
pm2 logs mikrus-mcp-server --lines 15 --nostream

# Test health
echo ""
echo "🧪 Test połączenia:"
curl -s http://localhost:40231/health | python3 -m json.tool 2>/dev/null || curl http://localhost:40231/health

echo ""
echo "🎉 Gotowe! Serwer powinien działać na porcie 40231"
echo "🌐 Dostępny publicznie: https://srv47-40231.wykr.es"
