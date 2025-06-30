# PAN-OS MCP 服务器

本项目提供了一个模型控制协议（MCP）服务器，用于通过XML API与Palo Alto Networks防火墙交互。它允许您使用Claude或其他兼容工具通过自然语言来管理和配置您的PAN-OS设备。

## 功能特点

- 使用API密钥与PAN-OS/Panorama设备进行身份验证
- 获取系统信息
- 执行操作命令
- 提交配置
- 执行配置操作（设置、编辑、删除、重命名等）
- 从Panorama向受管设备推送策略

## 系统要求

- Python 3.13+
- Palo Alto Networks防火墙
- 您的PAN-OS设备的API访问权限

## 安装步骤

1. 克隆代码库：
   ```bash
   git clone https://github.com/zm1990s/pan-os-mcp.git
   ```

2. 安装依赖项：
   ```bash
   pip install -r requirements.txt
   ```

3. 添加到您的Claude Desktop配置中（在args中添加正确的路径）：
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

4. 编辑devices.conf文件以配置您的PAN-OS设备，并将此文件放在安全位置。Agent将读取此配置文件，获取设备凭据，并将它们传递给MCP服务器（即MCP服务器不存储任何设备凭据；这些文件保存在Agent可以访问的本地位置）。

```
[devices]
# 多个PAN-OS设备的配置
# 格式：名称,主机,api_密钥

PA-440-1,10.29.9.1,LUFRPT1aSlXXXXXXX==
PA-440-2,10.29.9.2,LUFRPT1aSlYYYYYYY==
```

## 可用命令

服务器提供了几个与PAN-OS交互的工具：

- `get_system_info`：获取基本系统信息
- `op_command`：使用XML执行操作命令
- `commit_config`：提交候选配置
- `commit_all_shared_policy`：从Panorama向受管设备推送策略
- `config_action`：使用XPath执行配置操作
- `create_log_retrieval_job`：创建日志检索作业并获取job_id
- `get_logs_by_job_id`：基于job_id检索日志

## 使用示例（提示语）

### 检索GlobalProtect日志

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
我需要分析昨天的GlobalProtect用户连接。首先为PA-440创建一个日志检索作业，获取过去1小时的GlobalProtect日志。一旦您有了作业ID，请等待10秒钟让作业完成，然后检索日志并将其保存到临时文件中，阅读临时文件并给我一个日志摘要。
```

### 系统健康检查

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
请对PA-440-2进行全面的健康检查。检查系统资源，包括CPU、内存和会话使用情况。还要验证接口状态和状态。
您需要以下XML命令：
<show><session><info></info></session></show>
<show><system><resources></resources></system></show>
<show><interface>all</interface></show>
<show><system><state></state></system></show>
```

### 安全策略审计

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
审计PA-440-1上的安全策略，并识别任何过于宽松的规则，例如允许任何服务或使用"any"作为源或目标的规则。
还要识别过去30天内没有匹配流量的未使用规则。
```

### 威胁防护分析

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
分析过去一周PA-440-1的威胁日志。按频率识别前5大威胁，显示哪些主机被攻击，并推荐适当的行动来缓解这些威胁。
```

### 接口流量分析

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
向我显示PA-440-1上所有接口的流量统计信息。识别任何具有异常流量模式或错误的接口，并提供每个活动接口的吞吐量摘要。
您可能需要使用此命令：<show><counter><interface>all</interface></counter></show>
```

### VPN隧道状态检查

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
检查PA-440-2上所有IPSec VPN隧道的状态。列出所有隧道、它们的当前状态，并提供所有关闭隧道的详细信息，包括最后连接时间。
```

### URL过滤分析

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
从PA-440-1检索过去24小时的URL过滤日志。分析日志以识别前10个被阻止的网站和产生最多阻止的用户。还要检查是否有任何策略绕过尝试。
```

## 待优化

### 配置备份

```
根据devices.conf中的设备列表和凭据，使用您拥有的适当MCP工具。
从PA-440-2创建并导出配置备份。然后验证备份是否成功创建，并报告备份文件的时间戳和大小。
```

## 安全考虑

- 本项目专为演示和在受控环境中使用而设计。
- 配置文件中的API密钥应保持安全，不应提交到公共存储库中。
- 对于生产使用，请确保适当的身份验证控制，并考虑添加TLS验证。

## 许可证

[MIT许可证](LICENSE)
