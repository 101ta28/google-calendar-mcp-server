# Google Calendar MCP Server

[日本語のREADMEはこちら](README.ja.md)

This document explains the steps to set up the environment to use the Google Calendar API to search calendar contents as an MCP server.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) must be installed.
- A Google account.

## Steps

### 1. Create a Google Cloud Project

Enable the Google Calendar API in the Google Cloud Console or via the link below.

[Enable API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com&hl=en)

### 2. Set Up the OAuth 2.0 Consent Screen

Navigate to the branding page in the Google Cloud Console menu or via the link below.

[Branding](https://console.cloud.google.com/auth/branding?hl=en)

1. Set the application name.
2. Set the user support email.
3. Set the developer contact information.

### 3. Set Up Desktop Application Credentials

Navigate to the client page in the Google Cloud Console menu or via the link below.

[Client](https://console.cloud.google.com/auth/clients?hl=en)

1. Click **Create Credentials**.
2. Click Desktop app under Application type.
3. Enter a name for the credentials in the Name field.
4. Click Create.
5. Save the downloaded JSON file as `credentials.json` and move the file to your working directory.

### 4. Set Up the Python Environment

#### Create a Virtual Environment

1. Open a terminal or command prompt.
2. Navigate to your project directory.
3. Set up the virtual environment and download the required libraries.

   ```sh
   uv sync
   ```

### 5. Configure `calendar_settings.json`

1. Edit the `calendar_settings.json.sample` file in the project directory.

For example, configure it as follows:

```json
{
  "calendar_ids": {
    "primary": "primary",
    "work": "example_work_schedule_id"
  }
}
```

- `primary`: The ID of your Google account's primary calendar (usually "primary").
- `work`: The ID of your work calendar.

Set the necessary calendar IDs, then **rename** the file to `calendar_settings.json` and save it.

### 6. Configure MCP

1. Navigate to the `.vscode` directory within your project directory and edit the `mcp.json.sample` file.
2. Edit the `mcp.json.sample` file as follows:

   ```json
   {
     "servers": {
       "google-calendar-mcp-server": {
         "type": "stdio",
         "command": "/home/<username>/<dir>/.venv/bin/python",
         "args": [
           "/home/<username>/<dir>/google_calendar_mcp_server.py"
         ]
       }
     }
   }
   ```

   - Replace `<username>` with your username.
   - Replace `<dir>` with your project directory name.

   For example, if your username is `tatsuya` and your project directory name is `google-calendar-mcp-server`, the configuration would be:

   ```json
   {
     "servers": {
       "google-calendar-mcp-server": {
         "type": "stdio",
         "command": "/home/tatsuya/google-calendar-mcp-server/.venv/bin/python",
         "args": [
           "/home/tatsuya/google-calendar-mcp-server/google_calendar_mcp_server.py"
         ]
       }
     }
   }
   ```

3. After editing, **rename** the file to `mcp.json` and save it.

### 7. Configure Agent Mode

Follow the steps below to set up Agent Mode for GitHub Copilot Chat in Visual Studio Code.

1. Open Visual Studio Code and navigate to the Extensions view.
2. Search for and install the "GitHub Copilot Chat" extension.
3. Once installed, the "Copilot Chat" icon will appear in the sidebar. Click it to open the Copilot Chat panel.
4. Click the gear icon at the top of the Copilot Chat panel to open the settings.
5. Enable "Agent Mode" in the settings.

### 8. Use MCP

1. Open the Copilot Chat panel.
2. For example, enter a chat such as "List the events for April 8th."
3. A tool execution confirmation will be displayed, click the **Continue** button to execute.
4. On first use, a browser will open requesting permission to access your Google account. Grant the permission.
5. The result will be displayed.

### Troubleshooting

- **If an error occurs**: Check the error message and, if necessary, reinstall dependencies or check the settings in the Google Cloud Console.
