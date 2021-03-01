import discord


current_challenger = None
current_challengee = None


def start_challenge(new_challenger):
    print(f"RR challenge started with challenger {0}", new_challenger.name)
    current_challenger = new_challenger
