#   Welcome to my Blackjack program! The terminal and pygame window will walk you through the game.
#   Credits: 
# Pygame interface inspiration from LeMaster Tech, https://www.youtube.com/watch?v=e3YkdOXhFpQ
# Card Images for interface from https://opengameart.org/content/playing-cards-vector-png

import random
import pygame
import os
import time

# Pygame Window
pygame.init()
WIDTH = 1020
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH , HEIGHT])
pygame.display.set_caption('Python Multiplayer Blackjack')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf' , 44)

#Functions

def outcome_result(outcome):
    mult = 0
    if outcome == "lose":
        mult = -1
    if outcome == "win":
        mult = 1
    if outcome == "have Blackjack":
        mult = 1.5
    
    return mult

def balance_update(balances, round_bets, outcomes):
    for i in range(len(balances)):
        balances[i] += (round_bets[i] * outcome_result(outcomes[i]))

def keep_pygame_responsive():
    pygame.event.pump()      # handle OS events so window stays alive
    pygame.display.flip() 

def deal_card():
    if not cards:
        raise RuntimeError("No cards left to deal")
    idx = random.randrange(len(cards))
    card = cards.pop(idx)
    val  = vals.pop(idx)  
    return [card,val]

def draw_card(card, start_horiz, start_vert):
    image_path = os.path.join("Playing Cards",f"{card}.png")
    image_surface = pygame.image.load(image_path).convert_alpha()
    screen.blit(image_surface, (start_horiz, start_vert))
    pygame.display.flip


keep_pygame_responsive()
num_players = input('Enter the number of people playing (Max 5): ')
while not num_players.isdigit() or int(num_players) <= 0 or int(num_players) > 5:
    keep_pygame_responsive()
    num_players = input('Value Error> Please enter a positive, non-zero integer from 1 to 5: ')

num_players = int(num_players)
time.sleep(0.5)

# Ask for starting balances from players
balance_lst = []
balancereport = []
for i in range(num_players):
    keep_pygame_responsive()
    starting_sum = float(input(f"Player {i+1}: Enter the amount of money you want to play with: "))
    while starting_sum <= 0.0:
        keep_pygame_responsive()
        starting_sum = float(input(f"Player {i+1}: Value Error> Please enter a positive, non-zero value: "))
    balance_lst.append(starting_sum)
    balancereport.append(f"Player {i+1}: ${starting_sum:.2f}")
    time.sleep(0.5)

print(balancereport)

time.sleep(1)

# start collecting data for game wins/losses report
money_dat = []
for i in range(num_players):
    player_money = [balance_lst[i]]
    money_dat.append(player_money)


game_running = True

