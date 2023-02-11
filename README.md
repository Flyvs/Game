# README

## GENERAL INFORMATION

- 100% Python code

- The music is made with [beathoven](https://www.beatoven.ai)

## PLAYING

- supports the PS5 Controller and the Nintendo Switch Pro Controller

## EDITING CODE

- There is a line in class "Game" --> function "path" you need to comment out/in (remove comment when converted to an exe and comment when run in editor)

```(hier noch die Zeilennummer angeben, wenn fertig)
parentDirectory = os.path.join(parentDirectory, "game")
```

- remember to install a package to convert the script into an exe (for example [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/))

### CONTROLLER CONFIGS

- PS5 controller configs:

```Controller
BUTTON                  INDEX         FUNCTION
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
Directional-buttons------------------------------------------------------------------
|DIRECTIONAL-UP         |21           |pressed = 1    released = 0
|DIRECTIONAL-DOWN       |22           |pressed = 1    released = 0
|DIRECTIONAL-LEFT       |23           |pressed = 1    released = 0
|DIRECTIONAL-RIGHT      |24           |pressed = 1    released = 0
Sticks-------------------------------------------------------------------------------
|LEFT-STICK-UP/DOWN     | 4           |down = 1       up = -1        range -1 to 1
|LEFT-STICK-LEFT/RIGHT  | 3           |right 1        left = -1      range -1 to 1
|L3                     |17           |pressed = 1    released = 0
|RIGHT-STICK-UP/DOWN    | 6           |down = 1       up = -1        range -1 to 1
|RIGHT-STICK-LEFT/RIGHT | 5           |right = 1      left = -1      range -1 to 1
|R3                     |18           |pressed = 1    released = 0
Bonus-buttons------------------------------------------------------------------------
|CREATE                 |14           |pressed = 1    released = 0
|PS-BUTTON              |15           |pressed = 1    released = 0
|OPTIONS                |16           |pressed = 1    released = 0
|TOUCHPAD               |25           |pressed = 1    released = 0
|MUTE-BUTTON            |26           |pressed = 1    released = 0
```
