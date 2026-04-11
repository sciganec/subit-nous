import json
import random

def generate_dataset(num_samples=10000, output_path="classifier_data.json"):
    print(f"Generating {num_samples} samples...")
    # Simplified version
    data = []
    for i in range(num_samples):
        data.append({"text": f"Sample text {i}", "subit": random.randint(0, 255)})
    with open(output_path, "w") as f:
        json.dump(data, f)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    generate_dataset()