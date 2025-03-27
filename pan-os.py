import xml.etree.ElementTree as ET
from typing import Any, Optional
import httpx
import mcp.server.stdio
from mcp.server.fastmcp import FastMCP
import mcp

# -----------------------------------------------------------------------------
# Pan-OS / Panorama Configuration (adjust to your environment)
# -----------------------------------------------------------------------------
PA_HOST = "192.168.188.101"
PA_API_KEY = "LUFRPT1jS1JuckhGQXlORGVZVkthbjRsamdGS29PV009ci84WmxzU2E4RzN6QVZvZDZNM01hQ3IyVXNhZGF6ODl0ZnRQMWpRZnlXdUlROWZ3YmFGVlBDZVhEZjlkKzVuNQ=="  
USER_AGENT = "MyAsyncClient/1.0"

mcp = FastMCP("pan-os")

def xml_to_dict(elem: ET.Element) -> dict[str, Any]:
    node_dict: dict[str, Any] = {}

    # Attributes => _attributes
    if elem.attrib:
        node_dict["_attributes"] = dict(elem.attrib)

    # Text => _text
    text = (elem.text or "").strip()
    if text:
        node_dict["_text"] = text

    # Recursively handle children
    for child in elem:
        tag = child.tag
        child_dict = xml_to_dict(child)

        if tag in node_dict:
            # Convert existing entry to a list if it isn't one already
            if not isinstance(node_dict[tag], list):
                node_dict[tag] = [node_dict[tag]]
            node_dict[tag].append(child_dict)
        else:
            node_dict[tag] = child_dict

    return node_dict

async def panos_xml_api_request(
    api_type: str,
    *,
    action: Optional[str] = None,
    extra_params: Optional[dict[str, Any]] = None,
    method: str = "GET",
    xml_body: Optional[str] = None,
) -> dict[str, Any]:
    """
    Send a request to the PAN-OS XML API and parse the response into a dict.

    :param api_type: e.g. "keygen", "config", "commit", "op", "log", "report", 
                     "import", "export", "user-id", "version", etc.
    :param action: e.g. "set", "show", "delete", "move", "partial", "all", ...
    :param extra_params: Additional query params dict
    :param method: "GET" or "POST"
    :param xml_body: For requests requiring XML content (like 'cmd' or 'element'),
                     pass the raw XML string here. The function will add it as 
                     the appropriate parameter (e.g. cmd=<xml_body>).
    :return: Parsed XML response as Python dict
    """

    if extra_params is None:
        extra_params = {}

    # Base query parameters
    query_params = {
        "type": api_type,
        "key": PA_API_KEY,
    }

    # If there's an action, include it
    if action:
        query_params["action"] = action

    # If we have a raw XML body that goes into e.g. "cmd" or "element", 
    # we must decide which param it belongs to (it depends on the type of request).
    # We'll adopt a simple approach: for 'op' => cmd=..., for 'config' => depends on the action
    # but typically 'element' or 'cmd'. For commit => cmd=...
    # We'll let the caller decide if it's "cmd" or "element" by passing an extra_params if needed,
    # or we can guess here based on the request type:
    if xml_body:
        if api_type in ("op", "commit", "user-id", "report", "log", "version"):
            # Typically these use cmd= for the raw XML
            query_params["cmd"] = xml_body
        elif api_type == "config":
            # Some actions use element= for the body (e.g. set/edit), 
            # others might use cmd= for the multi-config or for show?
            # We'll just put it under 'element' by default here, or rely on extra_params
            query_params["element"] = xml_body
        else:
            # If we do not have a known pattern, fallback:
            query_params["cmd"] = xml_body

    # Merge any extra params
    for k, v in extra_params.items():
        query_params[k] = v

    # Do the HTTP request
    url = f"https://{PA_HOST}/api/"
    headers = {"User-Agent": USER_AGENT}
    verify_tls = False  # set True in production

    async with httpx.AsyncClient(verify=verify_tls) as client:
        try:
            if method.upper() == "GET":
                resp = await client.get(url, params=query_params, headers=headers, timeout=30.0)
            else:
                resp = await client.post(url, data=query_params, headers=headers, timeout=30.0)

            resp.raise_for_status()
            # Parse XML
            root = ET.fromstring(resp.text)
            return xml_to_dict(root)

        except Exception as exc:
            return {
                "error": f"Request to PAN-OS XML API failed: {exc}"
            }

# -----------------------------------------------------------------------------
# Helper Functions for XML Parsing
# -----------------------------------------------------------------------------
def element_to_dict(elem: ET.Element) -> dict[str, Any]:
    """
    Recursively convert an ElementTree node into a Python dictionary.
    - elem.text becomes the '_text' field (if non-empty).
    - elem.attrib becomes the '_attributes' field (if any).
    - Child nodes become keys. If multiple children share a tag,
      they get aggregated in a list.
    """
    node_dict: dict[str, Any] = {}

    # Store attributes under '_attributes' key if they exist
    if elem.attrib:
        node_dict["_attributes"] = dict(elem.attrib)

    # Store element text if it's non-empty and not just whitespace
    text = (elem.text or "").strip()
    if text:
        node_dict["_text"] = text

    # Process child elements
    for child in elem:
        child_tag = child.tag
        child_dict = element_to_dict(child)

        # If this tag already exists, turn it into (or append to) a list
        if child_tag in node_dict:
            if not isinstance(node_dict[child_tag], list):
                node_dict[child_tag] = [node_dict[child_tag]]
            node_dict[child_tag].append(child_dict)
        else:
            node_dict[child_tag] = child_dict

    return node_dict

