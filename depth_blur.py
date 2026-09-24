import pygame


class DepthBlur:
    """Applies distance-based blur to a group of decorative space objects.

    Smaller objects (assumed farther away) get blurred more; bigger objects
    (assumed closer) stay sharper. When two objects overlap on screen, the
    bigger one (treated as being in front) is always kept sharper than the
    one it's covering, regardless of what the size-based formula alone
    would have produced.
    """

    def __init__(self, max_blur=3, min_blur=0, overlap_margin=1):
        self.max_blur = max_blur
        self.min_blur = min_blur
        self.overlap_margin = overlap_margin
        self._cache = {}   # (image id, blur level) -> blurred surface

    def _blur_surface(self, surface, strength):
        """Downscale then upscale — a cheap, fast blur approximation."""
        if strength <= 0:
            return surface

        w, h = surface.get_size()
        if w < 2 or h < 2:
            return surface

        shrink = 1 + strength
        small_size = (max(1, int(w / shrink)), max(1, int(h / shrink)))

        small = pygame.transform.smoothscale(surface, small_size)
        return pygame.transform.smoothscale(small, (w, h))

    def _get_blurred(self, obj, strength):
        
        is_rotating = getattr(obj, "rotation_speed", 0) != 0

        if is_rotating:
            # Never cache — id() can be reused across frames for short-lived
            # rotated surfaces, causing stale/glitchy blur results.
            return obj.image

        rounded = round(strength, 1)
        if rounded <= 0:
            return obj.image


        key = (id(obj.image), rounded)
        if key in self._cache:
            return self._cache[key]

        blurred = self._blur_surface(obj.image, rounded)
        self._cache[key] = blurred
        return blurred

    def _object_size(self, obj):
        """Use the object's ORIGINAL (unrotated) size to judge distance,
        so a spinning object's growing/shrinking bounding box never
        makes its blur flicker."""
        source = getattr(obj, "original_image", obj.image)
        w, h = source.get_size()
        return w * h

    def apply(self, screen, objects):
        objects = list(objects)
        if not objects:
            return

        sizes = [self._object_size(obj) for obj in objects]
        min_size, max_size = min(sizes), max(sizes)
        size_range = max_size - min_size

        blur_values = {}
        for obj, size in zip(objects, sizes):
            if size_range == 0:
                blur_values[obj] = self.min_blur
                continue
            distance_ratio = 1 - ((size - min_size) / size_range)
            blur_values[obj] = self.min_blur + distance_ratio * (self.max_blur - self.min_blur)

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                a, b = objects[i], objects[j]
                if not a.rect.colliderect(b.rect):
                    continue
                size_a, size_b = self._object_size(a), self._object_size(b)
                front, back = (a, b) if size_a >= size_b else (b, a)
                if blur_values[front] > blur_values[back] - self.overlap_margin:
                    blur_values[front] = max(self.min_blur, blur_values[back] - self.overlap_margin)

    
        for obj in objects:
            image_to_draw = self._get_blurred(obj, blur_values[obj])
            screen.blit(image_to_draw, obj.rect)