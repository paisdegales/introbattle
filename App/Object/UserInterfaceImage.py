from App.Object.Image import Image
from App.Object.Object import Object

class UserInterfaceImage(Image):
    def __init__(self, ui_name: str):
        super().__init__("UI", ui_name)

class IntegralUserInterfaceImage(UserInterfaceImage):
    def __init__(self, ui_name: str):
        super().__init__(ui_name)

class AssembledUserInterfaceImage(Object):
    def __init__(self, ui_name: str):
        central_piece = UserInterfaceImage(ui_name)

        left_piece = ui_name.replace(".png", "").strip() + "_left" + ".png"
        left_piece = UserInterfaceImage(left_piece)

        right_piece = ui_name.replace(".png", "").strip() + "_right" + ".png"
        right_piece = UserInterfaceImage(right_piece)

        width = central_piece.rect.width+left_piece.rect.width+right_piece.rect.width
        height = max(central_piece.rect.height, left_piece.rect.height, right_piece.rect.height)
        super().__init__((width,height))

        self.add("left piece", "topleft", left_piece.to_surface(), (0, 0), None)
        self.add("central piece", "topleft", central_piece.to_surface(), (left_piece.rect.width, 0), None)
        self.add("right piece", "topright", right_piece.to_surface(), (width, 0), None)

class ArrowImage(IntegralUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_seta.png")

class MenuImage(IntegralUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_menu.png")

class Ballon1(AssembledUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_balao 1.png")

class Ballon2(AssembledUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_balao 2.png")

class Button(AssembledUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_button.png")

class HealthBar(AssembledUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_hp .png")

class ManaBar(AssembledUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_mp.png")

class StaminaBar(AssembledUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_stamina.png")
