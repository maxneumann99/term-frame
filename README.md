# term-frame

Term Frame adds a thin status bar at the top of interactive terminals. The bar
updates on every prompt and highlights SSH sessions in red so you immediately
know when you are working on a remote machine.

## Installation

1. Copy `term_frame.sh` somewhere on your machine (or keep it inside this
   repository).
2. Source it from your `~/.bashrc` (or `~/.bash_profile` on macOS) by adding:

   ```bash
   source /path/to/term_frame.sh
   ```

   The script is safe to source multiple times.

## Behaviour

- When the shell is running inside an SSH session the bar turns red and shows
  `user@host` with a five-space left padding.
- For local sessions the bar turns green with the same information.
- The bar automatically adapts to the terminal width and does not interfere
  with normal prompt usage.

## Compatibility

The script relies on ANSI escape sequences and `tput`. It targets interactive
Bash sessions running in terminals such as `xterm`, `tmux`, `screen`, `rxvt`,
`vt100`, or the Linux console. Non-interactive shells skip the status bar.