# Main game sequence
while game_running:

    timer.tick(fps)
    screen.fill((7,143,37))

    # Reset to full deck
    cards = ["A_di", "2_di", "3_di", "4_di", "5_di", "6_di", "7_di", "8_di", "9_di", "10_di", "Jk_di", "Qn_di", "Kg_di",
         "A_cl", "2_cl", "3_cl", "4_cl", "5_cl", "6_cl", "7_cl", "8_cl", "9_cl", "10_cl", "Jk_cl", "Qn_cl", "Kg_cl",
         "A_ht", "2_ht", "3_ht", "4_ht", "5_ht", "6_ht", "7_ht", "8_ht", "9_ht", "10_ht", "Jk_ht", "Qn_ht", "Kg_ht",
         "A_sp", "2_sp", "3_sp", "4_sp", "5_sp", "6_sp", "7_sp", "8_sp", "9_sp", "10_sp", "Jk_sp", "Qn_sp", "Kg_sp"]
    vals = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
         11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
         11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
         11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,]


    # Check for broke players
    out_indices = [i for i in range(num_players) if balance_lst[i] <= 0.0]
    
    # End game if all players broke
    if len(out_indices) == num_players:
        print("Sorry! All players have gone broke. Get better and come back next time!")
        break

    # Ask for initial bets
    round_bet_lst = []
    round_bets_report = []

    for i in range(num_players):
        keep_pygame_responsive()
        if balance_lst[i] <= 0.0:
            bet = 0.0
            print(f"Player {i+1}: you have $0.00 — betting ${bet:.2f} this round.")
        else:
            bet = float(input(f"Player {i+1}: Enter the amount of money you would like to bet for this round: "))
            time.sleep(0.25)
        
            while bet > balance_lst[i]:
                keep_pygame_responsive()
                print("Error: bet exceeds your available balance. Please enter a lower bet")
                bet = float(input(f"Player {i+1}: Enter the amount of money you would like to bet for this round: "))
                time.sleep(0.25)
        
            if bet == balance_lst[i]:
                print("Warning: You have gone all in. Your remaining balance is $0.00")

        round_bet_lst.append(bet)
        round_bets_report.append(f"Player {i+1}: ${bet:.2f}")
    
    time.sleep(0.5)
    
    print(round_bets_report)

    # Deal Cards

    pcard_1s = []
    pval_1s = []
    pcard_2s = []
    pval_2s = []

    x_orig = 20
    y_orig = 330

    for i in range(num_players):

        pdat_1 = deal_card()
        pcard_1 = pdat_1[0]
        pcard_1s.append(pcard_1)
        pval_1 = pdat_1[1]
        pval_1s.append(pval_1)
        draw_card(pcard_1, x_orig, y_orig)
        pygame.display.flip() 
        time.sleep(0.5)

        pdat_2 = deal_card()
        pcard_2 = pdat_2[0]
        pcard_2s.append(pcard_2)
        pval_2 = pdat_2[1]
        pval_2s.append(pval_2)
        draw_card(pcard_2, (x_orig+15), (y_orig-25))
        pygame.display.flip() 
        time.sleep(0.1)

        print(f"Player {i+1}: Your cards are {pcard_1} and {pcard_2}")
        x_orig += 200
        time.sleep(0.5)

    ddat_1 = deal_card()
    dcard_1 = ddat_1[0]
    dval_1 = ddat_1[1]
    draw_card("cardback", 460, 50)
    pygame.display.flip()
    time.sleep(0.5)

    ddat_2 = deal_card()
    dcard_2 = ddat_2[0]
    dval_2 = ddat_2[1]
    draw_card(dcard_2,460,75)
    pygame.display.flip()
    time.sleep(0.5)

    print(f"The dealer's shown card is {dcard_2}")

    player_sums = []

    for i in range(num_players):
        player_sum = pval_1s[i] + pval_2s[i]
        if player_sum == 22:
            player_sum = 12
            pval_1s[i] = 1
            print(f"Player {i+1}, your cards were both aces. Your total is being set to 12.")
            time.sleep(0.5)
        player_sums.append(player_sum)

    # Set default values for outcomes

    outcome_lst = []
    for i in range(num_players):
        outcome_lst.append("n")

    
    # Check for blackjack
    for i in range(num_players):
        if player_sums[i] == 21:
            print(f"Player {i+1}, you have Blackjack! Congratulations.")
            outcome_lst[i] = "have Blackjack"
            time.sleep(0.5)



    # Start turns
    print("Now the turns will commence...")
    
    for i in range(num_players):
        keep_pygame_responsive()
        pvals = [pval_1s[i], pval_2s[i]]
        newcard_x = (50 + (200 * i))
        newcard_y = 280
        if outcome_lst[i] == "have Blackjack":
            print(f"Player {i+1}, you have Blackjack! Moving to next player.")
            time.sleep(0.5)
            continue
        move = (input(f"Player {i+1}, would you like to hit or stand? H or S: ")).upper()
        time.sleep(0.25)
        hits = 0
        while move == "H":
            pdat_new = deal_card()
            pcard_new = pdat_new[0]
            pval_new = pdat_new[1]
            pvals.append(pval_new)
            draw_card(pcard_new,newcard_x,newcard_y)
            pygame.display.flip()
            player_sums[i] += pval_new
            time.sleep(0.5)
            print(f"Your new card is {pcard_new}. Your new sum is {player_sums[i]}")
            time.sleep(0.25)
            if player_sums[i] > 21:
                if 11 in pvals:
                    print(f"Bust avoided, one ace value in hand changed from 11 to 1. Your new total is {player_sums[i] - 10}.")
                    pvals[pvals.index(11)] = 1
                    player_sums[i] -= 10
                else:    
                    print(f"Drat! Player {i+1}, you have busted.")
                    outcome_lst[i] = "lose"
                    break
            hits += 1
            newcard_x += 15
            newcard_y -= 25

            if hits == 3 and player_sums[i] <= 21:
                print(f"Congratulations! You have 5 cards and have not busted, so you get an automatic 21! Proceeding to the next player")
                player_sums[i] = 21
                break

            keep_pygame_responsive()
            move = (input(f"Player {i+1}, would you like to hit or stand? H or S: ")).upper()
        
        if move == "S":
            print("Stand received.")
            time.sleep(0.5)
            continue
    
    # Final Stage: Dealer shows
    time.sleep(0.5)
    print("Now, the dealer's turn: ")

    dsum = dval_1 + dval_2
    print(f"The dealer has {dcard_1} and {dcard_2}, making their total {dsum}")
    time.sleep(0.25)
    draw_card(dcard_1, 460, 50)
    pygame.display.flip()
    time.sleep(0.25)


    dnew_y = 125
    dhits = 0
    while dsum < 17:
        print("Dealer takes a hit >")
        time.sleep(0.25)
        ddat_new = deal_card()
        dcard_new = ddat_new[0]
        dval_new = ddat_new[1]
        draw_card(dcard_new, 460, dnew_y)
        dsum += dval_new
        dnew_y +=25
        time.sleep(0.25)
        print(f"Dealer's new total is {dsum}")
        time.sleep(0.25)
        dhits += 1

        if dhits == 3:
            print("Dealer is still under 17 with 5 cards, by house rules the Dealer now has 21, pays Blackjack.")
            dsum = 21
            break
    
    # Game outcome scenarios

    if dsum >= 17:
        if dsum == 21:
            print(f"The dealer stays, pays Blackjack")
            for i in range(num_players):
                if outcome_lst[i] == "n":
                    if player_sums[i] < dsum:
                        outcome_lst[i] = "lose"
                    else:
                        outcome_lst[i] = "push"

        elif dsum < 21:
            print(f"The dealer stays, pays {dsum + 1}")
            for i in range(num_players):
                if outcome_lst[i] == "n":
                    if player_sums[i] < dsum:
                        outcome_lst[i] = "lose"
                    elif player_sums[i] > dsum:
                        outcome_lst[i] = "win"
                    else:
                        outcome_lst[i] = "push"

        else:
            print(f"The dealer goes bust, pays all still in!")
            for i in range(num_players):
                    if outcome_lst[i] == "n":
                        outcome_lst[i] = "win"
    
    # Print round outcomes:
    for i in range(num_players):
        time.sleep(0.5)
        print(f"Player {i+1}: you {outcome_lst[i]}!")
        time.sleep(0.5)
    
    balance_update(balance_lst, round_bet_lst, outcome_lst)

    print("Here are the new balances:")
    time.sleep(0.25)
    for i in range(num_players):
        balancereport[i] = f"Player {i+1}: ${balance_lst[i]:.2f}"
        print(f"{balancereport[i]}")
        time.sleep(0.25)

        # Ask if the players want another round
    
    
    keep_pygame_responsive()
    play_again = input("Would you like to play again? Y or N: ")
    if play_again == "N":
        game_running = False
        pygame.quit()
        time.sleep(1)



