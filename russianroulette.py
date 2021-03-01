import discord


current_challenger = None
current_challengee = None

currently_playing = False


def start_challenge(new_challenger, new_challengee):
    print(
        f"RR challenge started with challenger {new_challenger.name} and challengee {new_challengee.name}")
    currently_playing = True
    current_challenger = new_challenger
    current_challengee = new_challengee


def get_currently_playing():
    return currently_playing