def format_result(xml_text: str) -> dict[str, Any]:
    """
    Parse an XML string into a nested Python dictionary, including element text
    and attributes. Useful for processing PAN-OS XML API responses.
    """
    root = ET.fromstring(xml_text)
    return element_to_dict(root)

# -----------------------------------------------------------------------------
# Async function to make a PAN-OS XML API request
# -----------------------------------------------------------------------------
async def make_panos_xml_request(cmd: str) -> Optional[dict[str, Any]]:
    """
    Make a request to the PAN-OS XML API, expecting an XML response.
    Returns a nested dict representation of the XML on success, or None on error.
    """
    headers = {
        "User-Agent": USER_AGENT,
        # Not strictly required, but you can include if you like:
        # "Accept": "application/xml"
    }
    params = {
        "type": "op",
        "cmd": cmd,
        "key": PA_API_KEY
    }

    # If using a self-signed cert in a test environment, set verify=False.
    # In production, install a CA-signed cert on the firewall or supply a cert bundle.
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(
                f"https://{PA_HOST}/api/",
                headers=headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return format_result(response.text)

        except Exception:
            # In real code, you might want to log the exception details.
            return None

# -----------------------------------------------------------------------------
# MCP Tool Example: Retrieve System Info from PAN-OS
# Adding more tools like this can improve the performance since we are explaining in details how to use the API
# -----------------------------------------------------------------------------
@mcp.tool()
async def get_system_info() -> dict[str, Any]:
    """
    Example MCP tool function that retrieves basic system info
    from a PAN-OS device using the XML API.
    """
    # The <show><system><info></info></system></show> command is like "show system info"
    cmd_xml = "<show><system><info></info></system></show>"
    data = await make_panos_xml_request(cmd_xml)
    if not data:
        return {"error": "Failed to retrieve system info."}
    return data

@mcp.tool()
async def op_command(xml_cmd: str) -> dict[str, Any]:
    """
    Executes an arbitrary operational command (e.g. <show><system><info></info></system></show>)
    or 
    <request><restart><system></system></restart></request>
    """
    return await panos_xml_api_request(
        api_type="op",
        xml_body=xml_cmd,
        method="POST"
    )

@mcp.tool()
async def commit_config(force: bool = False, partial_xml: Optional[str] = None) -> dict[str, Any]:
    """
    Commit the candidate config on the firewall. 
    Optionally handle force commits or partial commits (by providing partial_xml).
    :param force: If True, commits with <force></force>
    :param partial_xml: e.g. <partial><admin><member>bob</member></admin></partial>
    """
    # Build the commit command
    # <commit> [ <force></force> ] [ <partial>...</partial> ] </commit>
    commit_elt = "<commit>"
    if force:
        commit_elt += "<force></force>"
    if partial_xml:
        commit_elt += partial_xml
    commit_elt += "</commit>"

    # type=commit => pass the commit XML in cmd=
    return await panos_xml_api_request(
        api_type="commit",
        xml_body=commit_elt,
        method="POST"
    )


@mcp.tool()
async def commit_all_shared_policy(device_group: Optional[str] = None, validate_only: bool = False) -> dict[str, Any]:
    """
    Commit (push) changes from Panorama to managed devices.
    If 'validate_only' is True, no actual commit is performed (just validation).
    If 'device_group' is provided, push only to that device-group.
    """
    # <commit-all><shared-policy>[<validate-only/>][<device-group><entry name="MyDG"/></device-group>]</shared-policy></commit-all>
    commit_all_xml = "<commit-all><shared-policy>"

    if validate_only:
        commit_all_xml += "<validate-only></validate-only>"

    if device_group:
        commit_all_xml += f"<device-group><entry name=\"{device_group}\"/></device-group>"

    commit_all_xml += "</shared-policy></commit-all>"

    return await panos_xml_api_request(
        api_type="commit",
        action="all",
        xml_body=commit_all_xml,
        method="POST"
    )


@mcp.tool()
async def config_action(
    action: str,
    xpath: str,
    element_xml: Optional[str] = None,
    newname: Optional[str] = None,
    from_path: Optional[str] = None,
    dst: Optional[str] = None,
    where: Optional[str] = None,
) -> dict[str, Any]:
    """
    Perform config actions (set/edit/delete/rename/clone/move/override...) on a 
    specified XPath. 
    :param action: e.g. "show", "get", "set", "edit", "delete", "rename",
                          "clone", "move", "override", "multi-move", ...
    :param xpath:  The target XPath, e.g. /config/devices/entry/vsys/entry/rulebase/security
    :param element_xml: XML snippet to set or edit (if any)
    :param newname: Used with rename or clone
    :param from_path: The source for clone
    :param dst: Used with move action to indicate the destination
    :param where: "before", "after", "top", or "bottom" for move actions
    """
    extra_params = {"xpath": xpath}
    if element_xml:
        # For 'set' or 'edit' or 'override', we must supply 'element='
        # We'll pass it as raw XML for the request function
        pass

    if newname:
        extra_params["newname"] = newname
    if from_path:
        extra_params["from"] = from_path
    if dst:
        extra_params["dst"] = dst
    if where:
        extra_params["where"] = where

    return await panos_xml_api_request(
        api_type="config",
        action=action,
        extra_params=extra_params,
        xml_body=element_xml,  # Will be placed under 'element=' by default
        method="POST"
    )

if __name__ == "__main__":
    mcp.run(transport='stdio')