import logging


def traverse(adjacency_dict, depth=4):
    state_combos = set()

    for start in adjacency_dict:
        temp_combos = dfs(start, set(), adjacency_dict, depth)
        state_combos.update(temp_combos)

    logging.debug(f"state_combos({state_combos})")
    return state_combos

def dfs(current_state, current_combo, adjacency_dict, depth):
    local_combo = current_combo.copy()

    if depth == 0:
        return {combo_to_str(local_combo)}

    local_combo.add(current_state)

    results = set()

    if current_state in adjacency_dict:
        for neighbor in adjacency_dict[current_state]:
            if neighbor not in local_combo:
                results.update(dfs(neighbor, local_combo, adjacency_dict, depth - 1))

    return results

def combo_to_str(combo):
    res = ""
    # sort combo to an alphabetical list
    combolist = sorted(combo)
    for item in combolist:
        res += item + "-"
    return res.strip("-")
