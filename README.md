# Mikrus MCP Server

**Remote MCP server providing access to complete Mikrus documentation (51 pages) for AI assistants.**

[![Live Server](https://img.shields.io/badge/status-online-brightgreen.svg)](https://srv47-40231.wykr.es/health)
[![MCP Protocol](https://img.shields.io/badge/protocol-MCP-blue.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Server URL

```
https://srv47-40231.wykr.es/sse
```

## 🚀 Quick Start

### Cursor IDE

Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://srv47-40231.wykr.es/sse"
    }
  }
}
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "mikrus": {
      "url": "https://srv47-40231.wykr.es/sse"
    }
  }
}
```

### Test via CLI

```bash
npx -y mcp-remote https://srv47-40231.wykr.es/sse
```

## 📚 What's Available

The server provides access to **51 Mikrus documentation pages**, including:

- Server setup and configuration guides
- Nginx, Apache, PHP, MySQL tutorials
- Docker and PM2 guides
- SSH, VPN, and networking guides
- Troubleshooting and FAQ
- And much more!

## 🛠️ Available Tools

Once connected, the AI assistant can use these tools:

### `user-mikrus-search_mikrus_docs`
Search through documentation by keyword or phrase.

**Parameters:**
- `query` (required): Search term
- `limit` (optional): Max results (default: 10)

**Example:**
```
Search for "nginx" in Mikrus docs
```

### `user-mikrus-get_mikrus_stats`
Get statistics about the documentation server.

**Example:**
```
Show Mikrus documentation stats
```

### `user-mikrus-list_mikrus_topics`
List all available documentation topics/categories.

**Example:**
```
List all Mikrus topics
```

## ✅ Verify Server Status

Check if the server is running:

```bash
# Health check
curl https://srv47-40231.wykr.es/health

# Expected response:
# {"status":"healthy","version":"1.0.0","uptime":...,"docs":{"totalDocs":51,...}}
```

## 🎯 Use Cases

- **Ask questions** about Mikrus VPS setup and configuration
- **Search documentation** without leaving your IDE
- **Get instant answers** about common issues and troubleshooting
- **Learn** best practices for server administration

## 📖 Example Queries

Once connected, try asking your AI assistant:

```
- "How do I set up Nginx on Mikrus?"
- "Show me how to configure MySQL database"
- "What are the available Linux distributions?"
- "How do I connect to my Mikrus server via SSH?"
- "Explain how IPv6 works on Mikrus"
```

## 🔧 Technical Details

- **Protocol**: Model Context Protocol (MCP) via Server-Sent Events (SSE)
- **Transport**: HTTPS with automatic SSL/TLS
- **Documentation**: 51 pages from [wiki.mikr.us](https://wiki.mikr.us)
- **Auto-updates**: Documentation syncs automatically with the wiki
- **Rate limiting**: Configured for fair use
- **CORS**: Enabled for cross-origin requests

## 🌍 Server Location

- **Hosted on**: Mikrus VPS (srv47.mikr.us)
- **Region**: Finland (Hetzner Helsinki)
- **Uptime**: 24/7 (monitored)

## 🐛 Troubleshooting

### Connection Failed

1. **Verify server is online**: `curl https://srv47-40231.wykr.es/health`
2. **Check your internet connection**
3. **Restart your IDE** after adding MCP configuration
4. **Verify JSON syntax** in your MCP config file

### Tools Not Showing

1. **Restart your IDE/application** after configuration
2. **Check MCP logs** in your application
3. **Verify the URL** is correct (must include `/sse` endpoint)

### SSL/Certificate Issues

The server uses CloudFlare SSL - if you encounter certificate errors:
- Update your system's root certificates
- Ensure your system clock is correct

## 📚 Source

- **Mikrus Wiki**: https://wiki.mikr.us
- **Documentation Repository**: https://github.com/Mrugalski-pl/mikrus-dokumentacja
- **MCP Protocol**: https://modelcontextprotocol.io

## 🤝 Contributing

Questions or issues? Contact the Mikrus community or open an issue.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Mikrus Hosting** - https://mikr.us
- **Model Context Protocol** - Anthropic
- **Documentation Source** - Mikrus Community

---

**Made for the Mikrus community** 🚀

**Server Status**: [https://srv47-40231.wykr.es/health](https://srv47-40231.wykr.es/health)

