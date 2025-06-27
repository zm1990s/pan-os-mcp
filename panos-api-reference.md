# PAN-OS API 参考文档

## 目录
- [XML API](#xml-api)
  - [API 认证](#api-认证)
  - [请求结构](#请求结构)
  - [请求类型](#请求类型)
  - [配置操作](#配置操作)
  - [操作命令示例](#操作命令示例)
  - [提交配置](#提交配置)
  - [日志检索](#日志检索)
  - [报告获取](#报告获取)
  - [用户 ID 映射](#用户-id-映射)
  - [导入导出文件](#导入导出文件)
  - [错误代码](#错误代码)
- [REST API](#rest-api)
  - [基本 URL 结构](#基本-url-结构)
  - [资源方法和查询参数](#资源方法和查询参数)
  - [资源 URI](#资源-uri)
  - [请求和响应示例](#请求和响应示例)
  - [错误代码](#rest-api-错误代码)

## XML API

### API 认证

获取 API 密钥：

```
curl -H "Content-Type: application/x-www-form-urlencoded" -X POST https://<firewall>/api/?type=keygen -d 'user=<user>&password=<password>'
```

响应示例：

```xml
<response status="success">
  <result>
    <key>gJlQWE56987nBxIqyfa62sZeRtYuIo2BgzEA9UOnlZBhU==</key>
  </result>
</response>
```

### 请求结构

```
curl -X POST 'https://<firewall>/api?type=<type>&action=<action>&xpath=<xpath>&key=<apikey>'
```

#### 参数说明

- **key**: API 密钥，用于认证
- **type**: 请求类型，如 config, op, report, log, import, export, user-id, version
- **action**: 操作类型，如 set, edit, delete, show, get 等（当 type=config 时使用）
- **xpath**: XML 路径，指定要操作的配置节点
- **cmd**: 当执行操作命令时使用的 XML 命令

### 请求类型

| 类型 | 描述 | 示例 |
|------|------|------|
| type=keygen | 生成 API 密钥 | `type=keygen` |
| type=config | 修改配置 | `type=config&action=show` |
| type=commit | 提交配置 | `type=commit&cmd=<commit></commit>` |
| type=op | 执行操作命令 | `type=op&cmd=<show><system><info></info></system></show>` |
| type=report | 获取报告 | `type=report&reporttype=dynamic` |
| type=log | 获取日志 | `type=log&log-type=traffic` |
| type=import | 导入文件 | `type=import&category=certificate` |
| type=export | 导出文件 | `type=export&category=tech-support` |
| type=user-id | 更新用户 ID 映射 | `type=user-id` |
| type=version | 显示版本信息 | `type=version` |

### 配置操作

#### 修改配置操作 (type=config)

| 操作 | 描述 | 示例 |
|------|------|------|
| action=set | 设置候选配置 | `action=set&xpath=/config/devices/entry/vsys/entry/address&element=<entry name="test"><ip-netmask>192.0.2.1</ip-netmask></entry>` |
| action=edit | 编辑候选配置 | `action=edit&xpath=/config/devices/entry/vsys/entry/address/entry[@name='test']&element=<entry name="test"><ip-netmask>192.0.2.2</ip-netmask></entry>` |
| action=delete | 删除配置对象 | `action=delete&xpath=/config/devices/entry/vsys/entry/address/entry[@name='test']` |
| action=rename | 重命名配置对象 | `action=rename&xpath=/config/devices/entry/vsys/entry/address/entry[@name='old_name']&newname=new_name` |
| action=clone | 克隆配置对象 | `action=clone&xpath=/config/devices/entry/vsys/entry/address&from=/config/devices/entry/vsys/entry/address/entry[@name='source']&newname=clone_name` |
| action=move | 移动配置对象 | `action=move&xpath=/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='rule1']&where=after&dst=rule2` |

#### 读取配置操作 (type=config)

| 操作 | 描述 | 示例 |
|------|------|------|
| action=show | 获取活动配置 | `action=show&xpath=/config/devices/entry/vsys/entry/address` |
| action=get | 获取候选配置 | `action=get&xpath=/config/devices/entry/vsys/entry/address` |

### 操作命令示例

系统信息：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<show><system><info></info></system></show>&key=<apikey>'
```

响应示例：

```xml
<response status="success">
  <result>
    <system>
      <hostname>PA-3050-A</hostname>
      <ip-address>10.2.3.4</ip-address>
      <model>PA-3050</model>
      <serial>0017010.1529</serial>
      <sw-version>9.0.0-b36</sw-version>
      <app-version>8111-5239</app-version>
      <av-version>3328-3783</av-version>
      <threat-version>8111-5239</threat-version>
      <wildfire-version>0</wildfire-version>
      <url-filtering-version>2019010.1.00005</url-filtering-version>
      <logdb-version>9.0.10</logdb-version>
      <multi-vsys>on</multi-vsys>
      <operational-mode>normal</operational-mode>
    </system>
  </result>
</response>
```

重启系统：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<request><restart><system></system></restart></request>&key=<apikey>'
```

软件更新检查：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<request><system><software><check></check></software></system></request>&key=<apikey>'
```

软件下载：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<request><system><software><download><version>10.1.0</version></download></software></system></request>&key=<apikey>'
```

软件安装：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<request><system><software><install><version>10.1.0</version></install></software></system></request>&key=<apikey>'
```

内容更新下载：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<request><content><upgrade><download><latest/></download></upgrade></content></request>&key=<apikey>'
```

内容更新安装：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<request><content><upgrade><install><version>latest</version></install></upgrade></content></request>&key=<apikey>'
```

查看 GlobalProtect 用户：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<show><global-protect-gateway><current-user/></global-protect-gateway></show>&key=<apikey>'
```

断开 GlobalProtect 用户：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<request><global-protect-gateway><client-logout><gateway>gateway-name</gateway><user>username</user><reason>force-logout</reason><computer>computer-name</computer></client-logout></global-protect-gateway></request>&key=<apikey>'
```

查看作业状态：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<show><jobs><id>job-id</id></jobs></show>&key=<apikey>'
```

配置验证：

```
curl -X POST 'https://<firewall>/api?type=op&cmd=<validate><full></full></validate>&key=<apikey>'
```

### 提交配置

基本提交：

```
curl -X POST 'https://<firewall>/api?type=commit&cmd=<commit></commit>&key=<apikey>'
```

强制提交：

```
curl -X POST 'https://<firewall>/api?type=commit&cmd=<commit><force></force></commit>&key=<apikey>'
```

部分提交：

```
curl -X POST 'https://<firewall>/api?type=commit&action=partial&cmd=<commit><partial><admin><member>admin-name</member></admin></partial></commit>&key=<apikey>'
```

### 日志检索

参数：
- **log-type**: 日志类型 (traffic, threat, config, system, hipmatch, globalprotect, wildfire, url, data, corr, corr-detail, corr-categ, userid, auth, gtp, external, iptag, decryption)
- **query**: 匹配条件
- **nlogs**: 要检索的日志数量，默认 20，最大 5000
- **skip**: 要跳过的日志数量，默认 0
- **dir**: 日志显示顺序 (forward, backward)，默认 backward
- **action**: 日志检索是异步操作，可以使用 action 参数：
  - **action=get**: 检查活动作业状态或检索日志数据
  - **action=finish**: 停止活动作业

示例：

```
curl -X POST 'https://<firewall>/api?type=log&log-type=traffic&query=(receive_time geq "2023/01/01 00:00:00")&nlogs=100&key=<apikey>'
```

响应示例：

```xml
<response status="success">
  <result>
    <job>...</job>
    <log>
      <logs count="20" progress="100">
        <entry logid="5753304543500710425">
          <domain>1</domain>
          <receive_time>2023/01/01 15:43:17</receive_time>
          <serial>001606000117</serial>
          <type>TRAFFIC</type>
          <subtype>start</subtype>
          <src>172.16.1.2</src>
          <dst>10.1.0.246</dst>
          <rule>default allow</rule>
          <!-- 更多日志字段 -->
        </entry>
        <!-- 更多日志条目 -->
      </logs>
    </log>
  </result>
</response>
```

### 报告获取

报告类型：
- **reporttype=dynamic**: 动态报告（ACC 报告）
- **reporttype=predefined**: 预定义报告
- **reporttype=custom**: 自定义报告

动态报告时间范围参数：
- **period=last-60-seconds**: 最近 60 秒
- **period=last-15-minutes**: 最近 15 分钟
- **period=last-hour**: 最近一小时
- **period=last-12-hrs**: 最近 12 小时
- **period=last-calendar-day**: 最近一个日历天
- **period=last-7-days**: 最近 7 天
- **period=last-calendar-week**: 最近一个日历周
- **period=last-30-days**: 最近 30 天

动态报告示例：

```
curl -X POST 'https://<firewall>/api?type=report&reporttype=dynamic&reportname=top-applications-summary&period=last-hour&topn=5&key=<apikey>'
```

预定义报告示例：

```
curl -X POST 'https://<firewall>/api?type=report&reporttype=predefined&reportname=top-application-categories&key=<apikey>'
```

自定义报告示例：

```
curl -X POST 'https://<firewall>/api?type=report&reporttype=dynamic&reportname=custom-dynamic-report&cmd=<type><appstat><aggregate-by><member>category-of-name</member><member>technology-of-name</member></aggregate-by></appstat></type><period>last-24-hrs</period><topn>10</topn><topm>10</topm><query>(name+neq+"")AND(vsys+eq+"vsys1")</query>&key=<apikey>'
```

### 用户 ID 映射

用户登录映射：

```xml
<uid-message>
  <version>1.0</version>
  <type>update</type>
  <payload>
    <login>
      <entry name="domain\uid1" ip="10.1.1.1" timeout="20"></entry>
    </login>
    <groups>
      <entry name="group1">
        <members>
          <entry name="user1"/>
          <entry name="user2"/>
        </members>
      </entry>
    </groups>
  </payload>
</uid-message>
```

多用户系统设置：

```xml
<uid-message>
  <payload>   
    <multiusersystem> 
      <entry ip="10.1.1.2" startport="xxxxx" endport="xxxxx" blocksize="xxx">   
    </multiusersystem> 
  </payload>   
  <type>update</type>   
  <version>1.0</version>   
</uid-message>
```

多用户系统登录事件：

```xml
<uid-message>
<payload>   
  <login> 
    <entry name="acme\jparker" ip="10.1.1.23" blockstart="20100"> 
  </login> 
</payload> 
<type>update</type> 
<version>1.0</version> 
</uid-message>
```

动态地址组 IP 地址注册：

```xml
<uid-message>  
  <version>1.0</version>  
  <type>update</type>  
  <payload>       
    <register>  
      <entry ip="10.1.1.1">  
        <tag> 
          <member timeout="3600">tag-name</member>  
        </tag> 
      </entry> 
    </register>  
    <unregister>  
      <entry ip="10.1.1.3"/>  
      <tag> 
        <member>tag-name-2</member>  
      </tag> 
    </entry> 
    </unregister>  
  </payload>  
</uid-message>
```

为用户注册标签：

```xml
<uid-message>
  <version>1.0</version>
  <type>update</type>
  <payload>
    <register-user>
      <entry user="paloaltonetworks\john">
        <tag>
          <member>finished_ethics_training</member>
          <member>mac_user</member>
        </tag>
      </entry>
    </register-user>
  </payload>
</uid-message>
```

### 导入导出文件

#### 导出文件

导出技术支持数据：

```
curl -X POST 'https://<firewall>/api?type=export&category=tech-support&key=<apikey>'
```

导出证书：

```
curl -X POST 'https://<firewall>/api?type=export&category=certificate&certificate-name=<certificate_name>&format=pem&include-key=no&key=<apikey>'
```

导出数据包捕获：

```
curl -X POST 'https://<firewall>/api?type=export&category=application-pcap&from=<yyyymmdd>/<filename>&key=<apikey>'
```

#### 导入文件

导入证书：

```
curl -F "file=@<path of the file>" "https://<firewall>/api/?key=<apikey>&type=import&category=certificate&certificate-name=<certificate_name>&format=pem"
```

导入配置：

```
curl -F "file=@<path of the file>" "https://<firewall>/api/?key=<apikey>&type=import&category=configuration"
```

导入许可证：

```
curl -F "file=@<path of the file>" "https://<firewall>/api/?key=<apikey>&type=import&category=license"
```

### 错误代码

| 错误代码 | 名称 | 描述 |
|----------|------|------|
| 400 | Bad request | 缺少必需参数或使用了非法参数值 |
| 403 | Forbidden | 认证或授权错误，包括无效密钥或管理员访问权限不足 |
| 1 | Unknown command | 未识别的配置或操作命令 |
| 6 | Bad Xpath | 命令中指定的 xpath 无效 |
| 7 | Object not present | xpath 指定的对象不存在 |
| 8 | Object not unique | 对于操作单个对象的命令，指定的对象不唯一 |
| 10 | Reference count not zero | 对象无法删除，因为其他对象引用了它 |

## REST API

### 基本 URL 结构

```
https://<firewall or panorama>/restapi/v10.1/<resource URI>
```

### 资源方法和查询参数

| 方法 | 操作 | 必需参数 | 可选参数 |
|------|------|----------|----------|
| GET | 读取资源列表 | location, vsys (如果 location=vsys) | output-format |
| POST | 创建资源 | name, location, vsys (如果 location=vsys) | input-format, output-format |
| PUT | 修改资源 | name, location, vsys (如果 location=vsys) | input-format, output-format |
| DELETE | 删除资源 | name, location, vsys (如果 location=vsys) | output-format |
| POST (:rename) | 重命名资源 | name, location, vsys (如果 location=vsys), newname | output-format |
| POST (:move) | 移动策略规则 | name, location, vsys (如果 location=vsys), where, dst (如果 where=before 或 after) | output-format |

### 资源 URI

#### 对象资源

| 资源类型 | URI |
|----------|-----|
| 地址对象 | /restapi/v10.1/Objects/Addresses |
| 地址组 | /restapi/v10.1/Objects/AddressGroups |
| 区域 | /restapi/v10.1/Objects/Regions |
| 应用 | /restapi/v10.1/Objects/Applications |
| 应用组 | /restapi/v10.1/Objects/ApplicationGroups |
| 应用过滤器 | /restapi/v10.1/Objects/ApplicationFilters |
| 服务 | /restapi/v10.1/Objects/Services |
| 服务组 | /restapi/v10.1/Objects/ServiceGroups |
| 标签 | /restapi/v10.1/Objects/Tags |
| GlobalProtect HIP 对象 | /restapi/v10.1/Objects/GlobalProtectHIPObjects |
| GlobalProtect HIP 配置文件 | /restapi/v10.1/Objects/GlobalProtectHIPProfiles |
| 外部动态列表 | /restapi/v10.1/Objects/ExternalDynamicLists |
| 自定义数据模式 | /restapi/v10.1/Objects/CustomDataPatterns |
| 自定义间谍软件签名 | /restapi/v10.1/Objects/CustomSpywareSignatures |
| 自定义漏洞签名 | /restapi/v10.1/Objects/CustomVulnerabilitySignatures |
| 自定义 URL 类别 | /restapi/v10.1/Objects/CustomURLCategories |
| 防病毒安全配置文件 | /restapi/v10.1/Objects/AntivirusSecurityProfiles |
| 反间谍软件安全配置文件 | /restapi/v10.1/Objects/AntiSpywareSecurityProfiles |
| 漏洞防护安全配置文件 | /restapi/v10.1/Objects/VulnerabilityProtectionSecurityProfiles |
| URL 过滤安全配置文件 | /restapi/v10.1/Objects/URLFilteringSecurityProfiles |
| 文件阻止安全配置文件 | /restapi/v10.1/Objects/FileBlockingSecurityProfiles |
| WildFire 分析安全配置文件 | /restapi/v10.1/Objects/WildFireAnalysisSecurityProfiles |
| 数据过滤安全配置文件 | /restapi/v10.1/Objects/DataFilteringSecurityProfiles |
| DoS 防护安全配置文件 | /restapi/v10.1/Objects/DoSProtectionSecurityProfiles |
| 安全配置文件组 | /restapi/v10.1/Objects/SecurityProfileGroups |
| 日志转发配置文件 | /restapi/v10.1/Objects/LogForwardingProfiles |
| 认证强制执行 | /restapi/v10.1/Objects/AuthenticationEnforcements |
| 解密配置文件 | /restapi/v10.1/Objects/DecryptionProfiles |
| 解密转发配置文件 | /restapi/v10.1/Objects/DecryptionForwardingProfiles |
| 计划 | /restapi/v10.1/Objects/Schedules |
| SD-WAN 路径质量配置文件 | /restapi/v10.1/Objects/SDWANPathQualityProfiles |
| SD-WAN 流量分配配置文件 | /restapi/v10.1/Objects/SDWANTrafficDistributionProfiles |

#### 策略资源

| 资源类型 | URI |
|----------|-----|
| 安全规则 | /restapi/v10.1/Policies/SecurityRules |
| NAT 规则 | /restapi/v10.1/Policies/NATRules |
| QoS 规则 | /restapi/v10.1/Policies/QoSRules |
| 基于策略的转发规则 | /restapi/v10.1/Policies/PolicyBasedForwardingRules |
| 解密规则 | /restapi/v10.1/Policies/DecryptionRules |
| 隧道检查规则 | /restapi/v10.1/Policies/TunnelInspectionRules |
| 应用覆盖规则 | /restapi/v10.1/Policies/ApplicationOverrideRules |
| 认证规则 | /restapi/v10.1/Policies/AuthenticationRules |
| DoS 规则 | /restapi/v10.1/Policies/DoSRules |
| SD-WAN 规则 | /restapi/v10.1/Policies/SDWANRules |

#### 网络资源

| 资源类型 | URI |
|----------|-----|
| 以太网接口 | /restapi/v10.1/Network/EthernetInterfaces |
| 聚合以太网接口 | /restapi/v10.1/Network/AggregateEthernetInterfaces |
| VLAN 接口 | /restapi/v10.1/Network/VLANInterfaces |
| 环回接口 | /restapi/v10.1/Network/LoopbackInterfaces |
| 隧道接口 | /restapi/v10.1/Network/TunnelIntefaces |
| SD-WAN 接口 | /restapi/v10.1/Network/SDWANInterfaces |
| 安全区域 | /restapi/v10.1/Network/Zones |
| VLAN | /restapi/v10.1/Network/VLANs |
| 虚拟线路 | /restapi/v10.1/Network/VirtualWires |
| 虚拟路由器 | /restapi/v10.1/Network/VirtualRouters |
| IPSec 隧道 | /restapi/v10.1/Network/IPSecTunnels |
| GRE 隧道 | /restapi/v10.1/Network/GRETunnels |
| DHCP 服务器 | /restapi/v10.1/Network/DHCPServers |
| DHCP 中继 | /restapi/v10.1/Network/DHCPRelays |
| DNS 代理 | /restapi/v10.1/Network/DNSProxies |
| GlobalProtect 门户 | /restapi/v10.1/Network/GlobalProtectPortals |
| GlobalProtect 网关 | /restapi/v10.1/Network/GlobalProtectGateways |

#### 设备资源

| 资源类型 | URI |
|----------|-----|
| 虚拟系统 | /restapi/v10.1/Device/VirtualSystems |

### 请求和响应示例

#### 创建地址对象

请求：

```
curl -X POST \
  'https://<firewall>/restapi/v10.1/Objects/Addresses?location=shared&name=web-servers' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": [
        {
            "@location": "shared",
            "@name": "web-servers",
            "description": "Web servers",
            "fqdn": "www.example.com",
            "tag": {
                "member": [
                    "web"
                ]
            }
        }
    ]
}'
```

响应：

```json
{
    "@code": "20",
    "@status": "success",
    "msg": "command succeeded"
}
```

#### 编辑地址对象

请求：

```
curl -X PUT \
  'https://<firewall>/restapi/v10.1/Objects/Addresses?location=shared&name=web-servers' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": [
        {
            "@location": "shared",
            "@name": "web-servers",
            "description": "Updated description",
            "fqdn": "www.example.com",
            "tag": {
                "member": [
                    "web",
                    "production"
                ]
            }
        }
    ]
}'
```

#### 重命名地址对象

请求：

```
curl -X POST \
  'https://<firewall>/restapi/v10.1/Objects/Addresses:rename?location=shared&name=web-servers&newname=production-web-servers' \
  -H 'X-PAN-KEY: <apikey>'
```

#### 删除地址对象

请求：

```
curl -X DELETE \
  'https://<firewall>/restapi/v10.1/Objects/Addresses?location=shared&name=web-servers' \
  -H 'X-PAN-KEY: <apikey>'
```

#### 获取地址对象列表

请求：

```
curl -X GET \
  'https://<firewall>/restapi/v10.1/Objects/Addresses?location=vsys&vsys=vsys1' \
  -H 'X-PAN-KEY: <apikey>'
```

响应：

```json
{
    "@code": "19",
    "@status": "success",
    "result": {
        "@count": "3",
        "@total-count": "3",
        "entry": [
            {
                "@location": "vsys",
                "@name": "fqdn1",
                "@vsys": "vsys1",
                "fqdn": "www.test.com"
            },
            {
                "@location": "vsys",
                "@name": "Peer1",
                "@vsys": "vsys1",
                "ip-netmask": "172.0.0.1/24"
            },
            {
                "@location": "vsys",
                "@name": "Peer2renamed",
                "@oldname": "Peer2",
                "@vsys": "vsys1",
                "ip-netmask": "200.0.0.1/24"
            }
        ]
    }
}
```

#### 创建安全策略规则

请求：

```
curl -X POST \
  'https://<firewall>/restapi/v10.1/Policies/SecurityRules?location=vsys&vsys=vsys1&name=allow-web' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": [
        {
            "@location": "vsys",
            "@name": "allow-web",
            "@vsys": "vsys1",
            "action": "allow",
            "application": {
                "member": [
                    "web-browsing"
                ]
            },
            "category": {
                "member": [
                    "any"
                ]
            },
            "destination": {
                "member": [
                    "web-servers"
                ]
            },
            "from": {
                "member": [
                    "trust"
                ]
            },
            "source-hip": {
                "member": [
                    "any"
                ]
            },
            "destination-hip": {
                "member": [
                    "any"
                ]
            },
            "service": {
                "member": [
                    "application-default"
                ]
            },
            "source": {
                "member": [
                    "any"
                ]
            },
            "source-user": {
                "member": [
                    "any"
                ]
            },
            "to": {
                "member": [
                    "untrust"
                ]
            }
        }
    ]
}'
```

#### 创建 SD-WAN 接口

请求：

```
curl -X POST \
  'https://<panorama>/restapi/v10.1/network/sdwanInterfaces?location=template&template=SDWAN-Branch-Network&name=sdwan.1' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": {
        "@name": "sdwan.1",
        "interface": {
            "member": [
                "ethernet1/3",
                "ethernet1/4"
            ]
        }
    }
}'
```

#### 创建安全区域

请求：

```
curl -X POST \
  'https://<panorama>/restapi/v10.1/network/zones?location=template&template=SDWAN-Branch-Network&name=Untrust' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": {
        "@name": "Untrust",
        "enable-user-identification": "no",
        "network": {
            "layer3": {
                "member": [
                    "ethernet1/1",
                    "ethernet1/2",
                    "ethernet1/3",
                    "sdwan.1"
                ]
            }
        }
    }
}'
```

#### 配置虚拟路由器

请求：

```
curl -X PUT \
  'https://<firewall>/restapi/v10.1/Network/VirtualRouters?name=default' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": {
        "@name": "default",
        "interface": {
            "member": [
                "ethernet1/3",
                "ethernet1/4"
            ]
        }
    }
}'
```

#### 创建解密配置文件

请求：

```
curl -X POST \
  'https://<firewall>/restapi/v10.1/Objects/DecryptionProfiles?name=decryptProfileTest&location=vsys&vsys=vsys1' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": {
        "@name": "decryptProfileTest",
        "ssl-forward-proxy": {
            "auto-include-altname": "no",
            "block-client-cert": "no",
            "block-expired-certificate": "no",
            "block-if-no-resource": "no",
            "block-timeout-cert": "no",
            "block-tls13-downgrade-no-resource": "no",
            "block-unknown-cert": "no",
            "block-unsupported-cipher": "no",
            "block-unsupported-version": "no",
            "block-untrusted-issuer": "no",
            "restrict-cert-exts": "no",
            "strip-alpn": "no"
        },
        "ssl-protocol-settings": {
            "auth-algo-md5": "no",
            "auth-algo-sha1": "yes",
            "auth-algo-sha256": "yes",
            "auth-algo-sha384": "yes",
            "enc-algo-3des": "yes",
            "enc-algo-aes-128-cbc": "yes",
            "enc-algo-aes-128-gcm": "yes",
            "enc-algo-aes-256-cbc": "yes",
            "enc-algo-aes-256-gcm": "yes",
            "enc-algo-chacha20-poly1305": "yes",
            "enc-algo-rc4": "yes",
            "keyxchg-algo-dhe": "yes",
            "keyxchg-algo-ecdhe": "yes",
            "keyxchg-algo-rsa": "yes",
            "max-version": "tls1-2",
            "min-version": "tls1-0"
        }
    }
}'
```

#### 在 Panorama 上创建 SD-WAN 策略规则

请求：

```
curl -X POST \
  'https://<panorama>/restapi/v10.1/policies/sdwanprerules?location=device-group&device-group=SD-WAN_Branch&name=HQ_Service_Test' \
  -H 'X-PAN-KEY: <apikey>' \
  -d '{
    "entry": {
        "@name": "HQ_Service_Test",
        "from": {
            "member": [
                "Trust-PA220"
            ]
        },
        "to": {
            "member": [
                "Untrust-PA220"
            ]
        },
        "source": {
            "member": [
                "any"
            ]
        },
        "source-user": {
            "member": [
                "any"
            ]
        },
        "destination": {
            "member": [
                "any"
            ]
        },
        "application": {
            "member": [
                "ping"
            ]
        },
        "service": {
            "member": [
                "any"
            ]
        },
        "negate-source": "no",
        "negate-destination": "no",
        "disabled": "no",
        "description": "For SD-WAN test",
        "path-quality-profile": "general-business",
        "action": {
            "traffic-distribution-profile": "BroadBand2"
        }
    }
}'
```

### REST API 错误代码

| 错误代码 | 描述 |
|----------|------|
| 1 | 操作被取消，通常由调用者取消 |
| 2 | 未知的内部服务器错误 |
| 3 | 错误请求。调用者指定了无效参数 |
| 4 | 网关超时。防火墙或 Panorama 模块在后端操作完成前超时 |
| 5 | 未找到。请求的实体未找到 |
| 6 | 冲突。调用者尝试创建的实体已存在 |
| 7 | 禁止。调用者没有执行指定操作的权限 |
| 16 | 未授权。请求没有有效的身份验证凭据来执行操作 |
