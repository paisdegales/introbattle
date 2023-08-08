from App.Object.Image import Image

class UserInterfaceImage(Image):
    def __init__(self, ui_name: str):
        super().__init__("UI", ui_name)

class IntegralUserInterfaceImage(UserInterfaceImage):
    def __init__(self, ui_name: str):
        super().__init__(ui_name)

class AssembledUserInterfaceImage(UserInterfaceImage):
    def __init__(self, ui_name: str):
        raise NotImplementedError()

class ArrowImage(IntegralUserInterfaceImage):
    def __init__(self):
        super().__init__("introcomp_seta.png")
