import random

# Single player game backlog
# [X] 1. Print score table
# [X] 2. Generate and print required X dice throw with values
# [X] 3. Users move
    # [X] 3.1 Look at current dices and values
    # [X] 3.2 Select what dices to keep (all or specific)
    # [X] 3.3 Generate another dice count (depends on selection 3.2) throw with values
    # [X] 3.4 Move returns 5 dices with values after 3 trow attempts

# [X] 4. Ask user input for current point save destination option
# [X] 5. Calculate points based user selection and 3.4 move return
# [ ] 6. Update score table with calculated points -- #TODO fix this bug
# [X] 7. Decrement move count and continue with next users move

# Feature 1: calculate premium and end game score
# Feature 2: Score to record list


def main():
    move_count = 6  # TODO implement remaining  options
    while move_count > 0:
        print_score_table(table)
        score_for_save = single_move()
        save_target = user_save_input()
        update_score_table(save_target, score_for_save)
        # calculate_score(save_target, score_for_save, save_target[1])  #TODO:fix bug not updating score table and remove duplicate code old function
        move_count -= 1

    game_end_score(table)


def generate_random_dices(dice_count) ->list:
    """ Simulates multiple dice throw

    Based ond dice_count it will return list

    Args:
        dice_count: int - required element count in list

    Returns:
        dices_and_values - dice count elements with values in range 1-6

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


def is_valid_selection(dice_values: list, user_selection: str) -> bool:
    """ Convert user selection to ints and compare with
    dice value list if user selection lenght and values are valid

    Args:
        dice values:
        user_selection:

    Returns:
        True if selection is valid

    Rises:
        #TODO: catch and add correct exception

    """
    valid_rethrow_opts = [1, 2, 3, 4, 5]
    special_cases = [0 ,9]
    slen = len(user_selection)

    if slen == 0:
        return False
    # Cases rethow all - 9 or keep all 0
    if slen == 1:
        if user_selection[0] == 0:
            return True
        if user_selection[0] == 9:
            return True
        else:
            return False

    if slen > 5:
        return False
    else:
        # TODO implement validation if this conversion does not fail
        selection_ints = [int(item) for item in user_selection]
        count = 0
        for item in selection_ints:
            if item in valid_rethrow_opts:
                count += 1
        if count == slen:
            return True


def get_dice_retrow_selection() ->list:
    """ Collects dices order numbers that will be rethrowed from STDIN

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

    print("Order number of dice was selected #TODO print dice values: ", selection_list)
    return selection_list


def single_move() ->list:
    """ Simulates 3 attempts to throw dices and keep desired dices

    Args:
        None - calls generate_random_dices function to produce dice values

    Returns:
        final_dice_list [ints] - if device rethrow selection is 0 first trow
                                device values are returned
    """

    final_dice_list = []
    trow_again = True
    count = 3
    default_dices_to_keep = 0

    while trow_again and count > 0:
        print("Debug info: ", )
        dice_count = 5 - default_dices_to_keep
        print("Debug info dice count : ", dice_count, "type of dice count :" ,type(dice_count) )
        first_throw_values = generate_random_dices(dice_count)
        print("Current dices and values: ", first_throw_values)
        dices_to_keep = get_dice_retrow_selection()  # returns str list with numbers

        if is_valid_selection(first_throw_values, dices_to_keep):
            # This handles scenario keep all dices from first throw
            if dices_to_keep[0] == 0:
                return first_throw_values # TODO fix me not correct valid on if after first throw 0 is selected

            # This is redundant to rethrow al dices just select 1,2,3,4,5
            # if dices_to_keep[0] == 9:
            #    default_dices_to_keep = default_dices_to_keep
            #    count -= 1
            else:
                default_dices_to_keep = default_dices_to_keep + len(dices_to_keep)
                count -= 1
        else:
            print("Your selection was not valid please try again")

    for drow in first_throw_values:
        final_dice_list.append(drow)

    return final_dice_list


def user_save_input() ->list:
    """ Collects user choise for saving points from STDIN

    Args:
        None

    Returns:
        save_input, opts_map[save_input] - list example: ones, 1

    """
    save_opts = ['ones', 'twos', 'threes',
                 'fours', 'fives', 'sixes']

    while True:
        save_input = str(
            input("Please enter destination for piont save (ex. ones, twos ...):"))
        if save_input in save_opts:
            return save_input

        else:
            print("Invalit save option try again")


def calculate_score(dest_opt: list, dice_values: list, point_value: str):
    """ Calculate score and update table with score

    Args:
        #TODO

    Returns:
        None
    """
    count = 0
    for value in dice_values:
        if value == point_value:
            count += point_value
    table_key = dest_opt[0]
    key_point_value = count

    table[table_key] = key_point_value


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

