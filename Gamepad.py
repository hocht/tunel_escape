import pygame

#class controlador:

    #def __init__(self):

pygame.joystick.init()
gamepadsConectados = [pygame.joystick.Joystick(x) for x in 
                      range (pygame.joystick.get_count())]
if len(gamepadsConectados) > 0:
   gamepad = gamepadsConectados[-1]
   gamepad.init()
   print(gamepad.get_id())
   print(gamepad.get_name())
   print(gamepad.get_numaxes())
   print(gamepad.get_numbuttons())
   print(gamepad.get_numhats())

else:
    print("no hay controles conectados")

##juego = controlador()
#controlador.__init__()