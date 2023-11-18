from types import NotImplementedType
from pygame.rect import Rect
from pygame.draw import rect
from App.Setup.Globals import GRAY, uipath, WHITE
from App.Object.Object import ImportedObject, SizedObject


class UserInterfaceImage(ImportedObject):
    def __init__(self, ui_name: str, ui_filepath: str):
        ui_name = ui_name.replace(".png", "").replace(".jpg", "").replace(".gif", "")
        super().__init__(ui_name, ui_filepath)


class IntegralUserInterfaceImage(UserInterfaceImage):
    def __init__(self, ui_name: str):
        super().__init__(ui_name, uipath(ui_name))


class AssembledUserInterfaceImage(SizedObject):
    def __init__(self, ui_name: str):
        self.central_piece = IntegralUserInterfaceImage(ui_name)

        left_piece = ui_name.replace(".png", "").replace(".png", "").replace(".gif", "").strip() + "_left" + ".png"
        self.left_piece =  IntegralUserInterfaceImage(left_piece)

        right_piece = ui_name.replace(".png", "").replace(".png", "").replace(".gif", "").strip() + "_right" + ".png"
        self.right_piece =  IntegralUserInterfaceImage(right_piece)

        width = self.central_piece.rect.w + self.left_piece.rect.w + self.right_piece.rect.w
        height = max(self.central_piece.rect.h, self.left_piece.rect.h, self.right_piece.rect.h)

        self.left_piece.move("topleft", (0, 0))
        self.central_piece.move("topleft", (self.left_piece.rect.w, 0))
        self.right_piece.move("topright", (width, 0))

        ui_name = ui_name.replace(".png", "").replace(".png", "").replace(".gif", "") + "_complete"
        super().__init__(ui_name, (width,height))

        self.left_piece.draw(self.image)
        self.central_piece.draw(self.image)
        self.right_piece.draw(self.image)


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


class FillingBar(AssembledUserInterfaceImage):
    def __init__(self, ui_name: str, max: int, regen: int):
        super().__init__(ui_name)
        self.scale_by(1.3)
        self.full = self.image.copy()
        self.full.blit(self.image, (0, 0))
        self.max = max
        self.value = max
        self.regen = regen


    def increase(self, value: int) -> Rect:
        if (self.value + value) > self.max:
            return self.fill()

        self.value += value
        percent = self.value / self.max
        width = int(self.rect.w * percent)
        size = width, self.rect.h
        pos = 0, 0
        r = Rect(pos, size)
        changed_area = self.image.blit(self.full, pos, r)
        return changed_area


    def decrease(self, value: int) -> Rect:
        if (self.value - value) <= 0:
            return self.empty()

        self.value -= value
        percent = self.value / self.max
        width = int(self.rect.w * (1 - percent))
        size = width, self.rect.h
        pos = self.rect.w - width, 0
        r = Rect(pos, size)
        changed_area = rect(self.image, GRAY, r, border_top_right_radius=10, border_bottom_right_radius=10)
        return changed_area


    def update(self, value: int) -> Rect:
        if value >= 0:
            return self.increase(value)
        else:
            return self.decrease(-value)


    def fill(self) -> Rect:
        self.value = self.max
        r = self.image.blit(self.full, (0, 0))
        return r


    def empty(self) -> Rect:
        self.value = 0
        r = rect(self.image, GRAY, Rect((0, 0), self.image.get_size()), border_top_right_radius=10, border_bottom_right_radius=10)
        return r



class HealthBar(FillingBar):
    def __init__(self, max: int, regen: int):
        super().__init__("introcomp_hp .png", max, regen)


class ManaBar(FillingBar):
    def __init__(self, max: int, regen: int):
        super().__init__("introcomp_mp.png", max, regen)


class StaminaBar(FillingBar):
    def __init__(self, max: int, regen: int):
        super().__init__("introcomp_stamina.png", max, regen)
