import random
import sys
import hashlib
import hmac
import math
import secrets
from tabulate import tabulate

class key_generator:
    @staticmethod
    def generate_key():
        return secrets.token_hex(32)


class HMAC_generator:
    @staticmethod
    def generate_hmac(choice, key):
        choice = choice.encode()
        key = key.encode()
        return hmac.new(key, choice, hashlib.sha3_256).hexdigest()
        

class game_logic:
    def __init__(self, choices):
        self.choices = choices
        self.total_length = len(choices)

    def find_winner(self, player_choice, computer_choice):
        mid = math.floor(self.total_length/2)
        
        player_choice = self.choices.index(player_choice)
        computer_choice = self.choices.index(computer_choice)

        if player_choice == computer_choice:
            return "Draw"
        elif ((computer_choice>player_choice and computer_choice-player_choice<=mid) or (player_choice>computer_choice and player_choice-computer_choice>mid)):
            return "Win"
    
        else:
            return "Lose"
        
        

    

class help_table:
    def __init__(self, choices):
        self.choices = choices
        self.total_length = len(choices)     

    def generate_table(self):
        header = ['v PC\\User >'] + self.choices
        game = game_logic(self.choices)
        table_data = []
        for i in range(self.total_length):
            pc_move = self.choices[i]
            row = []
            row.append(pc_move)
            for j in range(self.total_length):
                user_move = self.choices[j]
                result = game.find_winner(pc_move, user_move)
                row.append(result)
            table_data.append(row)
                
        table = tabulate(table_data, headers=header, tablefmt='grid')

        # Print the table
        print(table)
        

    

def verified(choices):
    if not choices:
        print("Enter this way: python game.py move1 move2 ....")
        sys.exit()
    if len(choices)<3:
        print("Sorry, You must provide at least 3 moves.")
        sys.exit()
    if len(choices) % 2==0:
        print("The number of move must be odd(eg.. 3,5,7,9..)")
        sys.exit()
    if len(choices) != len(set(choices)):
        print("You should not repeat same move, Move should be Unique. Try again..!")
        sys.exit()


def main():
    choices = sys.argv[1:]
    verified(choices)

    #Key generate
    key = key_generator.generate_key()
    computer_choice = random.choice(choices)
    HMAC = HMAC_generator.generate_hmac(computer_choice, key)
    print(f"HMAC: {HMAC}")

    game = game_logic(choices)
    
    # converted to dictionary
    elements = {}
    for index, element in enumerate(choices):
        elements[index] = element
    
    #Display options
    for index, value in elements.items():
        print(f"{index+1} - {value}")
    print("0 - exit")
    print("? - help")



    user_move = input("Enter your move: ")
    if user_move == '0':
        sys.exit("Game over! Thank you for playing.")
    elif user_move == '?':
        table = help_table(choices)
        table.generate_table()
    else:
        try:
            user_move = int(user_move)
            print(f"Your Move: {elements[user_move-1]}")
            print(f"Computer Move: {computer_choice}")
            res = game.find_winner(elements[user_move-1], computer_choice)
            if res == "Win":
                print("Computer Win!")
            elif res == "Lose":
                print("You Win!")
            else:
                print("Draw")

            print(f"HMAC key: {key}")
        except:
            print("Please choose correctly..!")
            


main()