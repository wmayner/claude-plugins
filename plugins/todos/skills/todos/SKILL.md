---
name: todos
description: Use when the user asks to add, track, review or tick off a to-do, or asks what is due; and when something of the kind that goes on a calendar or planner comes up (a deadline, an application, a trip, an appointment, a dated commitment to someone), to offer adding it. The user's to-dos live in Workflowy, which they often call "wf" ("add that to wf", "what's in wf?").
---

# To-dos in Workflowy

The user keeps every to-do in one place: a top-level Workflowy bullet named `Tasks`. "wf" means Workflowy. When the user says "add that to wf" about something to do, it goes in `Tasks`; when it is a note or a reference rather than a task, ask where in the outline it should go.

## Adding

Add a to-do only when the user asks for one. Then confirm in one line, for example "Added to Tasks: draft grant report (Nov 5)."

**Offering.** When the conversation surfaces something the user would put on a calendar or planner, end your reply with a one-line offer, for example "Add to wf: submit travel reimbursement (due nov 20) #admin?" It qualifies if it is something the user has to do, happens outside the current session's work, and is either dated (a deadline, an application, an appointment to make, a trip to arrange, a dated promise to someone) or a substantial undertaking (a talk to prepare, a paper to write). Phrase it as the action: `prepare lab meeting talk (nov 20)`, not `lab meeting talk`. An event that is already arranged, such as a booked flight or a scheduled meeting, belongs on a calendar, not in `Tasks`; offer nothing for it. It does not qualify if it is a step of the task at hand, a code or experiment follow-up, something the session itself will do, or a small chore. Offer each item once; if the user doesn't take it up, drop it. Add nothing without a yes.

Before adding, read `Tasks`. If an open to-do already covers the same thing, add nothing; if the new information changes it (a new date, a new source), edit that item and say so.

Make one to-do for each action the user will perform separately, even when the actions are related. Applying to a conference and changing a flight to attend it are two to-dos. A step with its own date, such as a draft due to a reviewer before the final deadline, is also its own to-do.

Each to-do has up to four parts:

1. **Text**: terse lowercase shorthand, the way a person jots a list: a verb, the object, nothing else. Drop articles, background and explanations. Write `apply to coevolution conference`, `change flight home to dec 7`, `email editor re figures`, not `Apply to the Coevolution Conference (Dec 4–6, Bay Area) and move the flight home`.
2. **Date**, if it has one: the day the user should **act**. A hard deadline that differs from that day goes in the text as `(due nov 20)`. If the user named no day to act, choose one that leaves time for the work, and name it in the confirmation line.
3. **Tags**, so the user can batch similar tasks without nesting. First exactly one for the kind of action: `#reply` (a message to send or answer), `#people` (calls and plans with people), `#read`, `#write` (essays, applications), `#research` (thinking, experiments) or `#admin` (logistics, money, bookings, forms). Then add `#ideas` if it is an idea to think over rather than a commitment, and `#someday` if it is worth keeping but not now. So `#reply`, `#research #ideas`, `#write #someday`. Tags are lowercase, one word each. Make a new tag only when none of these says how the user would group the item, such as a project with several to-dos (`#penobscot` was one). Check the tags already in `Tasks` first, reuse one that fits, and never add a synonym of one (`#idea`, `#email`).
4. **Source**, only when there is one worth opening: the bare link or file path, with no label or commentary.

The connector also records when each to-do was added. Each of the three dates has its own form:

- the day to act is a Workflowy date tag with no time;
- a hard deadline is text: `(due nov 20)`;
- the time added ends the item: the word `added` and a Workflowy date tag with the time, in Pacific time, such as `· added Thu, Nov 5, 2026 at 9:14 PM`. The connector writes it and keeps it when the item is edited; never write it yourself.

Both date tags put the item in Workflowy's calendar and date searches, so a new to-do also shows on the day it was added. When reading the outline directly, the day to act is the date tag without `added` before it.

Older items have one tag and no `added` stamp. Leave them as they are; `list_todos` gives their time added from Workflowy's creation time.

## Which route to use

Use the first that is available.

1. **The Workflowy Tasks connector**: tools named `list_todos`, `add_todo`, `update_todo` and `complete_todo` (in Claude Code the names carry a prefix, such as `mcp__claude_ai_Workflowy_Tasks__add_todo`). It works from every Claude surface and only ever touches `Tasks`. `add_todo` takes `text`, `tags` (a list), `act_by` (`YYYY-MM-DD`) and `source`, and ends the item with the time added. `list_todos` returns `todos`, each with its id, text, tags, date, time added and completed state, leaving completed items out unless asked, and `tags_in_use`, every tag in `Tasks` with how many items carry it; it takes a `tag` to list one kind of task. `update_todo` with `tags` replaces all of an item's tags, so pass the full set; with `act_by: null` it removes a date.
2. **The desktop `workflowy` tools** (`tree_seek`, `tree_patch`; only on a Mac with the Workflowy desktop app open):
   - Find `Tasks`: `tree_seek` from `"root"`, `direction: "downward-deep"`, `max_match_edge_distance_from_start: 1`, `limit: 5`, `truncate_text_at: 50`, filter `text_matches_any: [{pattern: "^Tasks$"}]`.
   - Read it: `tree_seek` from the `Tasks` id, `max_match_edge_distance_from_start: 1`, `limit: 200`, `truncate_text_at: 300`. The output does not mark completed items, so run the same request again with filter `{completed_after: 0}`; the items it returns are the completed ones.
   - Add: `tree_patch` with `{insert_after: <Tasks id>, inside: true, items: [{name, block_format: "todo", children: [{name: <source>, block_format: "bullets"}]}]}`. Write the tags into the name after the text, then the day to act as `<time startYear="2026" startMonth="11" startDay="17">Nov 17, 2026</time>`, then ` · added ` and the time now in Pacific time as `<time startYear="2026" startMonth="11" startDay="5" startHour="21" startMinute="14">Thu, Nov 5, 2026 at 9:14 PM</time>`. When editing a name, keep its `added` stamp unchanged at the end. Set `block_format` explicitly; an item without one becomes a paragraph.
   - Edit: `{replace: <id>, name: <new text>}`. Complete: `{complete: <id>}`.
3. **Tools exist but calls fail**: say so, and fall through to the next case.
4. **No Workflowy tools**: give the user the text to paste and the day to date it, for example "Add to Tasks: submit travel reimbursement (due nov 20) #admin; date it Nov 17." Say that you couldn't check `Tasks` for an existing item.

## What a session may change

Inside `Tasks`: add, edit and complete to-dos. Everything else in the outline, including other to-do lists and any move, merge or deletion, is a plan the user approves first. When a to-do is done, complete it; never delete. When a deadline moves, change the text and choose a new day to act.

## Reviewing what is due

When asked what is due, or what is in wf, read `Tasks` and report the open to-dos in four groups, in this order: overdue, the next 7 days, later, and undated. Group by the date (the day to act) and mention any hard deadline from the text. Leave out `#someday` items unless asked. When the user wants to work through one kind of task ("my replies", "who do I need to call?"), list that tag.
