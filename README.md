# Shebang Markdown IDE

A powerful, terminal-based Markdown IDE built with [Textual](https://textual.textualize.io/) by **Aryaneel Shivam**. Write, preview, and manage your Markdown files directly in your terminal with a beautiful, keyboard-first interface.

## About

Shebang Markdown IDE is a full-featured Markdown editor that runs entirely in your terminal. It combines the power of a modern IDE with the simplicity and speed of terminal-based tools. Whether you're writing documentation, taking notes, or creating technical content, this IDE provides everything you need without leaving your terminal.

## Features

### ✨ Core Features

- **Live Markdown Preview**: See your rendered Markdown in real-time as you type, side-by-side with your editor
- **Multi-Tab Editing**: Open and edit multiple Markdown files simultaneously with tabbed interface
- **File Explorer**: Navigate your project directory with an integrated file tree
- **Integrated Command Terminal**: Execute shell commands directly within the IDE without switching windows
- **Markdown Linting**: Real-time linting with error and warning detection for better code quality
- **Markdown Reference Guide**: Built-in comprehensive Markdown syntax reference accessible via keyboard shortcut
- **Syntax Highlighting**: Beautiful syntax highlighting for Markdown code blocks
- **File Type Detection**: Visual distinction for different file types (`.md` files in cyan, `.txt` files in green)

### 🎨 User Interface

- **Clean Terminal UI**: Modern, responsive interface built with Textual
- **Status Bar**: Real-time status updates showing current file, lint issues, and helpful hints
- **Keyboard-First Design**: All operations accessible via keyboard shortcuts
- **Multiple Themes**: Support for dark, light, blue, green, purple, and orange color themes
- **Rich Text Formatting**: Color-coded file explorer and syntax-highlighted command output

### 📝 Markdown Support

- **Standard Markdown**: Full support for CommonMark specification
- **Extended Syntax**:
  - Tables
  - Task lists
  - Strikethrough
  - Code blocks with syntax highlighting
  - Blockquotes
  - Horizontal rules
- **Mermaid Diagrams**: Support for flowcharts, sequence diagrams, Gantt charts, class diagrams, and state diagrams
- **LaTeX Math**: Inline and block mathematical expressions using LaTeX syntax
- **HTML Support**: Direct HTML tag support in Markdown

### 🔧 Command Terminal Features

- **Shell Command Execution**: Run any shell command directly from the IDE
- **Directory Navigation**: Built-in `cd` command support with directory tracking
- **Command History**: View command output in scrollable terminal area
- **Syntax Highlighting**: Shell keywords and commands are highlighted in output
- **Auto File Tree Refresh**: File tree automatically updates after file operations
- **Working Directory Tracking**: Commands execute in the current working directory
- **Error Handling**: Clear error messages and exit code display

### 🔍 Linting Features

The built-in linter checks for:

- **Header Issues**: Missing blank lines after headers, invalid heading levels (>6)
- **Link Validation**: Empty link URLs, broken link syntax
- **Image Accessibility**: Missing alt text for images
- **Table Formatting**: Table row formatting issues
- **Code Block Formatting**: Missing blank lines around code blocks
- **Real-time Feedback**: Linting runs automatically as you type
- **Issue Reporting**: View detailed lint issues with line numbers and error types

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Create a new file |
| `Ctrl+O` | Open selected file from explorer |
| `Ctrl+S` | Save current file |
| `Ctrl+W` | Close current tab |
| `Ctrl+H` | Show Markdown reference guide |
| `Ctrl+L` | Show lint issues for current file |
| `Ctrl+Enter` | Execute command in terminal |
| `Ctrl+Q` | Quit application |

### 🎯 File Management

- **Create New Files**: Quick file creation with auto-generated untitled names
- **Open Files**: Open files from file explorer or via command line argument
- **Save Files**: Save with visual indicator for unsaved changes (asterisk in status bar)
- **File Tree Navigation**: Expand/collapse directories, navigate with arrow keys
- **Auto-Refresh**: File tree automatically refreshes after file operations

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/aryaneelshivam/shebangMarkdownIDE.git
cd shebangMarkdownIDE
```

2. Install in editable mode:
```bash
pip install -e .
```

3. Run the application:
```bash
devcanvas
```

Or run directly:
```bash
python -m shebangMarkdownIDE.cli
```

### From PyPI (when available)

```bash
pip install shebangmarkdown
devcanvas
```

## Usage

### Basic Usage

1. **Start the IDE**:
   ```bash
   devcanvas
   ```

2. **Open a specific file**:
   ```bash
   devcanvas path/to/file.md
   ```

3. **Navigate**:
   - Use the file explorer on the left to browse your project
   - Press `Enter` on a file to open it
   - Use `Ctrl+O` to open the currently selected file

4. **Edit**:
   - Type in the editor (left side of the tab)
   - See live preview on the right side
   - Save with `Ctrl+S`

5. **Use Command Terminal**:
   - Type commands in the command input at the bottom of the sidebar
   - Press `Ctrl+Enter` or `Enter` to execute
   - View output in the scrollable command output area

### Command Terminal Examples

```bash
# Create a new directory
mkdir docs

# Create a new file
touch notes.md

# List files
ls -la

# Change directory
cd docs

# Run Python script
python script.py

# Git operations
git status
git add .
```

### Markdown Reference

Press `Ctrl+H` to open the built-in Markdown reference guide, which includes:
- All standard Markdown syntax
- Mermaid diagram examples
- LaTeX math examples
- Best practices and tips

### Linting

- Linting runs automatically as you type
- View lint status in the status bar
- Press `Ctrl+L` to see detailed lint issues
- Issues are categorized as errors or warnings with line numbers

## Requirements

- Python 3.10 or higher
- Textual >= 0.58.0

## Project Structure

```
shebang_dist/
├── src/
│   └── shebangMarkdownIDE/
│       ├── __init__.py
│       ├── app.py          # Main application
│       └── cli.py          # CLI entry point
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Development

### Building the Package

```bash
python -m build
```

### Running Tests

```bash
# Add tests as needed
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Author

**Aryaneel Shivam**
- Email: aryaneelshivam1234@gmail.com

## Acknowledgments

- Built with [Textual](https://textual.textualize.io/) - The TUI framework for Python
- Inspired by modern terminal-based editors and IDEs

---

**Note**: This is an actively developed project. Features may be added or changed in future versions.
