import logging
from utils import *

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Find all instances of naked twins
        possibly_twins = [box for box in unit if len(values[box])==2]
        if len(possibly_twins) > 1:
            count_twins = {}
            for box in possibly_twins:
                count_twins.setdefault(values[box], set()).add(box)

            # filter boxes with same value and length 2
            twins = dict(filter(lambda x: len(x[1]) > 1, count_twins.items()))
            # Eliminate the naked twins as possibilities for their peers
            if len(twins) > 0:
                remove_twins_in_unit(twins, unit, values)
    return values

def remove_twins_in_unit(twins, unit, values):
    """
    Remove all twins values from box values in given unit
    :param twins: dict of box value(twins value) and box labels where this values located 
    :param unit: one of unitlist unit where should  
    :param values: vc
    """
    for x in twins:
        for box in unit:
            if len(values[box]) > 1 and box not in twins[x]:
                remove_digits(box, values, x)

def remove_digits(box, values, digits):
    """
    Remove only specific digits from box value
    :param box: specific box label
    :param values: dict of box values
    :param digits: digits to remove in string representation.
    """
    for digit in digits:
        values[box] = values[box].replace(digit, '')

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return dict([(key, '123456789') if val == '.' else (key, val) for key, val in zip(boxes, grid)])

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    elimination_dict = [k for k in values if len(values[k]) == 1]
    for key in elimination_dict:
        for peer in peers[key]:
            assign_value(values, peer, values[peer].replace(values[key], ''))
            # values[peer] = values[peer].replace(values[key], '')

    return values

def only_choice(values):
    for unit in unitlist:
        for digit in "123456789":
            digits_in_unit = [box for box in unit if digit in values[box]]
            if len(digits_in_unit) == 1:
                assign_value(values, digits_in_unit[0], digit)
                # values[digits_in_unit[0]] = digit

    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_values = dict(filter(lambda x: len(x[1]) > 1, values.items()))
    preferred_box = min(unsolved_values.items(), key=lambda k: len(k[1]))

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[preferred_box[0]]:
        values_tmp = values.copy()
        values_tmp[preferred_box[0]] = digit
        result = search(values_tmp)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid_values(diag_sudoku_grid))
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
