def main():
	# Get number of teammates
	try:
		count = int(input("Enter team size: "))
		print(f"Team size set to {count}\n\n")
	except:
		count = 4
		print(f"Invalid input, setting team size to {count}\n\n")
	# Get leader information
	leader_present = input("Define a team Leader? (y/n): ")
	if(leader_present.lower() in ["y","yes"]):
		lead = str(input("Enter name of team leader: "))
		lead = break_name(lead)
		count -= 1;leader_present = True
	else: leader_present = False
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
	if(leader_present==True):
		final_combs = []
		for i in range(len(lead)):
			for j in range(len(combs)):
				final_combs.append(lead[i]+combs[j])
		combs = final_combs
    # Print the final results
	print(f"List of potential team names: \n\n{combs}")
	return

# Find all possible letter combinations
def find_team_names(members):
    output,combs = [],find_combs(members)
    for comb in combs:
        output += permutation([comb[i] for i in range(len(comb))])
	# Tidy list of lists of team initials into list of strings
    for i in range(len(output)):
        output[i] = "".join(output[i])
    output = clean_dupes(output)
    return output

# Find all combinations of team names
def find_combs(members,current_members=[""]):
	relevant,output = members[0],[]
	for m in relevant:
		for cm in current_members:
			output.append(cm+m)
	# If there is more than 1 member, repeat the process for everything beyond this member
	if(len(members)>1):
		output = find_combs(members[1:],output)
	return output



# Find all permutations of a given list (Of team initials)
def permutation(team):
	# If the list is empty or only one long then there are no permutations
    # Note: [list()] format needed as code assumes it is operating with a list of lists (line 72 p becomes a string which disallows proper concatenation)
    if len(team)<=1:return [list(team)]
    l = [] # empty list that will store the current permutation(s)
    # Iterate over the input and calculate the permutations
    for i in range(len(team)):
       # Extract a single entry from the list, store it as a length 1 list, and keep the rest as another list
       member,remainder = team[i],team[:i] + team[i+1:]
       # Generating all permutations where member is first element
       for p in permutation(remainder):
           l.append([member] + p)
    return l

# Clean letter combinations to remove duplicates
def clean_dupes(combs):
	combs,i = sorted(combs),1
	while(i<len(combs)):
		if(combs[i-1]==combs[i]):
			combs.pop(i)
		else:
			i+=1
	return combs

# Break name into a list of unique initials
def break_name(name,breakers=[" ","-"]):
	# 'breakers' differentiate parts of a name (i.e. spaces and hyphens)
    # Format input
    if(type(name)!=list): broken = [name]
    else: broken = [n for n in name]
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
    while(i<len(broken)):
        if(broken[i] in [""," ","-"]): broken.pop(i)
        else: i+=1
    return broken

if(__name__ == "__main__"): main()