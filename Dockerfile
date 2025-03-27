FROM python:3.11-slim

WORKDIR /app

# Install Lagoon CLI
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://github.com/uselagoon/lagoon-cli/releases/latest/download/lagoon-cli-linux-amd64 -o /usr/local/bin/lagoon \
    && chmod +x /usr/local/bin/lagoon

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY mcp_server.py .
COPY lagoon-commands.txt .

# Expose the default MCP port
EXPOSE 8000

# Run the MCP server
CMD ["python", "mcp_server.py"] 