import pygame

#class controlador:

    #def __init__(self):

pygame.joystick.init()
gamepadsConectados = [pygame.joystick.Joystick(x) for x in 
                      range (pygame.joystick.get_count())]
if len(gamepadsConectados) > 0:
   gamepad = gamepadsConectados[-1]
   gamepad.init()
   print("Id: ",gamepad.get_id())
   print("Name: ",gamepad.get_name())
   print("Num of axes: ",gamepad.get_numaxes())
   print("Num of buttons: ",gamepad.get_numbuttons())
   print("num of hats: ",gamepad.get_numhats())
   print("intancia:",gamepad.get_instance_id())

else:
    print("no hay controles conectados")

##juego = controlador()
#controlador.__init__()