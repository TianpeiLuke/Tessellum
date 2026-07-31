---
tags:
  - resource
  - documentation
  - claude_code
  - chrome
  - browser_automation
keywords:
  - claude in chrome
  - browser automation
  - browser tools
  - login state sharing
  - live debugging
  - data extraction
  - claude-in-chrome mcp server
  - example workflows
topics:
  - Claude Code
  - Chrome
language: markdown
date of note: 2026-06-13
status: active
building_block: concept
source_url: https://code.claude.com/docs/en/chrome
access_control_group: ["general"]
---

# Claude Code — Chrome Browser Automation

## Overview

Claude Code integrates with the **Claude in Chrome browser extension** to give browser automation capabilities from the CLI or the VS Code extension: build your code, then test and debug in the browser without switching contexts. Claude opens new tabs for browser tasks and **shares your browser's login state**, so it can access any site you are already signed into. Browser actions run in a visible Chrome window in real time, and when Claude encounters a login page or CAPTCHA, it **pauses and asks you to handle it manually**.

Chrome integration is in beta and currently works with Google Chrome and Microsoft Edge. It is not yet supported on Brave, Arc, or other Chromium-based browsers, and WSL (Windows Subsystem for Linux) is also not supported. This note covers what the integration is and the kinds of workflows it enables; setup, enabling-by-default, and troubleshooting are documented in the sibling procedure note [cc_chrome_setup_and_troubleshooting.md](cc_chrome_setup_and_troubleshooting.md).

## Capabilities

With Chrome connected, you can chain browser actions with coding tasks in a single workflow:

- **Live debugging**: read console errors and DOM state directly, then fix the code that caused them
- **Design verification**: build a UI from a Figma mock, then open it in the browser to verify it matches
- **Web app testing**: test form validation, check for visual regressions, or verify user flows
- **Authenticated web apps**: interact with Google Docs, Gmail, Notion, or any app you're logged into without API connectors
- **Data extraction**: pull structured information from web pages and save it locally
- **Task automation**: automate repetitive browser tasks like data entry, form filling, or multi-site workflows
- **Session recording**: record browser interactions as GIFs to document or share what happened

## Example workflows

These examples show common ways to combine browser actions with coding tasks. Run `/mcp` and select `claude-in-chrome` to see the full list of available browser tools.

### Test a local web application

When developing a web app, ask Claude to verify your changes work correctly:

```text theme={null}
I just updated the login form validation. Can you open localhost:3000,
try submitting the form with invalid data, and check if the error
messages appear correctly?
```

Claude navigates to your local server, interacts with the form, and reports what it observes.

### Debug with console logs

Claude can read console output to help diagnose problems. Tell Claude what patterns to look for rather than asking for all console output, since logs can be verbose:

```text theme={null}
Open the dashboard page and check the console for any errors when
the page loads.
```

Claude reads the console messages and can filter for specific patterns or error types.

### Automate form filling

Speed up repetitive data entry tasks:

```text theme={null}
I have a spreadsheet of customer contacts in contacts.csv. For each row,
go to the CRM at crm.example.com, click "Add Contact", and fill in the
name, email, and phone fields.
```

Claude reads your local file, navigates the web interface, and enters the data for each record.

### Draft content in Google Docs

Use Claude to write directly in your documents without API setup:

```text theme={null}
Draft a project update based on the recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123
```

Claude opens the document, clicks into the editor, and types the content. This works with any web app you're logged into: Gmail, Notion, Sheets, and more.

### Extract data from web pages

Pull structured information from websites:

```text theme={null}
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude navigates to the page, reads the content, and compiles the data into a structured format.

### Run multi-site workflows

Coordinate tasks across multiple websites:

```text theme={null}
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude works across tabs to gather information and complete the workflow.

### Record a demo GIF

To honor the ≤6 verbatim-code-block cap for this note, the seventh workflow is summarized in prose: you can ask Claude to record a GIF of a browser interaction — for example, recording the checkout flow from adding an item to the cart through to the confirmation page. Claude records the interaction sequence and saves it as a GIF file, producing a shareable recording of the browser session.

**Source**: https://code.claude.com/docs/en/chrome
**Last Updated**: 2026-06-13
**Status**: Active
