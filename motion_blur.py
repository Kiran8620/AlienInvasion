import pygame
from collections import deque


class MotionBlur:
    """Keeps a short history of an object's recent image/position and
    draws them as a fading trail behind the object's current frame."""

    def __init__(self, trail_length=5, max_alpha=120):
        """
        trail_length: how many past frames to remember (longer = longer trail)
        max_alpha: opacity of the most recent trail frame (0-255).
                   Older frames fade toward 0 automatically.
        """
        self.trail_length = trail_length
        self.max_alpha = max_alpha
        self.history = deque(maxlen=trail_length)

    def record(self, image, rect):
        """Call once per frame, after the object's image/rect have been
        updated, to store a snapshot for the trail."""
        self.history.append((image.copy(), rect.copy()))

    def draw(self, screen):
        """Draw the stored trail, oldest (dimmest) first. Does NOT draw
        the object's current frame — the caller still draws that separately."""
        history_list = list(self.history)
        history_count = len(history_list)
        if history_count <= 1:
            return   # nothing to trail yet

        # Skip the most recent snapshot — that's essentially the current
        # frame, which the object itself will draw on top.
        for i, (image, rect) in enumerate(history_list[:-1]):
            # Older snapshots (lower i) get more fade; newer ones are more visible.
            fade_progress = (i + 1) / history_count
            alpha = int(self.max_alpha * fade_progress)

            faded_image = image.copy()
            faded_image.set_alpha(alpha)
            screen.blit(faded_image, rect)

    def clear(self):
        """Reset the trail, e.g. when an object respawns."""
        self.history.clear()