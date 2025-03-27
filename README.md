# Lagoon CLI Commands Reference

This repository contains reference documentation for Lagoon CLI commands to help AI assistants in Cursor, Windsurfer, and other AI-enhanced IDEs better understand and assist with Lagoon operations.

## Overview

[Lagoon](https://lagoon.sh/) is a Docker-based infrastructure management system that helps developers build, deploy, and manage containerized applications. The Lagoon CLI provides a command-line interface for interacting with Lagoon instances.

This repository provides:
- A comprehensive reference of Lagoon CLI commands (`lagoon-commands.txt`)
- Easy-to-access documentation for AI tools to reference

## For Cursor/Windsurfer IDE Users

### How This Helps Your AI Assistant

AI assistants in IDEs like Cursor and Windsurfer work best when they have access to documentation about the tools you're using. By having this repository in your workspace:

1. **The AI can understand Lagoon commands** - When you ask about Lagoon operations, the AI can reference this documentation
2. **Get accurate command syntax** - The AI can suggest proper command structure and flags
3. **Discover available functionality** - Learn about Lagoon CLI capabilities you might not be aware of

### How to Use

1. Clone this repository into your project workspace:
   ```
   git clone https://github.com/rashed-k/lagoon-cli-commands-examples.git
   ```

2. Open the project in your AI-enhanced IDE (Cursor, Windsurfer, etc.)

3. Now your AI assistant can reference the command documentation when you ask questions like:
   - "How do I list all environments for my project?"
   - "What's the command to deploy a branch?"
   - "How can I run a custom task in Lagoon?"

4. The AI will use the documentation in `lagoon-commands.txt` to provide accurate answers.

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

## Contributing

If you discover new commands or features not documented here, please feel free to:

1. Update the `lagoon-commands.txt` file
2. Create a pull request to share with the community

## Resources

- [Official Lagoon Documentation](https://docs.lagoon.sh/)
- [Lagoon CLI GitHub Repository](https://github.com/uselagoon/lagoon-cli)
- [Lagoon Sync GitHub Repository](https://github.com/uselagoon/lagoon-sync)

## License

This documentation is provided for educational purposes and to assist with AI tools. 