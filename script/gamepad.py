import pygame

 
class Inputs():

    def scan():
        pygame.joystick.init()            
        a = 0
        while a < 2:
            data = []
            dataString = []

            joystick_count = pygame.joystick.get_count()
            data.append(joystick_count)
            dataString.append("Number of joysticks: {}".format(joystick_count))
        
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                #data.append(joystick)
                #dataString.append("Joystick {}".format(i))
        
                name = joystick.get_name()
                data.append(name)
                dataString.append("Joystick name: {}".format(name))
        
                axes = joystick.get_numaxes()
                data.append(axes)
                dataString.append("Number of axes: {}".format(axes))
                
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    data.append(round(axis, 1))
                    dataString.append("Axis {} value: {:>6.3f}".format(i, axis))
        
                buttons = joystick.get_numbuttons()
                data.append(buttons)
                dataString.append("Number of buttons: {}".format(buttons))
        
                for i in range(buttons):
                    button = joystick.get_button(i)
                    data.append(button)
                    dataString.append("Button {:>2} value: {}".format(i, button))
        
                hats = joystick.get_numhats()
                data.append(hats)
                dataString.append("Number of hats: {}".format(hats))
        
                for i in range(hats):
                    hat = joystick.get_hat(i)
                    data.append(hat)
                    dataString.append("Hat {} value: {}".format(i, str(hat)))

            a += 1
        if data[0] == 0:
            data = None
            dataString = None
        return data, dataString