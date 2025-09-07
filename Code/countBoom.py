# from collections import Counter

# def count_quartet_numbers(filename):
#     counts = Counter()

#     with open(filename, 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line.startswith("Number of right quartets:"):
#                 try:
#                     number = int(line.split(":")[1].strip())
#                     counts[number] += 1
#                 except ValueError:
#                     continue  # In case the number is not properly formatted

#     # Print results in a table
#     print(f"{'Number':>10} | {'Count':>5}")
#     print("-" * 18)
#     for number, count in sorted(counts.items()):
#         print(f"{number:>10} | {count:>5}")

# # Replace 'your_file.txt' with the path to your document
# count_quartet_numbers('./VerifyBoom.txt')


import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import poisson

def count_quartet_numbers(filename):
    counts = Counter()

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Number of right quartets:"):
                try:
                    number = int(line.split(":")[1].strip())
                    counts[number] += 1
                except ValueError:
                    continue

    return counts

def plot_results(counts, total_trials, poisson_mean=4):
    # Extract and sort the observed data
    observed_values = sorted(counts.items())
    x_obs = [k for k, _ in observed_values]
    y_obs = [v for _, v in observed_values]

    # Create Poisson expected frequencies
    x_range = range(min(x_obs), max(x_obs) + 1)
    y_expected = [poisson.pmf(k, poisson_mean) * total_trials for k in x_range]
    # y_expected2 = [poisson.pmf(k, 4) * total_trials for k in x_range]

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(x_obs, y_obs, width=1.0, alpha=0.6, label='Observed', color='skyblue', edgecolor='black')
    plt.plot(x_range, y_expected, 'r-', label='Expected (Poisson, μ=4)', linewidth=2)
    # plt.plot(x_range, y_expected2, 'g--', label='Expected (Poisson, μ=16)', linewidth=2)

    plt.title('Observed vs Expected (Poisson) Distribution of "Right Quartets"')
    plt.xlabel('Number of Right Quartets')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Replace 'your_file.txt' with the path to your document
counts = count_quartet_numbers('./verSandfirst10000.txt')
# for item, count in sorted(counts.items()):
#     print(f'{item}: {count}')
plot_results(counts, 10000)

# counts2 = count_quartet_numbers('./VerifyBoom2-8-10k.txt')
# # for item, count in sorted(counts2.items()):
# #     print(f'{item}: {count}')
# plot_results(counts2, 10000)