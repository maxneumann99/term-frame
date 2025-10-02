# term-frame

A lightweight terminal status bar that highlights whether you are working over
SSH. The bar displays your `user@host` information with a red background when
an SSH session is detected and a green background for local sessions.

## Installation

The project uses a standard `src/` layout. Install it into your current Python
environment (preferably a virtual environment) with:

```bash
pip install .
```

For development installs use:

```bash
pip install -e .
```

## Usage

Run the status bar directly as a module:

```bash
python -m term_frame.status_bar
```

Alternatively, invoke the installed console script:

```bash
term-frame-status-bar
```

Press `q` (or `Ctrl+C`) to exit. The bar refreshes automatically to reflect
changes in the SSH connection state.
