"""
Lagoon MCP Server

A Model Context Protocol (MCP) server implementation for Lagoon CLI commands.
Provides resources for retrieving Lagoon documentation and tools for executing Lagoon CLI commands.
"""

import asyncio
import subprocess
from typing import Any, Dict, List, Optional
import os
import logging
from mcp.server.fastmcp import FastMCP, Context, Image
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('lagoon-mcp')

# Create an MCP server
mcp = FastMCP("Lagoon MCP Server")

class CommandResult(BaseModel):
    """Result of a Lagoon command execution"""
    success: bool = Field(...)
    output: str = Field(...)
    error: Optional[str] = Field(None)

# Security check function for commands
def is_safe_command(command: str) -> bool:
    """Validate that the command is a safe Lagoon CLI command"""
    # Only allow lagoon commands
    if not command.startswith('lagoon '):
        return False
    
    # Prevent command injection
    if any(char in command for char in [';', '&&', '||', '|', '>', '<']):
        return False
    
    return True

# ------------------------
# Resources (Read-only data)
# ------------------------

@mcp.resource("lagoon://commands")
async def get_lagoon_commands() -> Dict[str, str]:
    """Get all available Lagoon CLI commands with descriptions"""
    try:
        result = subprocess.run(['lagoon', 'help'], capture_output=True, text=True)
        
        commands = {}
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('lagoon '):
                parts = line.split(' ', 2)
                if len(parts) >= 3:
                    command = f"{parts[0]} {parts[1]}"
                    description = parts[2]
                    commands[command] = description
        
        return commands
    except Exception as e:
        return {"error": f"Failed to get Lagoon commands: {str(e)}"}

@mcp.resource("lagoon://config")
async def get_lagoon_config() -> Dict[str, Any]:
    """Get current Lagoon configuration"""
    try:
        result = subprocess.run(['lagoon', 'config', 'list'], capture_output=True, text=True)
        
        config = {
            "instances": [],
            "raw_output": result.stdout
        }
        
        current_instance = {}
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line and not line.startswith('NAME') and not line.startswith('----'):
                parts = line.split()
                if len(parts) >= 4:
                    instance = {
                        "name": parts[0],
                        "version": parts[1],
                        "graphql": parts[2],
                        "ssh_hostname": parts[3] if len(parts) > 3 else "",
                        "ssh_port": parts[4] if len(parts) > 4 else "",
                        "is_default": "(default)" in line,
                        "is_current": "(current)" in line
                    }
                    config["instances"].append(instance)
        
        return config
    except Exception as e:
        return {"error": f"Failed to get Lagoon config: {str(e)}"}

@mcp.resource("lagoon://projects")
async def get_lagoon_projects() -> List[Dict[str, Any]]:
    """Get list of all Lagoon projects"""
    try:
        result = subprocess.run(['lagoon', 'list', 'projects'], capture_output=True, text=True)
        
        projects = []
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            return []
        
        # Skip header line and separator line
        for line in lines[2:]:
            if not line.strip():
                continue
                
            parts = line.split()
            if len(parts) >= 3:
                project_id = parts[0]
                project_name = parts[1]
                git_url = parts[2] if len(parts) > 2 else ""
                
                # Extract more info if available
                prod_environment = parts[3] if len(parts) > 3 else ""
                prod_route = parts[4] if len(parts) > 4 else ""
                dev_environments = parts[5] if len(parts) > 5 else "0/0"
                
                projects.append({
                    "id": project_id,
                    "name": project_name,
                    "git_url": git_url,
                    "production_environment": prod_environment,
                    "production_route": prod_route,
                    "dev_environments": dev_environments
                })
        
        return projects
    except Exception as e:
        return [{"error": f"Failed to get Lagoon projects: {str(e)}"}]

