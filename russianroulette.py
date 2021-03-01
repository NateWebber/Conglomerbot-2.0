import discord


class RussianRoulette:
    current_challenger = None
    current_challengee = None

    currently_playing = False

    current_turn = 1

    def __init__(self):
        super().__init__()
        self.current_challenger = None
        self.current_challengee = None
        self.currently_playing = False
        self.current_turn = 1

    #issue a challenge for a game
    def start_challenge(self, new_challenger, new_challengee):
        print(
            f"RR challenge started with challenger {new_challenger.name} and challengee {new_challengee.name}")
        # set_currently_playing(True)
        self.currently_playing = True
        # print(get_currently_playing())
        print(self.currently_playing)
        self.current_challenger = new_challenger
        self.current_challengee = new_challengee

    #run a game
    def play():
        self.current_turn = 1
        while(currently_playing):
            #TODO write the game logic ezpz
            print("please dont crash bc i haven't written you yet thanks")

    #cancel the current challenge
    def cancel(self):
        print("Cancelled RR challenge...")
        self.current_challenger = None
        self.current_challengee = None
        self.currently_playing = False

    #getter
    def get_currently_playing(self):
        return self.currently_playing

    #setter
    def set_currently_playing(self, new):
        self.currently_playing = new
