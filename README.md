# TreeNotes

A tool to interact with your markdown notes like one large tree. 

Very early on / WIP. Project started in [bs7280/Alfred-Note-Capture](https://github.com/bs7280/Alfred-Note-Capture) as a macos workflow tool, but moving core code to this repo.

Heavily inspired by dendron and applied towards my obsidian notes.

Features (planned or implemented):
- Search for notes by filename and header with a glob pattern
- Insert notes into a 'node' 
- Refactor a large note into sub notes

Future features:
- Combine notes by a glob pattern
    - `$Daily:##Bookmarks` > a list of all bookmarks with annotation
    - can be fed into other search featuers like a RAG model to find that bookmark I was thinking of
        - bonus -> scrape the page too
- Append `vscode.shortcuts:## Run tests hotkey`
    - Refernce these shortcuts easily with above detail
- TUI support more UI options than alfred can
    - Append / insert note - link or autocomplete another note
- bulk merge links to note tree

## CLI
`python src/cli.py search '*python*'`

```
Search pattern: *python*
--------------------------------------------------------------------------------
code.python.lib.pandas.md
code.python.lib.os.md
code.python.lib.jupyter.md
code.python.lib.fastapi.snippet-generate-docs.md
prj.python-map-plotting.marketing.md
code.python.snippets.logstash-scroll-api.md
code.python.lib.dask.md
prj.python-map-plotting.streamlit.md
```

## TUI

![TUI Example - Search for notes](images/readme_tui_example.png)