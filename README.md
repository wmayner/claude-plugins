# claude-plugins

My plugins for Claude, in one marketplace.

| Plugin | What it does |
|---|---|
| `git-workflow` | Skills for git: `/one-commit` commits the work done in the current session, `/logical-commits` splits changes into several commits, `/worktree` starts a task on a new branch in its own worktree, and `/towncrier` writes towncrier news fragments. |
| `vastai` | How to work with remote GPU instances on Vast.ai. |
| `paper-reader` | Turns an arXiv paper or research blog post into a private claude.ai artifact laid out for reading: about 66 characters per line, popovers for citations and footnotes, a contents rail, and font, size and theme settings. arXiv papers convert with a script; it needs [uv](https://docs.astral.sh/uv/). |
| [`prepare-compact`](https://github.com/wmayner/claude-prepare-compact) | Before you compact, Claude writes a handoff note that is loaded right after the summary. |
| [`glance`](https://github.com/wmayner/claude-glance) | Shows what Claude is doing and why, above the prompt. |
| [`iit-expert`](https://github.com/wmayner/iit-expert-plugin) | Answers questions about Integrated Information Theory from its primary literature. |
| [`better-figures`](https://github.com/wmayner/better-figures) | Research figures a busy reader understands at a glance: a plan before drawing, a matplotlib house style with a check on save, worked examples, HTML routes for interactive figures, diagrams and summary figures, and illustrated explainers of how code computes something. |

`prepare-compact`, `glance`, `iit-expert` and `better-figures` are developed in their own repositories; this marketplace points to them.

## Install

On claude.ai or in the Claude desktop app, go to Customize → Plugins → Add → Add marketplace and enter `wmayner/claude-plugins`. Plugins added there are also available in Cowork and in Claude Code sessions signed in to the same account.

In Claude Code alone:

```
/plugin marketplace add wmayner/claude-plugins
/plugin install git-workflow@wmayner
```

## License

MIT
