Sbox = [
    [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
    [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
    [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
    [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
    [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
    [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
    [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12]
]

def difference_distribution_table(sbox):
    # Create a 16x16 table 
    ddt = [[0] * 16 for _ in range(16)]
    for input_diff in range(16):
        for x in range(16):
            y = x ^ input_diff
            out_diff = sbox[x] ^ sbox[y]
            ddt[input_diff][out_diff] += 1
    return ddt

# Generate and print the tables for each S-box
for idx, s in enumerate(Sbox):
    print(f"S-box {idx + 1} difference distribution table:")
    ddt = difference_distribution_table(s)
    for inp_diff, row in enumerate(ddt):
        # Print the row corresponding to this input difference
        print(f"Input diff {inp_diff:2}: {row}")
    print()  # Blank line for separation between S-boxes

def difference_distribution_table(sbox):

    ddt = [[0] * 16 for _ in range(16)]
    for input_diff in range(16):
        for x in range(16):
            y = x ^ input_diff
            out_diff = sbox[x] ^ sbox[y]
            ddt[input_diff][out_diff] += 1
    return ddt

def highest_probability_differentials(ddt, include_trivial=False):

    max_count = 0
    diff_pairs = []
    for inp in range(16):
        # Optionally skip trivial differences
        if not include_trivial and inp == 0:
            continue
        for out in range(16):
            count = ddt[inp][out]
            if count > max_count:
                max_count = count
                diff_pairs = [(inp, out)]
            elif count == max_count:
                diff_pairs.append((inp, out))
    return max_count, diff_pairs

# Process each S-box and print its highest non-trivial differential pairs
for idx, s in enumerate(Sbox):
    print(f"\nS-box {idx + 1}:")

    # Compute the difference distribution table
    ddt = difference_distribution_table(s)
    
    # Find the highest probability differentials (ignoring the trivial pair)
    max_count, diff_pairs = highest_probability_differentials(ddt, include_trivial=False)
    
    # Calculate the probability (since there are 16 inputs per difference)
    probability = max_count / 16
    
    print(f"Highest non-trivial differential probability: {probability:.4f} (count = {max_count} out of 16)")
    print("Differential pairs (input_diff -> output_diff):")
    for inp, out in diff_pairs:
        print(f"  {inp:2} -> {out:2}")
