# Lagoon CLI Commands Reference

This repository contains reference documentation for Lagoon CLI commands and a Model Context Protocol (MCP) server that AI assistants can connect to for executing Lagoon operations.

## Overview

[Lagoon](https://lagoon.sh/) is a Docker-based infrastructure management system that helps developers build, deploy, and manage containerized applications. The Lagoon CLI provides a command-line interface for interacting with Lagoon instances.

This repository provides:
- A comprehensive reference of Lagoon CLI commands (`lagoon-commands.txt`)
- A Model Context Protocol (MCP) server for AI assistants to interact with Lagoon (`mcp_server.py`)
- Easy-to-access documentation for AI tools to reference

## Lagoon MCP Server

The Lagoon MCP Server is an implementation of the [Model Context Protocol](https://modelcontextprotocol.io/) that provides AI assistants like Claude with direct access to Lagoon CLI capabilities through a standardized API.

### Features

- **Resources**: Provide read-only access to Lagoon information
  - `lagoon://commands` - List all available Lagoon commands
  - `lagoon://config` - Get current Lagoon configuration
  - `lagoon://projects` - List all Lagoon projects
  - `lagoon://documentation` - Access the full Lagoon CLI documentation
  - `lagoon://project/{project_name}/environments` - List environments for a project

- **Tools**: Execute Lagoon commands through the MCP server
  - `execute_lagoon_command` - Run any Lagoon CLI command
  - `get_project_info` - Get detailed information about a project
  - `deploy_branch` - Deploy a branch to a Lagoon project
  - `ssh_to_environment` - Get SSH command for an environment

### Running the MCP Server

#### Using Docker

```bash
# Build the Docker image
docker build -t lagoon-mcp-server .

# Run the container
docker run -p 8000:8000 lagoon-mcp-server
```

#### Manual Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have Lagoon CLI installed and configured:
   ```bash
   # Example: Install Lagoon CLI on macOS
   brew tap uselagoon/lagoon-cli
   brew install lagoon
   
   # Configure Lagoon CLI
   lagoon config add --lagoon amazeeio \
       --graphql https://api.lagoon.amazeeio.cloud/graphql \
       --hostname ssh.lagoon.amazeeio.cloud \
       --port 32222
   ```

3. Run the MCP server:
   ```bash
   python mcp_server.py
   ```

### Connecting AI Assistants to the MCP Server

To use the Lagoon MCP server with Claude:

1. Launch Claude Desktop
2. Open the Data & Tool Connections settings
3. Add a new MCP server connection with the URL: `http://localhost:8000`
4. Start a new conversation with Claude and ask about Lagoon operations

Example prompts to try:
- "What Lagoon projects are available?"
- "Show me the environments for the project 'example'"
- "How do I deploy the 'main' branch to the 'example' project?"
- "What's the command to SSH into the 'main' environment of 'example' project?"

## For Cursor/Windsurfer IDE Users

### How This Helps Your AI Assistant

AI assistants in IDEs like Cursor and Windsurfer work best when they have access to documentation about the tools you're using. By having this repository in your workspace:

1. **The AI can understand Lagoon commands** - When you ask about Lagoon operations, the AI can reference this documentation
2. **Get accurate command syntax** - The AI can suggest proper command structure and flags
3. **Discover available functionality** - Learn about Lagoon CLI capabilities you might not be aware of
4. **Connect to the MCP server** - AI tools that support MCP can directly perform Lagoon operations

### How to Use

1. Clone this repository into your project workspace:
   ```
   git clone https://github.com/your-username/lagoon-agent.git
   ```

2. Open the project in your AI-enhanced IDE (Cursor, Windsurfer, etc.)

3. Start the MCP server if you want to enable direct Lagoon operations:
   ```
   python mcp_server.py
   ```

4. Now your AI assistant can reference the command documentation when you ask questions like:
   - "How do I list all environments for my project?"
   - "What's the command to deploy a branch?"
   - "How can I run a custom task in Lagoon?"

## Command Documentation

The `lagoon-commands.txt` file contains documentation for Lagoon CLI commands organized into the following sections:

- Installation instructions
- Configuration commands
- Authentication commands
- Project management commands
- Environment management commands
- SSH access commands
- Deployment commands
- Variable management commands
- Tasks and logs commands
- Custom tasks commands
- Backup commands
- Groups and users management commands
- Organization commands
- Lagoon Sync commands

## Keeping Documentation Updated

As Lagoon CLI evolves, this documentation may need updates. To ensure your AI assistant has the most current information:

1. Periodically update this repository with new or changed commands
2. Run `lagoon help` or `lagoon <command> -h` to check for any changes
3. Update the `lagoon-commands.txt` file with any new information

## Resources

- [Official Lagoon Documentation](https://docs.lagoon.sh/)
- [Lagoon CLI GitHub Repository](https://github.com/uselagoon/lagoon-cli)
- [Lagoon Sync GitHub Repository](https://github.com/uselagoon/lagoon-sync)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)

## License

This documentation is provided for educational purposes and to assist with AI tools. 