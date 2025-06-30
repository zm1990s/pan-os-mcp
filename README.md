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
   git clone https://github.com/zm1990s/pan-os-mcp.git
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add to your Claude Desktop configuration (add the correct path in the args):
   ```bash
   {
     "mcpServers": {
       "pan-os":{
         "command": "uv",
         "args":[
           "run",
           "/path-to-script/pan-os.py"
         ]
       }
     }
   }
   ```

4. Edit the devices.conf file to configure your PAN-OS devices and place this file in a secure location. The Agent will read this configuration file, obtain the devices' credentials, and pass them to the MCP Server (i.e., the MCP Server does not store any device credentials; these files are kept locally where the Agent can access them).

```
[devices]
# Configuration for multiple PAN-OS devices
# Format: name,host,api_key

PA-440-1,10.29.9.1,LUFRPT1aSlXXXXXXX==
PA-440-2,10.29.9.2,LUFRPT1aSlYYYYYYY==
```

## Available Commands

The server provides several tools for interacting with PAN-OS:

- `get_system_info`: Retrieve basic system information
- `op_command`: Execute operational commands using XML
- `commit_config`: Commit candidate configurations
- `commit_all_shared_policy`: Push policy from Panorama to managed devices
- `config_action`: Perform configuration actions using XPath
- `create_log_retrieval_job`: Create a Log retrieval job and obtain job_id.
- `get_logs_by_job_id`: Retrieval logs based on job_id.

## Usage Examples(Prompts)

### Retrieving GlobalProtect Logs

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
I need to analyze GlobalProtect user connections from yesterday. First create a log retrieval job for PA-440 to get GlobalProtect logs from the last 1 hours. Once you have the job ID, please wait for 10 seconds for the job to complete, then retrieve the logs and save it to a temporary file, read through the temporary file and give me a summary of the logs.
```

### System Health Check

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
Please perform a comprehensive health check on PA-440-2. Check system resources including CPU, memory, and 
session utilization. Also verify interface status and states.
You'll need the following XML commands:
<show><session><info></info></session></show>
<show><system><resources></resources></system></show>
<show><interface>all</interface></show>
<show><system><state></state></system></show>

```

### Security Policy Audit

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
Audit the security policies on PA-440-1 and identify any overly permissive rules, such as those allowing 
any service or using 'any' as source or destination. Also identify unused rules that haven't matched 
traffic in the past 30 days.
```

### Threat Prevention Analysis

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
Analyze threat logs from PA-440-1 for the past week. Identify the top 5 threats by frequency, show which 
hosts were targeted, and recommend appropriate actions to mitigate these threats.
```


### Interface Traffic Analysis

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
Show me the traffic statistics for all interfaces on PA-440-1. Identify any interfaces with unusual 
traffic patterns or errors, and provide a summary of throughput for each active interface.
You might need to use this command: <show><counter><interface>all</interface></counter></show>
```

### VPN Tunnel Status Check

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
Check the status of all IPSec VPN tunnels on PA-440-2. List all tunnels, their current state, and provide 
details on any tunnels that are down including their last connection time.
```

### URL Filtering Analysis

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
Retrieve URL filtering logs from PA-440-1 for the past 24 hours. Analyze the logs to identify the top 10 
blocked websites and users generating the most blocks. Also check if there are any policy bypass attempts.
```

## To be optimized

### Configuration Backup

```
Based on the device list and credentials in devices.conf. Use the appropriate MCP tools you have.
Create and export a configuration backup from PA-440-2. Then verify the backup was created successfully 
and report the timestamp and size of the backup file.
```

## Security Considerations

- This project is designed for demonstration and usage in controlled environments.
- The API keys in the config file should be kept secure and not committed to public repositories.
- For production use, ensure proper authentication controls and consider adding TLS verification.

## License

[MIT License](LICENSE)
