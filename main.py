import random

# Single player game backlog
# [X] 1. Print score table
# 2. generate and print 5 dices - 1 move - done
# 3. run over 3 iteration with user selection - result of 5 dices for score save
# 4. print final result after move 3-iteration dice result
# 5. get user input where to save - done
# 6. calculate how many points user will get in his selection - done for ones done for twos
# 7. update score table dict - done for ones
# 8. loop to next move with updated score board - working

# once you run out of moves calculate premium and end game score
# write score to record list


def main():
    move_count = 6  # TODO implement remaining  options
    while move_count > 0:
        score_table(table)
        score_for_save = single_move()
        save_target = user_save_input()
        update_score_table(save_target, score_for_save)
        move_count -= 1

    game_end_score(table)


def generate_random_dices(dice_count: int) -> list[int]:
    """ Simulates multiple dice throw

    Based ond dice_count it will return list

    Args:
        dice_count: int - required element count in list

    Returns:
        dices_and_values -  dice count elements with values in range 1-6

    Rises:
          None
    """

    dices_and_values = []
    for i in range(0, dice_count):
        dice_value = random.randint(1, 6)
        dices_and_values.append(dice_value)
    return dices_and_values


table = {'ones  ': 'None', 'twos  ': 'None', 'threes': 'None',
         'fours ': 'None', 'fives ': 'None', 'sixes ': 'None'}


def score_table(mydict):
    print("==== Current score table ====")
    for key in mydict:
        print(key, '->', mydict[key])

# TODO merge  get_dice_retrow_selection with single_move funcion


def get_dice_retrow_selection():
    print("Please select which dices you want to keep:(1-5 or 0 to keep all)")
    selection_list = []
    string = input()

    for x in string:
        selection_list.append(int(x))

    print("selection debug info: ", selection_list)
    return selection_list


def single_move():
    final_dice_list = []
    trow_again = True
    count = 3
    default_dices_to_keep = 0

    while trow_again and count > 0:
        temp_list = generate_random_dices(5 - default_dices_to_keep)
        print("Current dice throw: ", temp_list)
        # contunue here
        alist = get_dice_retrow_selection()
        if alist[0] == 0:
            return temp_list
        default_dices_to_keep = default_dices_to_keep + len(alist)
        count -= 1

    for drow in temp_list:
        final_dice_list.append(drow)

    return final_dice_list


def user_save_input():
    # this will return key value ones - sixes

    save_opts = ['ones', 'twos', 'threes',
                 'fours', 'fives', 'sixes']
    while True:
        save_input = str(
            input("Please enter destination for piont save (ex. ones):"))
        if save_input in save_opts:
            return save_input
        else:
            print("Invalit save option try again")


def update_score_table(save_input, score):
    score_list = score
    count = 0

    if save_input == 'ones':
        for num in score_list:
            if num == 1:
                count += 1
        table['ones  '] = count

    if save_input == 'twos':
        for num in score_list:
            if num == 2:
                count += 2
        table['twos  '] = count

    if save_input == 'threes':
        for num in score_list:
            if num == 3:
                count += 3
        table['threes'] = count

    if save_input == 'fours':
        for num in score_list:
            if num == 4:
                count += 4
        table['fours '] = count

    if save_input == 'fives':
        for num in score_list:
            if num == 5:
                count += 5
        table['fives '] = count

    if save_input == 'sixes':
        for num in score_list:
            if num == 6:
                count += 6
        table['sixes '] = count


def game_end_score(mydict):
    final_score = 0
    for key in mydict:
        final_score += mydict[key]
    print(" ")
    print("Game is ended your score is: ", final_score)


if __name__ == "__main__":
    main()

