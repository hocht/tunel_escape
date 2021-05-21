import pygame

class controlador:
    """ crea un objeto controlador y lo inicializa"""
    def __init__(self):
        """detecta los gamepads conectados y crea uno para iniciarlo"""
        pygame.joystick.init()
        gamepadsConectados = [pygame.joystick.Joystick(x) for x in 
                            range (pygame.joystick.get_count())]
        if len(gamepadsConectados) > 0:
            self.gamepad = gamepadsConectados[-1]
            self.gamepad.init()
            print("Id: ",self.gamepad.get_id())
            print("Name: ",self.gamepad.get_name())
            print("Num of axes: ",self.gamepad.get_numaxes())
            print("Num of buttons: ",self.gamepad.get_numbuttons())
            print("num of hats: ",self.gamepad.get_numhats())
        else:
            print("no hay controles conectados")