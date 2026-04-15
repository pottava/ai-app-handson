#!/bin/bash
set -euo pipefail

rm -rf .claude .gemini .geminiignore .mcp.json CLAUDE.md GEMINI.md

rulesync generate --targets claudecode,geminicli --features commands,subagents,skills,hooks,mcp,rules,ignore

echo -e "\nAll post-generation steps completed successfully.\n"
