---
name: todos
description: Use when a deadline, a dated commitment, or a follow-up the user owes someone comes up in conversation, even in passing and even when the request is about something else; when the user asks to add, track, review or tick off a to-do; or when asked what is due. The user's to-dos live in Workflowy, which they often call "wf" ("add that to wf", "what's in wf?").
---

# To-dos in Workflowy

The user keeps every to-do in one place: a top-level Workflowy bullet named `Tasks`. Any session that notices a to-do adds it there, so nothing is left in a repo file or a chat log. "wf" means Workflowy. When the user says "add that to wf" about something to do, it goes in `Tasks`; when it is a note or a reference rather than a task, ask where in the outline it should go.

## Adding

If the conversation contains something the user must do by a date, or a follow-up they owe someone, add it to `Tasks` without asking, then say so in one line, for example "Added to Tasks: draft grant report (Nov 5)." Do this alongside whatever else was asked. If it is unclear whether the item is the user's to do (rather than someone else's, or already done), ask in one line instead.

Before adding, read `Tasks`. If an open to-do already covers the same thing, add nothing; if the new information changes it (a new date, a new source), edit that item and say so.

Make one to-do for each action the user will perform separately, even when the actions are related. Applying to a conference and changing a flight to attend it are two to-dos. A step with its own date, such as a draft due to a reviewer before the final deadline, is also its own to-do.

Each to-do is built like this:

1. A to-do (`block_format: "todo"`) inside `Tasks`, at the top.
2. Terse lowercase shorthand, the way a person jots a list: a verb, the object, nothing else. Drop articles, background and explanations. Write `apply to coevolution conference`, `change flight home to dec 7`, `email editor re figures`, not `Apply to the Coevolution Conference (Dec 4–6, Bay Area) and move the flight home`.
3. If it has a date: a date tag on the day the user should **act**. A hard deadline that differs from that day goes in the text as `(due nov 20)`. If the user named no day to act, choose one that leaves time for the work, and name it in the confirmation line. Example: `submit travel reimbursement (due nov 20) <time startYear="2026" startMonth="11" startDay="17">Nov 17, 2026</time>`
4. A child bullet (`block_format: "bullets"`) only when there is a source worth opening: the bare link or file path, with no label or commentary. Set the format explicitly; an item without one becomes a paragraph.

## Which route to use

- **The `workflowy` MCP tools are available** (`tree_seek`, `tree_patch`; they work only while the Workflowy desktop app is open):
  - Find `Tasks`: `tree_seek` from `"root"`, `direction: "downward-deep"`, `max_match_edge_distance_from_start: 1`, `limit: 5`, `truncate_text_at: 50`, filter `text_matches_any: [{pattern: "^Tasks$"}]`.
  - Read it: `tree_seek` from the `Tasks` id, `max_match_edge_distance_from_start: 1`, `limit: 200`, `truncate_text_at: 300`. The output does not mark completed items. Run the same request again with filter `{completed_after: 0}`: the items it returns are the completed ones, so they are neither open to-dos nor duplicates.
  - Add: `tree_patch` with `{insert_after: <Tasks id>, inside: true, items: [{name, block_format: "todo", children: [{name, block_format: "bullets"}]}]}`. Several items in one request land at the top in the order given.
  - Edit: `{replace: <id>, name: <new text>}`. Complete: `{complete: <id>}`. When a deadline moves, change the text and choose a new day to act.
- **The tools exist but calls fail**: the desktop app is probably closed. Say so, and give the finished text as in the next case.
- **No Workflowy tools** (claude.ai, the phone, other machines): give the user the text to paste and the day to tag, for example "Add to Tasks: submit travel reimbursement (due nov 20); tag it Nov 17." Say that you couldn't check `Tasks` for an existing item.

## What a session may change

Inside `Tasks`: add, edit and complete to-dos. Everything else in the outline, including other to-do lists and any move, merge or deletion, is a plan the user approves first. When a to-do is done, complete it; never delete.

## Reviewing what is due

When asked what is due, or what is in wf, read `Tasks` and report the open to-dos in four groups, in this order: overdue, the next 7 days, later, and undated. Group by the date tag (the day to act) and mention the hard deadline from the text. Read dates from the `<time>` tag's `startYear`, `startMonth` and `startDay` attributes.
