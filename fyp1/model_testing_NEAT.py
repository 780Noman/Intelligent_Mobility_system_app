import neat
import pickle
import os

# Import your simulation function
from newcar import run_simulation  # Make sure run_simulation accepts ([(genome_id, genome)], config)

# Paths
config_path = "config.txt"
genome_path = "best_neat_genome.pkl"

# Load NEAT config
config = neat.config.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    config_path
)

# Load the best genome
if not os.path.exists(genome_path):
    raise FileNotFoundError(f"Best genome file not found at {genome_path}")

with open(genome_path, "rb") as f:
    best_genome = pickle.load(f)

# print("\n✅ Best genome loaded successfully!")
# print(f"Fitness: {best_genome.fitness}")

# Wrap the genome in the expected format: list of tuples (genome_id, genome)
test_genomes = [(0, best_genome)]

# Run the simulation for testing
run_simulation(test_genomes, config)
