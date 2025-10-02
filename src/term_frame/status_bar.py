"""Utilities for drawing a simple terminal status bar."""

from __future__ import annotations

import curses
import getpass
import os
import signal
import socket
import time
from types import FrameType
from typing import Mapping, Optional

SSH_ENV_VARS = ("SSH_CONNECTION", "SSH_CLIENT", "SSH_TTY")


def detect_ssh(env: Optional[Mapping[str, str]] = None) -> bool:
    """Return ``True`` when an SSH session is detected.

    Parameters
    ----------
    env:
        Optional mapping of environment variables. Defaults to
        :data:`os.environ` when not provided which allows the function to be
        used directly in production code while remaining testable.
    """

    if env is None:
        environment = os.environ
    else:
        # ``env`` might be mutable (like os.environ) but the protocol we care
        # about is a simple mapping for lookups.
        environment = env

    return any(environment.get(var) for var in SSH_ENV_VARS)


class StatusBarApp:
    """Render a single-line status bar that reflects SSH connectivity."""

    def __init__(self, refresh_interval: float = 0.5) -> None:
        self.refresh_interval = refresh_interval
        self._running = True
        self._user = getpass.getuser()
        self._host = socket.gethostname()
        self._color_enabled = False

    def stop(self) -> None:
        """Request the application to stop."""

        self._running = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Start the curses application."""

        previous_handlers = {}
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                previous_handlers[sig] = signal.getsignal(sig)
                signal.signal(sig, self._handle_signal)
            except (ValueError, AttributeError):  # pragma: no cover - platform
                continue

        try:
            curses.wrapper(self._curses_main)
        finally:
            for sig, handler in previous_handlers.items():
                try:
                    signal.signal(sig, handler)
                except (ValueError, AttributeError):  # pragma: no cover
                    continue

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _handle_signal(self, _signum: int, _frame: Optional[FrameType]) -> None:
        self.stop()

    def _curses_main(self, stdscr) -> None:
        curses.curs_set(0)
        stdscr.nodelay(True)

        if curses.has_colors():
            curses.start_color()
            try:
                curses.use_default_colors()
            except curses.error:
                pass

            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
            self._color_enabled = True

        prev_state: Optional[bool] = None
        prev_size: Optional[tuple[int, int]] = None

        while self._running:
            try:
                key = stdscr.getch()
            except curses.error:
                key = -1

            if key in (ord("q"), ord("Q")):
                self.stop()
                break
            if key == curses.KEY_RESIZE:
                prev_size = None  # Force redraw

            is_ssh = detect_ssh()
            size = stdscr.getmaxyx()

            if is_ssh != prev_state or size != prev_size:
                self._render(stdscr, size[1], is_ssh)
                prev_state = is_ssh
                prev_size = size

            time.sleep(self.refresh_interval)

    def _render(self, stdscr, width: int, is_ssh: bool) -> None:
        indent = 5
        text = f"{self._user}@{self._host}"
        color_pair = 0
        if self._color_enabled:
            color_pair = curses.color_pair(1 if is_ssh else 2)

        try:
            stdscr.attrset(color_pair)
            stdscr.addstr(0, 0, " " * max(0, width))
            stdscr.addnstr(0, indent, text, max(0, width - indent), color_pair)
            stdscr.attrset(0)
        except curses.error:
            pass

        stdscr.refresh()


def main() -> None:
    """Entry point for running the status bar application."""

    app = StatusBarApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    main()
