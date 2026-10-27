---
name: vastai
description: Use when interacting with remote GPU instances on Vast.ai.
---

## Context

- Current instances: !`vastai show instances`

## Working with remote GPUs on Vast.ai

**MANDATORY: Never create, start, stop, or destroy any vast.ai instances without explicit confirmation from the user.** This includes any `vastai` CLI commands or API calls that would affect instance lifecycle (e.g., `vastai create instance`, `vastai start instance`, `vastai stop instance`, `vastai destroy instance`). Always describe the intended action and wait for approval before executing.

**`stop` ≠ `destroy`.** `vastai stop instance` suspends the instance but keeps the disk and image, so it can be resumed with `vastai start instance` later. `vastai destroy instance` is permanent — disk, cached models, and any uncommitted state are wiped. When the user says "stop", use stop; treat "destroy" as a separate, explicit instruction.

**Finding a suitable instance.** Taking into account the minimum requirements for the task, optimize first for cost, then download speed / disk space etc. Be efficient with your choice of instance. Note that efficiency entails anticipating needs beyond this task, to some extent. For example, it's less efficient overall in terms of time and money if we have to port over work to a new instance, re-download models, etc. because we saved a few cents getting an instance that didn't have that much space and subsequently needed more.

**Running remote experiments**: Use `nohup` for overnight or long-running jobs so the experiment survives laptop sleep / SSH drops. Use direct SSH for shorter jobs where you want automatic completion notifications.

```bash
# Overnight / long-running — survives SSH drops, but no auto-notification:
ssh ... 'cd /workspace && nohup python experiment.py > /workspace/experiment.log 2>&1 &'
# Check status manually later:
ssh ... "tail -20 /workspace/experiment.log"

# Shorter jobs — get notified when done, but dies if SSH drops:
ssh ... "cd /workspace && python experiment.py"
# (with run_in_background: true on the Bash tool)
```
When possible, use the Monitor tool to automatically be notified when the task finishes, so you can continue working in the meantime.

When possible, always use a command that will allow the user to see output in stdout in the background/monitor task.
