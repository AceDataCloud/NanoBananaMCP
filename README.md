# MCP NanoBanana

[![PyPI version](https://img.shields.io/pypi/v/mcp-nanobanana-pro.svg)](https://pypi.org/project/mcp-nanobanana-pro/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-nanobanana-pro.svg)](https://pypi.org/project/mcp-nanobanana-pro/)

[![PyPI version](https://img.shields.io/pypi/v/mcp-nanobanana-pro.svg)](https://pypi.org/project/mcp-nanobanana-pro/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-nanobanana-pro.svg)](https://pypi.org/project/mcp-nanobanana-pro/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI image generation and editing using [Google's Nano Banana](https://deepmind.google/technologies/imagen/) model through the [AceDataCloud API](https://platform.acedata.cloud).

Generate and edit AI images directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Image Generation** - Create high-quality images from text prompts
- **Image Editing** - Modify existing images or combine multiple images
- **Virtual Try-On** - Put clothing on people in photos
- **Product Placement** - Place products in realistic scenes
- **Task Tracking** - Monitor generation progress and retrieve results

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud):

1. Sign up or log in
2. Navigate to [Nano Banana Images API](https://platform.acedata.cloud/documents/23985a11-d713-41d1-ad84-24b021805b3d)
3. Click "Acquire" to get your token

### 2. Install

```bash
# Clone the repository
git clone https://github.com/AceDataCloud/MCPNanoBanana.git
cd MCPNanoBanana

# Install with pip
pip install -e .

# Or with uv (recommended)
uv pip install -e .
```

### 3. Configure

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API token
echo "ACEDATACLOUD_API_TOKEN=your_token_here" > .env
```

### 4. Run

```bash
# Run the server
mcp-nanobanana-pro

# Or with Python directly
python main.py
```

## Claude Desktop Integration

Add to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "nanobanana": {
      "command": "mcp-nanobanana-pro",
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Or if using uv:

```json
{
  "mcpServers": {
    "nanobanana": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/MCPNanoBanana", "mcp-nanobanana-pro"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## Remote HTTP Mode (Hosted)

AceDataCloud hosts a managed MCP server that you can connect to directly — **no local installation required**.

**Endpoint**: `https://nanobanana.mcp.acedata.cloud/mcp`

All requests require a Bearer token in the `Authorization` header. Get your token from [AceDataCloud Platform](https://platform.acedata.cloud).

### Claude Desktop (Remote)

```json
{
  "mcpServers": {
    "nanobanana": {
      "type": "streamable-http",
      "url": "https://nanobanana.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your_api_token_here"
      }
    }
  }
}
```

### Cursor / VS Code

In your MCP client settings, add:

- **Type**: `streamable-http`
- **URL**: `https://nanobanana.mcp.acedata.cloud/mcp`
- **Headers**: `Authorization: Bearer your_api_token_here`

### cURL Test

```bash
# Health check (no auth required)
curl https://nanobanana.mcp.acedata.cloud/health

# MCP initialize (requires Bearer token)
curl -X POST https://nanobanana.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer your_api_token_here" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### Self-Hosting with Docker

```bash
docker pull ghcr.io/acedatacloud/mcp-nanobanana:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-nanobanana:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header and uses it for upstream API calls.

## Available Tools

### Image Generation

| Tool | Description |
|------|-------------|
| `nanobanana_generate_image` | Generate an image from a text prompt |
| `nanobanana_edit_image` | Edit or combine images with AI |

### Tasks

| Tool | Description |
|------|-------------|
| `nanobanana_get_task` | Query a single task status |
| `nanobanana_get_tasks_batch` | Query multiple tasks at once |

## Usage Examples

### Generate Image from Prompt

```
User: Create an image of a sunset over mountains

Claude: I'll generate that image for you.
[Calls nanobanana_generate_image with detailed prompt]
```

### Virtual Try-On

```
User: Put this shirt on this model
[Provides two image URLs]

Claude: I'll combine these images.
[Calls nanobanana_edit_image with both image URLs]
```

### Product Photography

```
User: Place this product in a modern kitchen scene
[Provides product image URL]

Claude: I'll create a product scene for you.
[Calls nanobanana_edit_image with scene description]
```

## Prompt Writing Tips

For best results, include these elements in your prompts:

- **Main Subject**: What is the primary focus?
- **Atmosphere**: What mood should the image convey?
- **Lighting**: How is the scene illuminated?
- **Camera/Lens**: What photographic style? (85mm portrait, wide-angle, etc.)
- **Quality Keywords**: Technical descriptors (bokeh, film grain, HDR, etc.)

### Example Prompt

```
A photorealistic close-up portrait of an elderly Japanese ceramicist
with deep wrinkles and a warm smile. Soft golden hour light streaming
through a window. Captured with an 85mm portrait lens, soft bokeh
background. Serene and masterful mood.
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | **Required** |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `NANOBANANA_REQUEST_TIMEOUT` | Request timeout in seconds | `1800` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Command Line Options

```bash
mcp-nanobanana-pro --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/MCPNanoBanana.git
cd MCPNanoBanana

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=core --cov=tools

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy core tools
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Project Structure

```
NanoBanana/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for NanoBanana API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── image_tools.py     # Image generation/editing tools
│   └── task_tools.py      # Task query tools
├── prompts/                # MCP prompt templates
│   └── __init__.py
├── tests/                  # Test suite
├── deploy/                 # Deployment configs
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── .gitignore
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud NanoBanana API](https://platform.acedata.cloud/documents/23985a11-d713-41d1-ad84-24b021805b3d):

- [NanoBanana Images API](https://platform.acedata.cloud/documents/23985a11-d713-41d1-ad84-24b021805b3d) - Image generation and editing
- [NanoBanana Tasks API](https://platform.acedata.cloud/documents/63e01dc3-eb21-499e-8049-3025c460058f) - Task queries

## Use Cases

- **Portrait Enhancement** - Try different clothing on the same person
- **Product Scene Composition** - Place white-background products in realistic environments
- **Attribute Replacement** - Change materials, colors, or variants
- **Poster Quick Editing** - Rapidly change styles or themes
- **2D to 3D Conversion** - Convert images to 3D product mockups
- **Image Restoration** - Restore old or damaged photos

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
