import random

# Single player game backlog
# [X] 1. Print score table
# [X] 2. Generate and print required X dice throw with values
# [ ] 3. Users move
    # 3.1 Look at current dices and values
    # 3.2 Select what dices to keep (all or specific)
    # 3.3 Generate another dice count (depends on selection 3.2) throw with values
    # 3.4 Move returns 5 dices with values after 3 trow attempts

# [ ] 4. Ask user input for current point save destination option
# [ ] 5. Calculate points based user selection and 3.4 move return
# [ ] 6. Update score table with calculated points
# [ ] 7. Decrement move count and continue with next users move

# Feature 1: calculate premium and end game score
# Feature 2: Score to record list


def main():
    move_count = 6  # TODO implement remaining  options
    while move_count > 0:
        print_score_table(table)
        score_for_save = single_move()
        save_target = user_save_input()
        update_score_table(save_target, score_for_save)
        move_count -= 1

    game_end_score(table)


def generate_random_dices(dice_count) ->list:
    """ Simulates multiple dice throw

    Based ond dice_count it will return list

    Args:i
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


# TODO this table is incomplete add missing options
table = {'ones  ': '0', 'twos  ': '0', 'threes': '0',
         'fours ': '0', 'fives ': '0', 'sixes ': '0'}


def print_score_table(mydict) ->None:
    """ Prints current score table """
    print("==== My Score Table ====")
    for key in mydict:
        print(key, '->', mydict[key])


# TODO merge  get_dice_retrow_selection with single_move funcion


def get_dice_retrow_selection() ->list:
    """ Collects user dices order numbers that will be rethrowed from STDIN

    Args:
        None

    Returns:
        selection_list - list of integers

    """
    print("Please select which dices you want to keep:(1-5th or 0 to keep all dices)")
    selection_list = []
    string = input()

    for x in string:
        selection_list.append(int(x))

    print("selection debug info: ", selection_list)
    return selection_list


def single_move() ->list:
    """ Simulates 3 attempts to throw dices and keep desired dices

    Args:
        None - calls generate_random_dices function to produce dice values

    Return:
        final_dice_list [ints]
    """


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