@mcp.resource("lagoon://documentation")
async def get_lagoon_documentation() -> str:
    """Get documentation on Lagoon CLI commands"""
    try:
        with open('lagoon-commands.txt', 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading documentation: {str(e)}"

@mcp.resource("lagoon://project/{project_name}/environments")
async def get_project_environments(project_name: str) -> List[Dict[str, Any]]:
    """Get environments for a specific project"""
    try:
        result = subprocess.run(
            ['lagoon', 'list', 'environments', '-p', project_name], 
            capture_output=True, 
            text=True
        )
        
        environments = []
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            return []
        
        # Skip header line and separator line
        for line in lines[2:]:
            if not line.strip():
                continue
                
            parts = line.split()
            if len(parts) >= 2:
                env_id = parts[0]
                env_name = parts[1]
                
                environments.append({
                    "id": env_id,
                    "name": env_name,
                    "project": project_name
                })
        
        return environments
    except Exception as e:
        return [{"error": f"Failed to get environments for project {project_name}: {str(e)}"}]

# ------------------------
# Tools (Commands with side effects)
# ------------------------

@mcp.tool()
async def execute_lagoon_command(command: str, ctx: Context) -> CommandResult:
    """
    Execute a Lagoon CLI command
    
    Parameters:
        command: The full Lagoon command to execute (must start with 'lagoon')
    
    Returns:
        The result of the command execution
    """
    if not is_safe_command(command):
        return CommandResult(
            success=False, 
            output="", 
            error="Invalid or unsafe command. Command must start with 'lagoon' and cannot contain shell operators."
        )
    
    try:
        ctx.info(f"Executing: {command}")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return CommandResult(
            success=process.returncode == 0,
            output=stdout.decode(),
            error=stderr.decode() if stderr else None
        )
    except Exception as e:
        return CommandResult(
            success=False,
            output="",
            error=f"Error executing command: {str(e)}"
        )

@mcp.tool()
async def get_project_info(project_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific project
    
    Parameters:
        project_name: The name of the Lagoon project
    
    Returns:
        Detailed information about the project
    """
    try:
        # Get project details
        result = subprocess.run(
            ['lagoon', 'get', 'project', project_name, '--output-json'], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            return {"error": f"Failed to get project info: {result.stderr}"}
        
        # Get environments
        environments = await get_project_environments(project_name)
        
        # Combine information
        project_info = {
            "name": project_name,
            "raw_output": result.stdout,
            "environments": environments
        }
        
        return project_info
    except Exception as e:
        return {"error": f"Failed to get project info: {str(e)}"}

@mcp.tool()
async def deploy_branch(project_name: str, branch_name: str) -> CommandResult:
    """
    Deploy a branch to a Lagoon project
    
    Parameters:
        project_name: The name of the Lagoon project
        branch_name: The branch to deploy
    
    Returns:
        The result of the deployment command
    """
    command = f"lagoon deploy branch -p {project_name} -b {branch_name}"
    return await execute_lagoon_command(command, Context())

@mcp.tool()
async def ssh_to_environment(project_name: str, environment_name: str) -> CommandResult:
    """
    Get SSH command for an environment
    
    Parameters:
        project_name: The name of the Lagoon project
        environment_name: The environment name
    
    Returns:
        The SSH command to connect to the environment
    """
    command = f"lagoon ssh -p {project_name} -e {environment_name}"
    return await execute_lagoon_command(command, Context())

# ------------------------
# Prompts (Templates for LLM interaction)
# ------------------------

@mcp.prompt()
def lagoon_command_help() -> str:
    """Help text for using Lagoon commands"""
    return """
    I can help you with Lagoon CLI commands. Here are some examples of what you can do:
    
    1. Get a list of all projects:
       - Use the lagoon://projects resource
    
    2. Get environments for a project:
       - Use the lagoon://project/{project_name}/environments resource
    
    3. Execute a specific Lagoon command:
       - Use the execute_lagoon_command tool with a command like "lagoon list projects"
    
    4. Deploy a branch:
       - Use the deploy_branch tool with project_name and branch_name
    
    5. Get SSH command:
       - Use the ssh_to_environment tool with project_name and environment_name
    
    What would you like to do with Lagoon?
    """

@mcp.prompt()
def lagoon_project_prompt(project_list: List[Dict[str, Any]]) -> str:
    """Create a prompt for working with Lagoon projects"""
    project_text = "\n".join([f"- {p['name']} (ID: {p['id']})" for p in project_list[:10]])
    
    return f"""
    Here are the available Lagoon projects:
    
    {project_text}
    
    What would you like to do with these projects?
    """

# Run the server if executed directly
if __name__ == "__main__":
    logger.info("Starting Lagoon MCP Server...")
    try:
        import uvicorn
        uvicorn.run(mcp.sse_app, host="0.0.0.0", port=8000, log_level="info", reload=False)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise 