import sys
import threading
import time

try:
    import readline
except ImportError:
    readline = None


class CountdownTimer:
    def __init__(self, duration_seconds, label="Time left", interval_seconds=1):
        self.duration_seconds = duration_seconds
        self.interval_seconds = interval_seconds
        self.label = label
        self.remaining_seconds = duration_seconds
        self._lines_below = 0
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = None
        self._line_created = False

    def start(self, reset=True):
        self.stop()
        if reset:
            with self._lock:
                self.remaining_seconds = self.duration_seconds
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def reset(self):
        """Reset the timer to its configured duration."""
        with self._lock:
            self.remaining_seconds = self.duration_seconds
        if self._line_created:
            self._refresh_timer_line()

    def stop(self):
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join()
        self._thread = None
        self._clear_timer_line()

    def has_time_left(self):
        """Return True if the countdown has remaining time."""
        with self._lock:
            return self.remaining_seconds > 0

    def render(self):
        """Return the current timer text without writing directly to stdout."""
        with self._lock:
            return f"{self.label}: {self.remaining_seconds}s"

    def set_duration(self, seconds):
        """Set the timer duration before starting it."""
        if seconds <= 0:
            raise ValueError("duration_seconds must be positive")
        with self._lock:
            self.duration_seconds = seconds
            if not self._thread or not self._thread.is_alive():
                self.remaining_seconds = seconds

    def set_lines_below(self, lines_below):
        """Set how many lines are below the timer line before the prompt."""
        self._lines_below = max(0, int(lines_below))

    def place(self, lines_below=0):
        """Print the timer line at the current cursor position and register it."""
        self.set_lines_below(lines_below)
        sys.stdout.write(self.render() + "\n")
        sys.stdout.flush()
        self._line_created = True

    def add_time(self, seconds):
        """Add seconds to the remaining countdown time."""
        if seconds <= 0:
            return
        with self._lock:
            self.remaining_seconds += seconds
        self._refresh_timer_line()

    def display(self, force=False):
        """Display the timer line on the terminal and keep it live."""
        if not self._line_created or force:
            self._print_initial_line()
        else:
            self._refresh_timer_line()

    def _run(self):
        while self.remaining_seconds > 0 and not self._stop_event.is_set():
            time.sleep(self.interval_seconds)
            with self._lock:
                self.remaining_seconds -= self.interval_seconds
                if self.remaining_seconds < 0:
                    self.remaining_seconds = 0
            self._refresh_timer_line()

        if not self._stop_event.is_set():
            self._refresh_timer_line(final=True)

    def _print_initial_line(self):
        sys.stdout.write(self.render() + "\n")
        sys.stdout.flush()
        self._line_created = True

    def _refresh_timer_line(self, final=False):
        if not self._line_created:
            return

        timer_text = self.render()
        sys.stdout.write("\x1b[s")
        sys.stdout.write(f"\x1b[{self._lines_below}A")
        sys.stdout.write("\r")
        sys.stdout.write("\x1b[K")
        sys.stdout.write(timer_text)
        sys.stdout.write("\x1b[u")
        sys.stdout.flush()

        if readline is not None:
            try:
                readline.redisplay()
            except Exception:
                pass

    def _clear_timer_line(self):
        if not self._line_created:
            return

        sys.stdout.write("\x1b[s")
        sys.stdout.write(f"\x1b[{self._lines_below}A")
        sys.stdout.write("\r")
        sys.stdout.write("\x1b[K")
        sys.stdout.write("\x1b[u")
        sys.stdout.flush()
        self._line_created = False
