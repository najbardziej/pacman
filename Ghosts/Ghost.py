import Character
import constants


class Ghost(Character.Character):
    def __init__(self, game, tile_x, tile_y, image_row):
        super().__init__(game, tile_x, tile_y)
        self.image_row = image_row
        self.direction = constants.Direction.RIGHT
        self.animation = False

    def draw(self):
        sprite_size = self.game.sprite_sheet.sprite_size
        if self.animation:
            frame = int(self.game.tick * constants.ANIMATION_SPEED) % 2
        else:
            frame = 0
        self.game.window.blit(
            self.game.sprite_sheet.get_image_at(frame + self.direction * 2, self.image_row),
            (self.x - sprite_size / 2, self.y - sprite_size / 2))