class GameStats:
    """ Track statistics for Aliens invasion"""

    def __init__(self,ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start alien invasion in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """initialize statics thath can change during the game"""
        self.ships_left = self.settings.ship_limit