---
allowed-tools: Bash(git add *), Bash(git status*), Bash(git show *), Bash(git commit *), Bash(git reset HEAD *), Bash(git restore --staged *), Bash(git log *), Bash(git diff *), Bash(git branch *), Bash(git stash), Bash(git stash push *), Bash(git stash pop *), Bash(git stash apply *), Bash(git stash list*), Bash(git stash show *), Bash(printf *), Bash(wc *), Bash(ls *)
description: Use when the user asks to break changes into multiple logical git commits, especially via /logical-commits — by default splits only files changed during this session, or all changes if "all" is passed
context: fork
model: sonnet
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -15`

## Rules

- Do NOT chain commands with `&&` — use separate parallel tool calls instead so each matches the allowed-tools patterns.

## Session-only mode (default)

IMPORTANT: By default, *only* commit changes made during this Claude session. Do not include any work that you did not do in this session. To commit everything instead, the user passes "all" as an argument.

You should assume that other agents are concurrently modifying the repo state.

### How to identify session changes

1. Scan the conversation history for every Edit, Write, and NotebookEdit tool call. Collect the file paths and the specific changes made (old_string/new_string for Edit, full content for Write).

2. For each session-modified file, check `git diff HEAD -- <file>` and verify the diff matches what the session's tool calls did.

3. **Clean session files**: If the diff only contains changes from this session's tool calls, `git add <file>`.

4. **Mixed-change files**: If the diff contains additional changes beyond what this session did (from a concurrent agent or pre-existing edits), do NOT stage the file. Report it to the user explaining which changes are from this session and which are not.

5. **Non-session files**: Ignore entirely — do not stage or commit.

If no session-modified files have uncommitted changes, report that and stop.

## Your task

Based on the above changes, create a series of git commits in logical units.

If `$ARGUMENTS` contains "all" or "everything", commit all current changes (ignore session filtering).

$ARGUMENTS
