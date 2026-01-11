# visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Load CSV
df = pd.read_csv("data/travel_destinations.csv")

# Count words in each description
df["description_word_count"] = df["description"].apply(lambda x: len(str(x).split()))

# Create figure
plt.figure(figsize=(12,7))
bars = plt.bar(df["destination"], df["description_word_count"], color=plt.cm.viridis(np.linspace(0.2, 0.8, len(df))))

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 1, f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Titles and labels
plt.title("Word Count in Travel Destination Descriptions", fontsize=16, fontweight='bold', pad=20)
plt.xlabel("City", fontsize=12, labelpad=10)
plt.ylabel("Number of Words", fontsize=12, labelpad=10)

# Gridlines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Rotate x-axis labels
plt.xticks(rotation=35, ha='right', fontsize=11)

# Tight layout
plt.tight_layout()

# Save figure
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/wordcount.png", dpi=300, bbox_inches='tight')

plt.show()
