"""
class Item(pygame.sprite.Sprite):
    # initializing
    def __init__(self, pos, group):
        super().__init__(group)

        Item.hitted = False
        Item.path = Game.path("sprites", "items")

        Item.allItems = []
        if Game.itemSpawned == False:
            Item.image = pygame.image.load(Item.path + Item.randomSpawn()).convert_alpha()
            Item.rect = Item.image.get_rect(topleft=pos)
            Game.itemSpawned = True

    # spawning a specific item
    def spawn(item: str):
        for file in os.listdir(Item.path):
            casefoldFile = file[:-4].casefold()
            item = item.casefold()
            if casefoldFile == item:
                return file

    # spawning a random item
    def randomSpawn():
        for file in os.listdir(Item.path):
            Item.allItems.append(file)
        if Game.itemSpawned == False:
            Game.whichItem = random.randint(0, len(Item.allItems) - 1)
            Game.itemSpawned = True
        return str(Item.allItems[Game.whichItem])

    # check if item is hit
    def hit():
        collision_x = Player.rect[0] + 64 >= Item.rect[0] and Item.rect[0] + 64 >= Player.rect[0]
        collision_y = Player.rect[1] + 64 >= Item.rect[1] and Item.rect[1] + 64 >= Player.rect[1]
        return collision_y and collision_x
"""