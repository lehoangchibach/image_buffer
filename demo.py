def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

# Example usage
my_list = [i for i in range(23)]
sublists = split_list(my_list, 8)

print(sublists)
for i, sublist in enumerate(sublists):
    print(f"Sublist {i + 1}: {sublist}")
