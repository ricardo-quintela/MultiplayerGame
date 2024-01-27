# Wave Function Collapse in Rooms

## Pseudo Code


```
size = 10 # the size of the map
rules = dict(room_name, dict(direction, list(room_name))) # the map tiles rules

# stores the avaliable rooms to colapse for each cell
collapse_table = [[[] for j in range size] for i in range size]
# contains the info on all the collapsed cells (the map itself)
generated_map = [[null for j in range size] for i in range size]

x = randint(0, size - 1)
y = randint(0, size - 1)

function wfc(x,y):

    # base cases
    if -1 < x < size - 1 or -1 < y < size - 1:
        return false

    if generated_map[x,y] is not null:
        return false

    # collapsing
    room = random_choice(collapse_table[x,y])
    generated_map[x,y] = room

    if x - 1 >= 0:
        collapse_table[x-1,y].extend(rules[room]["left"])
    if x + 1 < size:
        collapse_table[x+1,y].extend(rules[room]["right"])
    if y - 1 >= 0:
        collapse_table[x,y-1].extend(rules[room]["down"])
    if y + 1 < size:
        collapse_table[x,y+1].extend(rules[room]["up"])

    return wfc(x-1,y) or wfc(x+1,y) or wfc(x,y-1) or wfc(x,y+1)

```

