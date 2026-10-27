---
name: worktree
description: Use when starting any task that should happen on a new branch in an isolated git worktree, especially when invoked as /worktree — creates a sensibly-named worktree first, then handles the rest of the prompt exactly as normal
---

## What this skill does

This skill adds **exactly one** behavior to your normal handling of the user's prompt: before changing any files, create a git worktree to isolate the work.

After the worktree exists, treat the prompt below **exactly as you would have without this skill** — same mode, same approach, same level of detail, same questions, same use of other skills. Do not turn this into a worktree-themed response. The worktree is just scaffolding; the real task is the user's prompt.

## Steps

### 1. Pick a sensible branch name

Read the user's prompt below and choose a short, kebab-case branch name that summarizes the work (e.g. `fix-auth-redirect`, `add-csv-export`, `refactor-payment-flow`, `investigate-flaky-tests`).

- Keep it under ~5 words.
- If the prompt explicitly names a branch, use that name verbatim.
- If the prompt is so vague that no sensible name exists, ask the user for one — but only in that case.

### 2. Create the worktree

Invoke the `superpowers:using-git-worktrees` skill via the Skill tool to do the actual creation. It handles directory selection, gitignore safety, setup, and baseline verification.

If that skill isn't available, fall back to this minimal procedure:

- Pick a directory: `.worktrees/` if it exists, else `worktrees/` if it exists, else ask the user.
- For project-local directories, verify they're gitignored (`git check-ignore -q <dir>`); if not, add to `.gitignore` and commit before proceeding.
- `git worktree add <dir>/<branch-name> -b <branch-name>`
- `cd` into the new worktree.

### 3. Handle the user's prompt as normal

Once the worktree exists and you're inside it, process `$ARGUMENTS` as if the user had just typed it without `/worktree`. Don't summarize what you're about to do unless the prompt itself would have warranted it. Don't prepend extra worktree-related commentary beyond whatever `using-git-worktrees` already announces.

## Plan mode

If you're in plan mode, you can't create the worktree yet — but the **first step of your plan must be** "create a git worktree named `<chosen-name>`". Don't omit it just because plan mode is read-only. After ExitPlanMode, the worktree creation runs first, then the rest of the plan.

## Don'ts

- Don't restrict tools, change verbosity, or switch modes because of this skill.
- Don't ask for confirmation of the branch name unless the prompt is genuinely ambiguous.
- Don't create the worktree *after* editing files. The whole point is isolation before changes.
- Don't treat this as a worktree-management task. The user's real task is in `$ARGUMENTS`.

## User's prompt

$ARGUMENTS
