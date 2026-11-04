---
name: todos
description: Use when a deadline, a dated commitment, or a follow-up the user owes someone comes up in conversation, even in passing and even when the request is about something else; when the user asks to add, track, review or tick off a to-do; or when asked what is due. The user's to-dos live in Workflowy, which they often call "wf" ("add that to wf", "what's in wf?").
---

# To-dos in Workflowy

The user keeps every to-do in one place: a top-level Workflowy bullet named `Tasks`. Any session that notices a to-do adds it there, so nothing is left in a repo file or a chat log. "wf" means Workflowy. When the user says "add that to wf" about something to do, it goes in `Tasks`; when it is a note or a reference rather than a task, ask where in the outline it should go.

## Adding

If the conversation contains something the user must do by a date, or a follow-up they owe someone, add it to `Tasks` without asking, then say so in one line, for example "Added to Tasks: Draft the grant report, dated Nov 5." Do this alongside whatever else was asked. If it is unclear whether the item is the user's to do (rather than someone else's, or already done), ask in one line instead.

Before adding, read `Tasks`. If an open to-do already covers the same thing, add nothing; if the new information changes it (a new date, a new source), edit that item and say so.

Make one to-do for each thing the user must finish. A step with its own date, such as a draft due to a reviewer before the final deadline, is a to-do of its own.

Each to-do is built like this:

1. A to-do (`block_format: "todo"`) inside `Tasks`, at the top.
2. Text that starts with a verb and makes sense without the conversation: `Send the revised figures to the editor`.
3. If it has a date: a date tag on the day the user should **act**, and the hard deadline written in the text. If the user named no day to act, choose one that leaves time for the work, and name it in the confirmation line. Example: `Submit the travel reimbursement (due Nov 20) <time startYear="2026" startMonth="11" startDay="17">Nov 17, 2026</time>`
4. One child (`block_format: "bullets"`) giving the source: a link, a file path, a meeting, or the conversation itself (its session link if there is one, otherwise the project and date). Set the format explicitly; an item without one becomes a paragraph.

## Which route to use

- **The `workflowy` MCP tools are available** (`tree_seek`, `tree_patch`; they work only while the Workflowy desktop app is open):
  - Find `Tasks`: `tree_seek` from `"root"`, `direction: "downward-deep"`, `max_match_edge_distance_from_start: 1`, `limit: 5`, `truncate_text_at: 50`, filter `text_matches_any: [{pattern: "^Tasks$"}]`.
  - Read it: `tree_seek` from the `Tasks` id, `max_match_edge_distance_from_start: 1`, `limit: 200`, `truncate_text_at: 300`. The output does not mark completed items. Run the same request again with filter `{completed_after: 0}`: the items it returns are the completed ones, so they are neither open to-dos nor duplicates.
  - Add: `tree_patch` with `{insert_after: <Tasks id>, inside: true, items: [{name, block_format: "todo", children: [{name, block_format: "bullets"}]}]}`. Several items in one request land at the top in the order given.
  - Edit: `{replace: <id>, name: <new text>}`. Complete: `{complete: <id>}`. When a deadline moves, change the text, choose a new day to act, and add a child bullet saying what changed and who said so.
- **The tools exist but calls fail**: the desktop app is probably closed. Say so, and give the finished text as in the next case.
- **No Workflowy tools** (claude.ai, the phone, other machines): give the user the text to paste and the day to tag, for example "Add to Tasks: Submit the travel reimbursement (due Nov 20); tag it Nov 17." Say that you couldn't check `Tasks` for an existing item.

## What a session may change

Inside `Tasks`: add, edit and complete to-dos. Everything else in the outline, including other to-do lists and any move, merge or deletion, is a plan the user approves first. When a to-do is done, complete it; never delete.

## Reviewing what is due

When asked what is due, or what is in wf, read `Tasks` and report the open to-dos in four groups, in this order: overdue, the next 7 days, later, and undated. Group by the date tag (the day to act) and mention the hard deadline from the text. Read dates from the `<time>` tag's `startYear`, `startMonth` and `startDay` attributes.
