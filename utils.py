rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
main_diagonal = [rows[index] + cols[index] for index in range(len(rows))]
minor_diagonal = [rows[index] + cols[len(rows) - index-1] for index in reversed(range(len(rows)))]
unitlist = row_units + column_units + square_units + [main_diagonal, minor_diagonal]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)