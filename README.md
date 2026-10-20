# Expense Tracker MCP Server

A local Model Context Protocol (MCP) server built with **FastMCP** and **SQLite**, designed to let you manage, query, and summarize your personal expenses using natural language through AI chatbot clients like Claude Desktop.

---

## Features

- **Add Expenses**: Record new expenses with date, amount, category, subcategory, and optional notes.
- **List Expenses**: Retrieve and view expense records within an inclusive date range.
- **Summarize**: Aggregate and total expenses grouped by category for specific date ranges.
- **Update & Delete**: Modify or remove existing expense records dynamically by their ID.
- **Category Management**: Enforce and read categories dynamically from a local `categories.json` resource file.
- **MCP Inspector Support**: Test and inspect your tools interactively through the CLI.

---

## Project Structure

```text
expense-tracker-mcp-server/
│
├── src/
│   └── expense_tracker_mcp_server/
│       ├── __init__.py         # Main MCP server implementation & tools
│       └── categories.json     # Dynamic JSON resource file for categories
│
├── pyproject.toml              # Project dependencies and metadata
├── uv.lock                     # Lock file managed by uv
└── README.md                   # Project documentation