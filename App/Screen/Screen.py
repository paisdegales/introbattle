from pygame.display import init, get_init, set_mode, list_modes, set_caption
from pygame.event import get as get_events
from pygame.surface import Surface
from logging import warning

class Screen:
    """
        Class responsible for creating/managing the user's display screen.
    """

    def __init__(self) -> None:
        if not get_init():
            init()
        set_caption("Introbattle")

    def new_display(self, display_resolution: tuple[int, int], flags: int = 0) -> Surface:
        available_displays = list_modes()
        # creates a window with max proportions if the desired display is not available
        surf =  set_mode(size=display_resolution, flags=flags) \
                if display_resolution in available_displays \
                else set_mode(flags=flags)

        return surf
