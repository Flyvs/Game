import pygame

 
class Inputs():

    def scan():
        """
        PS5:
        X:                     10,   pressed = 1, released = 0
        O:                     11,   pressed = 1, released = 0
        □:                     12,   pressed = 1, released = 0
        ▲:                     13,   pressed = 1, released = 0
        L1:                    19,   pressed = 1, released = 0
        R1:                    20,   pressed = 1, released = 0
        L2:                     7, range -1 to 1, pressed 1, released -1
        R2:                     8, range -1 to 1, pressed 1, released -1
        CREATE:                14,   pressed = 1, released = 0
        PS-BUTTON:             15,   pressed = 1, released = 0
        OPTIONS:               16,   pressed = 1, released = 0
        TOUCHPAD:              25,   pressed = 1, released = 0
        DIRECTIONAL-UP:        21,   pressed = 1, released = 0
        DIRECTIONAL-DOWN:      22,   pressed = 1, released = 0
        DIRECTIONAL-LEFT:      23,   pressed = 1, released = 0
        DIRECTIONAL-RIGHT:     24,   pressed = 1, released = 0
        LEFT-STICK-UP/DOWN:     4, range -1 to 1, down 1, up -1
        LEFT-STICK-LEFT/RIGHT:  3, range -1 to 1, right 1, left -1
        L3:                    17,   pressed = 1, released = 0
        RIGHT-STICK-UP/DOWN:    6, range -1 to 1, down 1, up -1
        RIGHT-STICK-LEFT/RIGHT: 5, range -1 to 1, right 1, left -1
        R3:                    18,   pressed = 1, released = 0
        MUTE-BUTTON:           26,   pressed = 1, released = 0
        """
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
                    data.append(axis)
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
        return data, dataString