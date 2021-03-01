import discord
from random import randint

class RussianRoulette:
    current_challenger = None
    current_challengee = None

    currently_challenging = False
    currently_playing = False

    current_turn = 1

    p1_alive = True
    p2_alive = True

    def __init__(self):
        super().__init__()
        self.current_challenger = None
        self.current_challengee = None
        self.currently_challenging = False
        self.currently_playing = False
        self.current_turn = 1
        self.p1_alive = True
        self.p2_alive = True

    #issue a challenge for a game
    def start_challenge(self, new_challenger, new_challengee):
        print(
            f"RR challenge started with challenger {new_challenger.name} and challengee {new_challengee.name}")
        # set_currently_playing(True)
        self.currently_challenging = True
        # print(get_currently_playing())
        # print(self.currently_challenging)
        self.current_challenger = new_challenger
        self.current_challengee = new_challengee

    #cancel the current challenge
    def cancel(self):
        print("Cancelled RR challenge...")
        self.current_challenger = None
        self.current_challengee = None
        self.currently_challenging = False

    #run a game
    def play(self):
        self.current_turn = 1
        self.currently_challenging = False
        self.currently_playing = True
        self.p1_alive = True
        self.p2_alive = True

    def shoot(self):
        result = randint(1, 6)
        if (result == 6):
            if (self.current_turn == 1):
                self.p1_alive = False
            else:
                self.p2_alive = False
        if (self.current_turn == 1):
            self.current_turn = 2
        else:
            self.current_turn = 1
        return result

    def end_game(self):
        self.current_challenger = None
        self.current_challengee = None
        self.currently_challenging = False
        self.currently_playing = False
        self.current_turn = 1
        self.p1_alive = True
        self.p2_alive = True
        



