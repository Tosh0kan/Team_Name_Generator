import pandas as pd


def main():
    # Get number of teammates
    try:
        count = int(input("Enter team size: "))
        print(f"Team size set to {count}\n\n")

    except ValueError:
        count = 4
        print(f"Invalid input, setting team size to {count}\n\n")

    # Get leader information
    leader_present = input("Define a team Leader? (y/n): ")
    if (leader_present.lower() in ["y", "yes"]):
        lead = str(input("Enter name of team leader: "))
        lead = break_name(lead)
        count -= 1
        leader_present = True
    else:
        leader_present = False

    print("\n\n")

    # Get member information
    members = []
    for i in range(count):
        member = str(input(f"Enter name of team member {i+1}: "))
        members.append(break_name(member))
    print("\n\n")
    # Make all possible combinations of members
    combs = find_team_names(members)
    # If there is a team leader, add to this list of combs using their initials
    if (leader_present is True):
        final_combs = []
        for i in range(len(lead)):
            for j in range(len(combs)):
                final_combs.append(lead[i] + combs[j])
        combs = final_combs

    # Print the final results
    print(f"List of potential team names: \n\n{combs}")

    # Print possible team names based on a list of colours
    cols = loadcols()

    # Format cols so every colour is 1 word long and unique
    _ = {}
    for col in cols:
        temp = col.split(" ")
        for temp2 in temp:
            if (temp2 not in _):
                _[temp2] = True
    cols = _.copy()
    del _
    # Cycle through the team names and search for colours they could ascribe to
    for team_name in combs:
        find_colour(team_name, cols)
    return


# Find possible colours from a given name (i.e. team initial)
def find_colour(name, colours):
    n, found = name.lower().strip(" "), False

    # Remove duplicate letters in name
    i = 1
    while (i < len(n) - 1):
        if (n[i] == n[i + 1]):
            n = n[:i] + n[i + 1:]
        i += 1

    # Go through colours and check if any can be applied to this name
    for colour in colours:
        c, i = colour.lower(), 0

        for char in c:
            if (char == n[i]):
                i += 1

            if (i >= len(n)):
                print(f"Team {name}: {colour}")
                found = True
                break

    if (found is False):
        print(f"No valid colour found for team {name}")
    return


# Find all possible letter combinations
def find_team_names(members):
    output, combs = [], find_combs(members)
    for comb in combs:
        output += permutation([comb[i] for i in range(len(comb))])

    # Tidy list of lists of team initials into list of strings
    for i in range(len(output)):
        output[i] = "".join(output[i])
    output = clean_dupes(output)
    return output


# Find all combinations of team names
def find_combs(members, current_members=[""]):
    relevant, output = members[0], []
    for m in relevant:
        for cm in current_members:
            output.append(cm + m)

    # If there is more than 1 member, repeat the process for everything beyond this member
    if (len(members) > 1):
        output = find_combs(members[1:], output)
    return output


# Find all permutations of a given list (Of team initials)
def permutation(team):
    # If the list is empty or only one long then there are no permutations
    # Note: [list()] format needed as code assumes it is operating with a list of lists (line 72 p becomes a string which disallows proper concatenation)
    if len(team) <= 1:
        return [list(team)]
    l = []  # empty list that will store the current permutation(s)
    # Iterate over the input and calculate the permutations
    for i in range(len(team)):
        #  Extract a single entry from the list, store it as a length 1 list, and keep the rest as another list
        member, remainder = team[i], team[:i] + team[i + 1:]
        #  Generating all permutations where member is first element
        for p in permutation(remainder):
            l.append([member] + p)
    return l


# Clean letter combinations to remove duplicates
def clean_dupes(combs):
    combs, i = sorted(combs), 1
    while (i < len(combs)):
        if (combs[i - 1] == combs[i]):
            combs.pop(i)
        else:
            i += 1
    return combs


# Break name into a list of unique initials
def break_name(name, breakers=[" ", "-"]):
    #  'breakers' differentiate parts of a name (i.e. spaces and hyphens)
    #  Format input
    if (type(name) != list):
        broken = [name]
    else:
        broken = [n for n in name]

    # Break name into list of initals
    for breaker in breakers:
        temp = []
        for _ in broken:
            temp.append(_.split(breaker))
        broken = []
        for lst in temp:
            for word in lst:
                broken.append(word)
    for i in range(len(broken)):
        broken[i] = broken[i].upper()[0]
    # Remove duplicates and remnants (blanks and odd characters)
    broken = clean_dupes(broken)
    i = 0
    while (i < len(broken)):
        if (broken[i] in ["", " ", "-"]):
            broken.pop(i)
        else:
            i += 1
    return broken


def loadcols(file='v1_colours.csv'):
    if (file[-3:] == "csv"):
        frame = pd.read_csv(file)

    elif (file[-4:] == "json"):
        frame = pd.read_json(file)

    return frame["name"]


if (__name__ == "__main__"):
    main()