# Create file with game outcomes:

starting_balances = []
ending_balances = []
balance_changes = []
change_percents = []




for i in range(num_players):
    money_dat[i].append(balance_lst[i])
    starting_balances.append(money_dat[i][0])
    ending_balances.append(money_dat[i][1])
    balance_changes.append(abs(ending_balances[i] - starting_balances[i]))
    change_percents.append((balance_changes[i] / starting_balances[i]) * 100)

with open('Balance_Data.txt','w') as result:
    result.write("Great game players! Here is how your balances have changed: \n")
    result.write("\n")
    
    for i in range(num_players):
        result.write(f"Player {i+1}, your results: \n")
        result.write(f"Starting Balance: ${(starting_balances[i]):.2f} \n")
        result.write(f"Ending Balance: ${(ending_balances[i]):.2f} \n")
        if starting_balances[i] <= ending_balances[i]:
            result.write(f"Your balance changed by ${(balance_changes[i]):.2f}, or {(change_percents[i]):.1f}% \n")
        else:
            result.write(f"Your balance changed by -${(balance_changes[i]):.2f}, or -{(change_percents[i]):.1f}% \n")
        
        result.write("\n")

print("Thanks for playing! See the new file, Balance_Data.txt, for final game stats ->")

# *END PROGRAM*
