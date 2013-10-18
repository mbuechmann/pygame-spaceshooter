from pygame.constants import KEYDOWN, K_SPACE
import play_state


class GameOverState(object):
    def __init__(self, game):
        self.game = game
        pass

    def logic(self, delta):
        pass

    def render(self, screen):
        pass

    def handle_event(self, event):
        if event.type == KEYDOWN and event.key == K_SPACE:
            self.game.set_current_state(play_state.PlayState(self.game))

