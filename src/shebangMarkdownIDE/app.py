from __future__ import annotations

import sys
import subprocess
import shlex
import re
from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Header,
    Footer,
    Label,
    Tree,
    TabbedContent,
    TabPane,
    TextArea,
    Markdown,
    Static,
    Input,
)


class MarkdownIDE(App):
    """
    Terminal-based Markdown editor/mini-IDE by Aryaneel Shivam.

    Layout:
    - Header
    - Status bar
    - Main area:
        - Left: File explorer + Command terminal
        - Right: Tabbed editor (TextArea + Markdown preview)
    - Footer (shows keybindings)
    """

    TITLE = "Shebang Markdown"

    CSS = """
    Screen {
        layout: vertical;
    }

    #status-bar {
        height: 1;
        padding: 0 1;
        background: $surface;
        text-style: bold;
    }

    #main {
        layout: horizontal;
        height: 1fr;
    }

    #sidebar {
        width: 30%;
        border: round $accent;
    }

    #explorer-title, #command-title {
        padding: 0 1;
        text-style: bold;
    }

    #file_tree {
        height: 1fr;
    }

    /* File type highlighting - using Rich markup in labels */
    /* .md files are cyan, .txt files are green via label markup */

    #command-section {
        height: 15;
        border-top: heavy $primary;
    }

    #command-input {
        height: 3;
        border: round $accent;
    }

    #command-output-scroll {
        height: 1fr;
        border: round $secondary;
    }

    #command-output {
        width: 1fr;
    }

    #editor-panel {
        width: 1fr;
        border: round $secondary;
    }

    #tabs {
        height: 1fr;
    }

    .editor-layout {
        layout: horizontal;
        height: 1fr;
    }

    .editor-text {
        width: 2fr;
        border-right: round $accent;
    }

    VerticalScroll.preview {
        width: 1fr;
        height: 1fr;
        padding: 1;
    }

    Markdown.preview {
        width: 100%;
    }

    #lint-panel {
        height: 8;
        border-top: heavy $warning;
    }

    .lint-error {
        color: $error;
    }

    .lint-warning {
        color: $warning;
    }

    /* Theme: Dark (default) */
    .theme-dark {
        background: $background;
    }

    /* Theme: Light */
    .theme-light {
        background: #ffffff;
    }
    .theme-light #status-bar {
        background: #f0f0f0;
        color: #000000;
    }
    .theme-light #sidebar {
        border: round #4a90e2;
        background: #fafafa;
    }
    .theme-light #command-section {
        border-top: heavy #4a90e2;
    }
    .theme-light #command-input {
        border: round #4a90e2;
        background: #ffffff;
    }
    .theme-light #command-output-scroll {
        border: round #888888;
        background: #ffffff;
    }
    .theme-light #editor-panel {
        border: round #888888;
        background: #ffffff;
    }
    .theme-light .editor-text {
        border-right: round #4a90e2;
        background: #ffffff;
    }

    /* Theme: Blue */
    .theme-blue {
        background: #1e3a5f;
    }
    .theme-blue #status-bar {
        background: #2d4a6b;
        color: #e0e8f0;
    }
    .theme-blue #sidebar {
        border: round #5a9fd4;
        background: #253d5a;
    }
    .theme-blue #command-section {
        border-top: heavy #5a9fd4;
    }
    .theme-blue #command-input {
        border: round #5a9fd4;
        background: #2d4a6b;
    }
    .theme-blue #command-output-scroll {
        border: round #4a7ba0;
        background: #253d5a;
    }
    .theme-blue #editor-panel {
        border: round #4a7ba0;
        background: #253d5a;
    }
    .theme-blue .editor-text {
        border-right: round #5a9fd4;
        background: #1e3a5f;
    }

    /* Theme: Green */
    .theme-green {
        background: #1f3d2e;
    }
    .theme-green #status-bar {
        background: #2d4f3d;
        color: #d0e8d8;
    }
    .theme-green #sidebar {
        border: round #5abf7f;
        background: #253d2e;
    }
    .theme-green #command-section {
        border-top: heavy #5abf7f;
    }
    .theme-green #command-input {
        border: round #5abf7f;
        background: #2d4f3d;
    }
    .theme-green #command-output-scroll {
        border: round #4a9f6f;
        background: #253d2e;
    }
    .theme-green #editor-panel {
        border: round #4a9f6f;
        background: #253d2e;
    }
    .theme-green .editor-text {
        border-right: round #5abf7f;
        background: #1f3d2e;
    }

    /* Theme: Purple */
    .theme-purple {
        background: #2d1f3d;
    }
    .theme-purple #status-bar {
        background: #3d2f4d;
        color: #e8d0f0;
    }
    .theme-purple #sidebar {
        border: round #9f7fbf;
        background: #2d253d;
    }
    .theme-purple #command-section {
        border-top: heavy #9f7fbf;
    }
    .theme-purple #command-input {
        border: round #9f7fbf;
        background: #3d2f4d;
    }
    .theme-purple #command-output-scroll {
        border: round #7f5f9f;
        background: #2d253d;
    }
    .theme-purple #editor-panel {
        border: round #7f5f9f;
        background: #2d253d;
    }
    .theme-purple .editor-text {
        border-right: round #9f7fbf;
        background: #2d1f3d;
    }

    /* Theme: Orange */
    .theme-orange {
        background: #3d2f1f;
    }
    .theme-orange #status-bar {
        background: #4d3f2f;
        color: #f0e8d0;
    }
    .theme-orange #sidebar {
        border: round #df9f5f;
        background: #3d352f;
    }
    .theme-orange #command-section {
        border-top: heavy #df9f5f;
    }
    .theme-orange #command-input {
        border: round #df9f5f;
        background: #4d3f2f;
    }
    .theme-orange #command-output-scroll {
        border: round #bf7f4f;
        background: #3d352f;
    }
    .theme-orange #editor-panel {
        border: round #bf7f4f;
        background: #3d352f;
    }
    .theme-orange .editor-text {
        border-right: round #df9f5f;
        background: #3d2f1f;
    }
    """

    BINDINGS = [
        ("ctrl+n", "new_file", "New file"),
        ("ctrl+o", "open_from_tree", "Open selected file"),
        ("ctrl+s", "save", "Save file"),
        ("ctrl+w", "close_tab", "Close tab"),
        ("ctrl+h", "show_markdown_reference", "Show Markdown reference"),
        ("ctrl+l", "show_lint_issues", "Show lint issues"),
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+enter", "execute_command", "Execute command"),
    ]

    def __init__(self, root_path: str | None = None) -> None:
        super().__init__()
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.current_working_dir = self.root_path  # Track current directory for commands

        # editor_id -> Path
        self.editor_files: dict[str, Path] = {}
        # editor_id -> modified flag
        self.modified: dict[str, bool] = {}
        
        # Linting: editor_id -> list of lint issues
        self.lint_issues: dict[str, list] = {}

    # ---------- Compose UI ----------

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("Ready", id="status-bar")

        with Horizontal(id="main"):
            # Sidebar: file explorer + command terminal
            with Vertical(id="sidebar"):
                yield Static("📁 Explorer", id="explorer-title")
                self.file_tree = Tree(str(self.root_path), id="file_tree")
                yield self.file_tree

                yield Static("🛠️  Command Terminal", id="command-title")
                with Vertical(id="command-section"):
                    self.command_input = Input(
                        placeholder="Enter shell command (e.g., mkdir test, touch file.md, ls -la)...",
                        id="command-input"
                    )
                    yield self.command_input
                    with VerticalScroll(id="command-output-scroll"):
                        self.command_output = Static("", id="command-output", markup=True)
                        yield self.command_output

            # Editor + preview area with tabs
            with Vertical(id="editor-panel"):
                self.tabs = TabbedContent(id="tabs")
                yield self.tabs

        yield Footer()

    # ---------- Lifecycle ----------

    def _create_markdown_reference_tab(self) -> None:
        """Create a tab with Markdown syntax reference."""
        markdown_cheat_sheet = r"""# Markdown Syntax Reference

## Headers
```
# H1
## H2
### H3
#### H4
##### H5
###### H6
```

## Emphasis
```
*italic* or _italic_
**bold** or __bold__
***bold italic*** or ___bold italic___
~~strikethrough~~
```

## Lists

### Unordered
```
- Item 1
- Item 2
  - Nested item
  - Another nested item
```

### Ordered
```
1. First item
2. Second item
3. Third item
```

## Links
```
[Link text](https://example.com)
[Link with title](https://example.com "Title")
```

## Images
```
![Alt text](image.jpg)
![Alt text](image.jpg "Image title")
```

## Code

### Inline code
```
Use `backticks` for inline code
```

### Code blocks
````
```python
def hello():
    print("Hello, World!")
```
````

## Blockquotes
```
> This is a blockquote
> It can span multiple lines
> > And be nested
```

## Horizontal Rule
```
---
***
___
```

## Tables
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

## Task Lists
```
- [x] Completed task
- [ ] Incomplete task
```

## Escaping
```
Use backslash \ to escape special characters:
\*not italic\*
\#not a header
```

## Line Breaks
```
End a line with two spaces  
to create a line break.
```

## HTML
```
You can use <b>HTML</b> tags directly.
```

## Mermaid Diagrams

Mermaid diagrams are supported! Use code blocks with `mermaid` language:

### Flowchart
````
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```
````

### Sequence Diagram
````
```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello Bob!
    B-->>A: Hello Alice!
```
````

### Gantt Chart
````
```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Task 1 :a1, 2024-01-01, 30d
    Task 2 :a2, after a1, 20d
```
````

### Class Diagram
````
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +eat()
    }
    class Dog {
        +bark()
    }
    Animal <|-- Dog
```
````

### State Diagram
````
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Running: Start
    Running --> Idle: Stop
    Running --> Paused: Pause
    Paused --> Running: Resume
```
````

## Math (LaTeX)

Mathematical expressions using LaTeX syntax:

### Inline Math
```
Use $E = mc^2$ for inline math.
```

### Block Math
```
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

### Examples
```
The quadratic formula: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

Euler's identity: $e^{i\pi} + 1 = 0$

Summation: $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$

Matrix:
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$
```

---
*Tip: Use Ctrl+S to save your markdown files!*
*Note: Mermaid diagrams and math render in the preview. Export to HTML/PDF for full rendering.*
"""
        
        # Create the reference tab
        reference_text = TextArea(
            text=markdown_cheat_sheet,
            id="markdown_reference_editor",
            language="markdown",
            read_only=True,
            classes="editor-text",
        )
        reference_preview = Markdown(markdown_cheat_sheet, classes="preview")
        preview_scroll = VerticalScroll(reference_preview, classes="preview")
        
        reference_content = Horizontal(reference_text, preview_scroll, classes="editor-layout")
        reference_pane = TabPane("📖 Markdown Reference", reference_content, id="markdown_reference_pane")
        
        # Add as the first tab
        self.tabs.add_pane(reference_pane)
        # Don't set it as active by default - let user files be active

    def on_mount(self) -> None:
        """Populate file tree and maybe open a default file."""
        self._build_file_tree(self.root_path, self.file_tree.root)
        self.file_tree.root.expand()
        self._set_status("Markdown IDE ready. Ctrl+N: New file  Ctrl+O: Open from tree  Ctrl+H: Markdown reference.")
        self._append_command_output("Markdown IDE started. Use command terminal to run shell commands.")
        
        # Create markdown reference tab
        self._create_markdown_reference_tab()

        # If user passed a file path on CLI, open it
        if len(sys.argv) > 1:
            initial = Path(sys.argv[1]).expanduser().resolve()
            if initial.is_file():
                self.open_file(initial)

    # ---------- Helpers ----------

    def _build_file_tree(self, base: Path, node) -> None:
        """Recursively build a simple file tree."""
        try:
            for entry in sorted(base.iterdir()):
                if entry.name.startswith("."):
                    continue  # skip dotfiles/dirs
                if entry.is_dir():
                    # Color directories/folders
                    child = node.add(f"[yellow bold]{entry.name}[/yellow bold]", expand=False)
                    child.data = entry
                    self._build_file_tree(entry, child)
                else:
                    # Add file with extension-based styling
                    child = node.add(entry.name)
                    child.data = entry
                    # Store extension for styling
                    ext = entry.suffix.lower()
                    if ext == '.md':
                        child.label = f"[cyan]{entry.name}[/cyan]"
                    elif ext == '.txt':
                        child.label = f"[green]{entry.name}[/green]"
        except PermissionError:
            pass

    def _refresh_file_tree_for_path(self, path: Path) -> None:
        """Refresh the file tree to show a newly created/saved file."""
        if not path.exists():
            return
        
        # Find the directory node that contains this file
        target_dir = path.parent.resolve()
        
        # If the file is in the root directory, refresh root
        if target_dir == self.root_path:
            # Clear and rebuild root children
            self.file_tree.root.remove_children()
            self._build_file_tree(self.root_path, self.file_tree.root)
            return
        
        # Otherwise, find the directory node in the tree
        def find_dir_node(node, target: Path):
            """Recursively find the node for a given directory path."""
            if hasattr(node, 'data') and node.data == target:
                return node
            for child in node.children:
                if hasattr(child, 'data') and isinstance(child.data, Path) and child.data.is_dir():
                    result = find_dir_node(child, target)
                    if result:
                        return result
            return None
        
        dir_node = find_dir_node(self.file_tree.root, target_dir)
        if dir_node:
            # Clear children and rebuild this directory
            dir_node.remove_children()
            self._build_file_tree(target_dir, dir_node)
            # Expand to show the new file
            dir_node.expand()

    def _set_status(self, text: str) -> None:
        status = self.query_one("#status-bar", Label)
        status.update(text)

    def _highlight_shell_keywords(self, text: str) -> str:
        """Highlight shell keywords in the text using Rich markup."""
        # Shell command keywords to highlight
        keywords = [
            'mkdir', 'cd', 'touch', 'ls', 'rm', 'mv', 'cp', 'cat', 'echo',
            'grep', 'find', 'chmod', 'chown', 'pwd', 'which', 'whereis',
            'tar', 'zip', 'unzip', 'git', 'python', 'python3', 'node',
            'npm', 'pip', 'pip3', 'export', 'alias', 'source', 'exec',
            'sudo', 'su', 'exit', 'clear', 'history', 'man', 'help'
        ]
        
        # Create a pattern that matches whole words only
        pattern = r'\b(' + '|'.join(re.escape(kw) for kw in keywords) + r')\b'
        
        # Replace keywords with highlighted version using Rich markup
        # Using cyan color for keywords
        highlighted = re.sub(
            pattern,
            lambda m: f'[cyan bold]{m.group(1)}[/cyan bold]',
            text,
            flags=re.IGNORECASE
        )
        
        # Also highlight common patterns
        # Highlight command prompts: $ 
        highlighted = re.sub(r'(\$\s+)', r'[yellow]\1[/yellow]', highlighted)
        # Highlight error tags: [error]
        highlighted = re.sub(r'(\[error\])', r'[red bold]\1[/red bold]', highlighted)
        # Highlight success tags: [success]
        highlighted = re.sub(r'(\[success\])', r'[green bold]\1[/green bold]', highlighted)
        # Highlight warning tags: [warning]
        highlighted = re.sub(r'(\[warning\])', r'[yellow bold]\1[/yellow bold]', highlighted)
        # Highlight stderr tags: [stderr]
        highlighted = re.sub(r'(\[stderr\])', r'[red]\1[/red]', highlighted)
        # Highlight cwd tags: [cwd:]
        highlighted = re.sub(r'(\[cwd:\s*[^\]]+\])', r'[blue]\1[/blue]', highlighted)
        # Highlight exit code tags: [exit code:]
        highlighted = re.sub(r'(\[exit code:\s*\d+\])', r'[magenta]\1[/magenta]', highlighted)
        
        return highlighted

    def _lint_markdown(self, editor_id: str, text: str) -> None:
        """Lint markdown content and store issues."""
        issues = []
        lines = text.split('\n')
        
        # Check for common markdown issues
        for i, line in enumerate(lines, 1):
            # Check for headers without blank line after
            if i < len(lines) and line.startswith('#'):
                next_line = lines[i] if i < len(lines) else ""
                if next_line and not next_line.strip() == "" and not next_line.startswith('#'):
                    issues.append({
                        'line': i + 1,
                        'type': 'warning',
                        'message': f"Consider adding blank line after header at line {i}"
                    })
            
            # Check for inconsistent heading levels (skip first few lines)
            if line.startswith('#') and i > 3:
                level = len(line) - len(line.lstrip('#'))
                if level > 6:
                    issues.append({
                        'line': i,
                        'type': 'error',
                        'message': f"Invalid heading level {level} at line {i} (max is 6)"
                    })
            
            # Check for broken links [text](url) format
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            matches = re.finditer(link_pattern, line)
            for match in matches:
                url = match.group(2)
                if url.strip() == "":
                    issues.append({
                        'line': i,
                        'type': 'error',
                        'message': f"Empty link URL at line {i}: {match.group(0)}"
                    })
            
            # Check for images without alt text
            img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
            img_matches = re.finditer(img_pattern, line)
            for match in img_matches:
                alt_text = match.group(1)
                if not alt_text or alt_text.strip() == "":
                    issues.append({
                        'line': i,
                        'type': 'warning',
                        'message': f"Image without alt text at line {i} (accessibility issue)"
                    })
            
            # Check for table formatting issues
            if '|' in line and not line.strip().startswith('|'):
                # Table row that doesn't start with |
                if i > 1 and '|' in lines[i-2] if i > 1 else False:
                    issues.append({
                        'line': i,
                        'type': 'warning',
                        'message': f"Table row at line {i} should start with |"
                    })
        
        # Check for missing blank lines around code blocks
        in_code_block = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if not in_code_block and i < len(lines):
                    next_line = lines[i] if i < len(lines) else ""
                    if next_line and not next_line.strip() == "":
                        issues.append({
                            'line': i + 1,
                            'type': 'warning',
                            'message': f"Consider adding blank line after code block at line {i}"
                        })
        
        # Store issues
        self.lint_issues[editor_id] = issues
        
        # Update status bar with lint info
        if issues:
            errors = sum(1 for issue in issues if issue['type'] == 'error')
            warnings = sum(1 for issue in issues if issue['type'] == 'warning')
            if errors > 0:
                self._set_status(f"Lint: {errors} error(s), {warnings} warning(s) | Press Ctrl+L for details")
            else:
                self._set_status(f"Lint: {warnings} warning(s) | Press Ctrl+L for details")
        else:
            # Only update if we're on this editor
            current_editor = self._active_editor_id()
            if current_editor == editor_id:
                # Don't overwrite status if there are no issues
                pass

    def _append_command_output(self, message: str) -> None:
        """Append message to command output area with syntax highlighting."""
        # Highlight keywords in the message
        highlighted_message = self._highlight_shell_keywords(message)
        
        # Get current text from Static widget
        current_text = ""
        if hasattr(self.command_output, 'renderable'):
            # Try to get text from renderable
            try:
                current_text = str(self.command_output.renderable)
            except:
                pass
        
        # If we can't get it from renderable, try to track it ourselves
        if not hasattr(self, '_command_output_text'):
            self._command_output_text = ""
        
        # Append the highlighted message
        if self._command_output_text:
            self._command_output_text = f"{self._command_output_text}\n{highlighted_message}"
        else:
            self._command_output_text = highlighted_message
        
        # Update the Static widget with the new text
        self.command_output.update(self._command_output_text)

    def _execute_shell_command(self, command: str) -> None:
        """Execute a shell command and display output."""
        if not command.strip():
            return
        
        # Handle cd command specially to track current directory
        command_stripped = command.strip()
        if command_stripped.startswith("cd "):
            target_dir = command_stripped[3:].strip()
            if not target_dir:
                # cd without arguments goes to home, but we'll go to root_path
                self.current_working_dir = self.root_path
            elif target_dir == "..":
                # Go up one directory, but don't go above root_path
                parent = self.current_working_dir.parent
                if parent.resolve() != self.root_path.resolve() and self.root_path.resolve() in parent.resolve().parents:
                    self.current_working_dir = parent
                elif parent.resolve() == self.root_path.resolve():
                    self.current_working_dir = self.root_path
                else:
                    # Don't go above root_path
                    self.current_working_dir = self.root_path
            else:
                # Change to specified directory
                target_path = (self.current_working_dir / target_dir).resolve()
                # Ensure we don't go outside root_path
                if target_path.exists() and target_path.is_dir():
                    if self.root_path.resolve() in target_path.resolve().parents or target_path.resolve() == self.root_path.resolve():
                        self.current_working_dir = target_path
                    else:
                        self._append_command_output(f"$ {command}")
                        self._append_command_output("[error]Cannot change directory outside root path")
                        return
                else:
                    self._append_command_output(f"$ {command}")
                    self._append_command_output(f"[error]Directory not found: {target_dir}")
                    return
            
            # Show the command and new directory
            self._append_command_output(f"$ {command}")
            self._append_command_output(f"[cwd: {self.current_working_dir}]")
            return
        
        # Show the command being executed
        self._append_command_output(f"$ {command}")
        
        try:
            # Use current_working_dir for commands
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.current_working_dir),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout:
                self._append_command_output(result.stdout)
            if result.stderr:
                self._append_command_output(f"[stderr]\n{result.stderr}")
            if result.returncode != 0:
                self._append_command_output(f"[exit code: {result.returncode}]")
            else:
                self._append_command_output("[success]")
            
            # Refresh file tree if command might have changed files
            if any(cmd in command.lower() for cmd in ['mkdir', 'touch', 'rm', 'mv', 'cp', 'create', 'delete', 'rename']):
                # Refresh the entire tree by rebuilding root
                self.file_tree.root.remove_children()
                self._build_file_tree(self.root_path, self.file_tree.root)
                
        except subprocess.TimeoutExpired:
            self._append_command_output("[error]Command timed out after 10 seconds")
        except Exception as e:
            self._append_command_output(f"[error]Failed to execute command: {e}")

    def _current_editor_and_preview(self) -> tuple[TextArea | None, Markdown | None]:
        """Return the active TextArea and Markdown, if any."""
        pane = self.tabs.active_pane
        if pane is None:
            return None, None
        editor = pane.query_one("TextArea")
        preview = pane.query_one("Markdown")
        return editor, preview

    def _active_editor_id(self) -> str | None:
        editor, _ = self._current_editor_and_preview()
        return editor.id if editor else None

    def _update_status_for_editor(self, editor_id: str | None) -> None:
        if editor_id is None:
            self._set_status("No file open.")
            return

        path = self.editor_files.get(editor_id)
        star = "*" if self.modified.get(editor_id, False) else ""
        file_name = path.name if path else "untitled.md"
        self._set_status(
            f"{file_name}{star}  |  Ctrl+N: New  Ctrl+O: Open  Ctrl+S: Save  Ctrl+W: Close tab  Ctrl+H: Help  Ctrl+L: Lint  Ctrl+Enter: Execute  Ctrl+Q: Quit"
        )

    # ---------- File / tab management ----------

    def open_file(self, path: Path) -> None:
        """Open a file in a new tab, or focus if already open."""
        path = path.resolve()

        # Check if already open
        for editor_id, p in self.editor_files.items():
            if p == path:
                # Focus that tab
                for pane in self.tabs.query("TabPane"):
                    editor = pane.query_one("TextArea")
                    if editor.id == editor_id:
                        self.tabs.active = pane.id
                        self._update_status_for_editor(editor_id)
                        self._append_command_output(f"Focused already-open file: {path}")
                        return

        # Create new tab
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            self._append_command_output(f"[error]Failed to open {path}: {e}")
            self._set_status(f"Failed to open {path.name}")
            return

        # Warn if file is not a markdown file
        if path.suffix.lower() != ".md":
            self._append_command_output(f"[warning]Opened non-markdown file: {path.name} (extension: {path.suffix or 'none'})")

        editor_id = f"editor_{len(self.editor_files) + 1}"
        pane_id = f"pane_{len(self.editor_files) + 1}"

        file_title = path.name

        editor = TextArea(
            text=text,
            id=editor_id,
            language="markdown",
            classes="editor-text",
        )
        preview = Markdown(text, classes="preview")
        preview_scroll = VerticalScroll(preview, classes="preview")

        content = Horizontal(editor, preview_scroll, classes="editor-layout")

        pane = TabPane(file_title, content, id=pane_id)
        self.tabs.add_pane(pane)
        self.tabs.active = pane.id

        self.editor_files[editor_id] = path
        self.modified[editor_id] = False
        self._update_status_for_editor(editor_id)
        self._append_command_output(f"Opened {path}")

    def create_new_file(self) -> None:
        """Create a new empty file in a new tab."""
        editor_id = f"editor_{len(self.editor_files) + 1}"
        pane_id = f"pane_{len(self.editor_files) + 1}"

        # Generate a unique untitled filename
        untitled_count = sum(1 for p in self.editor_files.values() if p and p.name.startswith("untitled"))
        if untitled_count > 0:
            file_title = f"untitled{untitled_count + 1}.md"
        else:
            file_title = "untitled.md"

        editor = TextArea(
            text="",
            id=editor_id,
            language="markdown",
            classes="editor-text",
        )
        preview = Markdown("", classes="preview")
        preview_scroll = VerticalScroll(preview, classes="preview")

        content = Horizontal(editor, preview_scroll, classes="editor-layout")

        pane = TabPane(file_title, content, id=pane_id)
        self.tabs.add_pane(pane)
        self.tabs.active = pane.id

        # New file has no path yet (will be set on first save)
        self.editor_files[editor_id] = None
        self.modified[editor_id] = True  # New file is considered modified
        self._update_status_for_editor(editor_id)
        self._append_command_output(f"Created new file: {file_title}")
        
        # Run initial linting
        self._lint_markdown(editor_id, "")

    def save_current(self) -> None:
        editor, preview = self._current_editor_and_preview()
        if not editor:
            self._set_status("No file to save.")
            return

        editor_id = editor.id
        path = self.editor_files.get(editor_id)

        if path is None:
            path = Path("untitled.md").resolve()
            self.editor_files[editor_id] = path

        try:
            path.write_text(editor.text, encoding="utf-8")
        except Exception as e:
            self._append_command_output(f"[error]Failed to save {path}: {e}")
            self._set_status(f"Failed to save {path.name}")
            return

        self.modified[editor_id] = False
        self._update_status_for_editor(editor_id)
        self._append_command_output(f"Saved {path}")
        
        # Refresh file tree to show the new/updated file
        self._refresh_file_tree_for_path(path)

    def close_current_tab(self) -> None:
        """Close the active tab."""
        editor, _ = self._current_editor_and_preview()
        if not editor:
            return
        editor_id = editor.id

        # Remove pane
        pane = self.tabs.active_pane
        if pane:
            self.tabs.remove_pane(pane.id)
            self._append_command_output(f"Closed tab for {self.editor_files.get(editor_id, 'unknown')}")

        # Cleanup maps
        self.editor_files.pop(editor_id, None)
        self.modified.pop(editor_id, None)

        # Update status
        self._update_status_for_editor(self._active_editor_id())

    # ---------- Actions (keybindings) ----------

    def action_open_from_tree(self) -> None:
        """Open the currently selected file in the tree."""
        node = self.file_tree.cursor_node
        if not node or not hasattr(node, "data"):
            self._set_status("No file selected in explorer.")
            return

        path = node.data
        if isinstance(path, Path) and path.is_file():
            self.open_file(path)
        else:
            node.expand()
            self._set_status("Expanded folder.")

    def action_new_file(self) -> None:
        self.create_new_file()

    def action_save(self) -> None:
        self.save_current()

    def action_close_tab(self) -> None:
        self.close_current_tab()

    def action_execute_command(self) -> None:
        """Execute the command in the command input."""
        command = self.command_input.value
        if command.strip():
            self._execute_shell_command(command)
            self.command_input.value = ""  # Clear input after execution

    def action_show_markdown_reference(self) -> None:
        """Show or recreate the Markdown reference tab."""
        # Check if the reference tab already exists
        reference_pane = None
        for pane in self.tabs.query("TabPane"):
            if pane.id == "markdown_reference_pane":
                reference_pane = pane
                break
        
        if reference_pane:
            # Tab exists, just switch to it
            self.tabs.active = reference_pane.id
        else:
            # Tab doesn't exist, recreate it
            self._create_markdown_reference_tab()
            # Switch to the newly created tab
            for pane in self.tabs.query("TabPane"):
                if pane.id == "markdown_reference_pane":
                    self.tabs.active = pane.id
                    break

    def action_show_lint_issues(self) -> None:
        """Show lint issues for the current editor."""
        editor_id = self._active_editor_id()
        if not editor_id:
            self._set_status("No file open for linting.")
            return
        
        issues = self.lint_issues.get(editor_id, [])
        if not issues:
            self._append_command_output("[lint] No issues found! ✓")
            self._set_status("Lint: No issues found")
            return
        
        # Show issues in command output
        self._append_command_output(f"[lint] Found {len(issues)} issue(s):")
        for issue in issues[:10]:  # Show first 10 issues
            issue_type = issue['type'].upper()
            line_num = issue['line']
            message = issue['message']
            if issue_type == 'ERROR':
                self._append_command_output(f"[error]Line {line_num}: {message}")
            else:
                self._append_command_output(f"[warning]Line {line_num}: {message}")
        
        if len(issues) > 10:
            self._append_command_output(f"[lint] ... and {len(issues) - 10} more issue(s)")
        
        errors = sum(1 for issue in issues if issue['type'] == 'error')
        warnings = sum(1 for issue in issues if issue['type'] == 'warning')
        self._set_status(f"Lint: {errors} error(s), {warnings} warning(s) | See command output")

    def action_quit(self) -> None:
        self.exit()

    # ---------- Events ----------

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """When user hits Enter on a node, try open file or expand dir."""
        node = event.node
        path = getattr(node, "data", None)
        if isinstance(path, Path) and path.is_file():
            self.open_file(path)
        else:
            node.expand()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Update modified flag and live preview on text change."""
        editor = event.text_area
        editor_id = editor.id

        if editor_id not in self.editor_files:
            # Might be some other TextArea; ignore
            return

        self.modified[editor_id] = True
        self._update_status_for_editor(editor_id)

        # Update preview for this pane
        pane = self.tabs.active_pane
        if not pane:
            return
        preview = pane.query_one("Markdown")
        preview.update(editor.text)
        
        # Run linting on markdown content
        self._lint_markdown(editor_id, editor.text)

    def on_tabbed_content_tab_activated(
        self, event: TabbedContent.TabActivated
    ) -> None:
        """Update status when switching tabs."""
        self._update_status_for_editor(self._active_editor_id())

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command input submission."""
        if event.input.id == "command-input":
            self.action_execute_command()


def run_app(root_path: str | None = None) -> None:
    """Run the Markdown IDE application."""
    app = MarkdownIDE(root_path)
    # Set initial terminal size: (columns, rows)
    # Default: 120 columns x 40 rows
    app.run(size=(150, 50))


if __name__ == "__main__":
    # Optional: pass a starting file: python markdown_ide.py notes.md
    run_app()