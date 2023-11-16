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
    def __init__(self, ui_name: str):
        super().__init__(ui_name)
        self.scale_by(1.3)
        self.full = self.image.copy()
        self.full.blit(self.image, (0, 0))
        self.percent = 1


    def update(self, percent: float) -> Rect:
        """ decreases/increases the bar by how much it's filled
            
            Parameters:
                percent: how much the fillbar is filled

            Return: Rect
                the area of the filling bar's surface that has changed """

        if percent > 1:
            raise Exception("'update' method of FillingBar got something other than a percentage lesser than 1")

        if percent < 0:
            percent = 0

        self.percent = percent
        width = int(self.rect.w * (1 - percent))
        size = width, self.rect.h
        pos = self.rect.w - width, 0
        r = Rect(pos, size)
        changed_area = rect(self.image, GRAY, r, border_top_right_radius=10, border_bottom_right_radius=10)
        return changed_area


    def restore(self) -> None:
        self.percent = 1
        self.image = self.full.copy()
        self.image.blit(self.full, (0, 0))


class HealthBar(FillingBar):
    def __init__(self):
        super().__init__("introcomp_hp .png")


class ManaBar(FillingBar):
    def __init__(self):
        super().__init__("introcomp_mp.png")


class StaminaBar(FillingBar):
    def __init__(self):
        super().__init__("introcomp_stamina.png")
