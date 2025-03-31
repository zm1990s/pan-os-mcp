# PAN-OS MCP Server

This project provides a Model Control Protocol (MCP) server for interacting with Palo Alto Networks firewalls using the XML API. It allows you to use Claude or other compatible tools to manage and configure your PAN-OS devices through natural language.

## Features

- Authenticate with a PAN-OS/Panorama device using API key
- Retrieve system information
- Execute operational commands
- Commit configurations
- Perform configuration actions (set, edit, delete, rename, etc.)
- Push policy from Panorama to managed devices

## Requirements

- Python 3.13+
- Palo Alto Networks firewall
- API access to your PAN-OS device

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/edoscars/pan-os-mcp-server.git
   cd pan-os-mcp-server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On Linux/Mac
   source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit the `pan-os.py` file to configure your PAN-OS device:

```python
# -----------------------------------------------------------------------------
# Pan-OS / Panorama Configuration (adjust to your environment)
# -----------------------------------------------------------------------------
PA_HOST = "your-firewall-ip"
PA_API_KEY = "your-api-key"  
```

## Usage

1. Connect with an MCP client (like Claude) and start interacting with your PAN-OS device.

## Available Commands

The server provides several tools for interacting with PAN-OS:

- `get_system_info`: Retrieve basic system information
- `op_command`: Execute operational commands using XML
- `commit_config`: Commit candidate configurations
- `commit_all_shared_policy`: Push policy from Panorama to managed devices
- `config_action`: Perform configuration actions using XPath

## Security Considerations

- This project is designed for demonstration and usage in controlled environments.
- The API key in the code should be kept secure and not committed to public repositories.
- For production use, ensure proper authentication controls and consider adding TLS verification.

## License

[MIT License](LICENSE)
