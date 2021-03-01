import discord


class RussianRoulette:
    current_challenger = None
    current_challengee = None

    currently_playing = False

    def __init__(self):
        super().__init__()
        self.current_challenger = None
        self.current_challengee = None
        self.currently_playing = False

    def start_challenge(self, new_challenger, new_challengee):
        print(
            f"RR challenge started with challenger {new_challenger.name} and challengee {new_challengee.name}")
        # set_currently_playing(True)
        self.currently_playing = True
        # print(get_currently_playing())
        print(self.currently_playing)
        self.current_challenger = new_challenger
        self.current_challengee = new_challengee

    def get_currently_playing(self):
        return self.currently_playing

    def set_currently_playing(self, new):
        self.currently_playing = new
