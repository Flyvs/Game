# README

## GENERAL INFORMATION

- 100% Python code (it's not good)

- **DO _NOT_ DELETE THE .key FILES** (or any other files lol but those are essential)

- The music is mostly made with [beathoven](https://www.beatoven.ai)

- Also a track is taken from [here](https://youtu.be/tgIddOrtMFQ)

## PLAYING

- supports keyboard and most controllers but the PS5 Controller and the Nintendo Switch Pro Controller work best

## EDITING CODE

- remember to install a package to convert the script into an exe (for example [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/))

Set this to true if you want to export the script as an exe.

```
Game.export = False
```

### FUNCTIONS

#### gamepad.py

returns a list with the buttons a controller has:

```
Inputs.scan()[0]
```

returns a list with controller details

```
Inputs.scan()[1]
```

#### crypting.py

encrypts the given file and creates a key with the given name

```
Crypting.encrypt(path: str, fileToEncrypt: str, filekeyName: str)
```

decrypts the given file and uses the given key(file)

```
Crypting.decrypt(path: str, fileToDecrypt: str, filekeyName: str)
```

renames a file (idk why I created this (There is [os.rename](https://www.tutorialspoint.com/python/os_rename.htm)), maybe there's a reason why but I can't remember)

```
Crypting.rename(path: str, oldName: str, newName: str)
```

#### pygame_merge.py

merges multiple surfaces & the last surface given will be on top

```
Merge.surfaces(path: str, *surfaces: pygame.Surface)
```

#### expandlist.py

expands a list with multiple values and returns it

```
Expandlist.expand(list: list, *values)
```

### CONTROLLER CONFIGS

Technically works with every controller.
However, the index changes depending on which controller you plug in and use.
If you don't want to use a PS5 or Nintendo Switch Pro Controller you have to figure out the index yourself.

#### PS5 CONTROLLER

```
BUTTON                  INDEX         FUNCTIONALITY
Action-buttons----------------------------------------------------------------------
|X                      |10           |pressed = 1    released = 0
|O                      |11           |pressed = 1    released = 0
|□                      |12           |pressed = 1    released = 0
|▲                      |13           |pressed = 1    released = 0
Back-buttons------------------------------------------------------------------------
|L1                     |19           |pressed = 1    released = 0
|R1                     |20           |pressed = 1    released = 0
|L2                     | 7           |pressed = 1    released = -1  range -1 to 1
|R2                     | 8           |pressed = 1    released = -1  range -1 to 1
Directional-buttons-----------------------------------------------------------------
|UP                     |21           |pressed = 1    released = 0
|DOWN                   |22           |pressed = 1    released = 0
|LEFT                   |23           |pressed = 1    released = 0
|RIGHT                  |24           |pressed = 1    released = 0
Sticks------------------------------------------------------------------------------
|LEFT-STICK-UP/DOWN     | 4           |down = 1       up = -1        range -1 to 1
|LEFT-STICK-LEFT/RIGHT  | 3           |right 1        left = -1      range -1 to 1
|L3                     |17           |pressed = 1    released = 0
|RIGHT-STICK-UP/DOWN    | 6           |down = 1       up = -1        range -1 to 1
|RIGHT-STICK-LEFT/RIGHT | 5           |right = 1      left = -1      range -1 to 1
|R3                     |18           |pressed = 1    released = 0
Bonus-buttons-----------------------------------------------------------------------
|CREATE                 |14           |pressed = 1    released = 0
|PS-BUTTON              |15           |pressed = 1    released = 0
|OPTIONS                |16           |pressed = 1    released = 0
|TOUCHPAD               |25           |pressed = 1    released = 0
|MUTE-BUTTON            |26           |pressed = 1    released = 0
```

#### NINTENDO SWITCH PRO CONTROLLER

```
BUTTON                  INDEX         FUNCTIONALITY
Action-buttons----------------------------------------------------------------------
|A                      |10           |pressed = 1    released = 0
|B                      |11           |pressed = 1    released = 0
|X                      |12           |pressed = 1    released = 0
|Y                      |13           |pressed = 1    released = 0
Back-buttons------------------------------------------------------------------------
|L1                     |19           |pressed = 1    released = 0
|R1                     |20           |pressed = 1    released = 0
|L2                     | 7           |pressed = 1    released = -1  range -1 to 1
|R2                     | 8           |pressed = 1    released = -1  range -1 to 1
Control-Pad-------------------------------------------------------------------------
|UP                     |21           |pressed = 1    released = 0
|DOWN                   |22           |pressed = 1    released = 0
|LEFT                   |23           |pressed = 1    released = 0
|RIGHT                  |24           |pressed = 1    released = 0
Sticks------------------------------------------------------------------------------
|LEFT-STICK-UP/DOWN     | 4           |down = 1       up = -1        range -1 to 1
|LEFT-STICK-LEFT/RIGHT  | 3           |right 1        left = -1      range -1 to 1
|L3                     |17           |pressed = 1    released = 0
|RIGHT-STICK-UP/DOWN    | 6           |down = 1       up = -1        range -1 to 1
|RIGHT-STICK-LEFT/RIGHT | 5           |right = 1      left = -1      range -1 to 1
|R3                     |18           |pressed = 1    released = 0
Bonus-buttons-----------------------------------------------------------------------
|MINUS                  |14           |pressed = 1    released = 0
|HOME                   |15           |pressed = 1    released = 0
|PLUS                   |16           |pressed = 1    released = 0
|CAPTURE                |25           |pressed = 1    released = 0
```
