import json
import glob
from datasets import Dataset
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

# Read all grid problem files
data_files = glob.glob("./data/grid_problems_*.jsonl")
all_data = []

for file_path in data_files:
    grid_size = int(file_path.split("_")[-1].split("x")[0])
    with open(file_path, "r") as f:
        for line in f:
            problem_data = json.loads(line)
            system_data = json.loads(problem_data[0]["content"])
            # once its loaded, remove the system part of it
            del problem_data[0]
            all_data.append({
                "text": tokenizer.apply_chat_template(problem_data, tokenize=False),
                "problem": problem_data[0]["content"],
                "solution": problem_data[1]["content"],
                "grid_size": grid_size,
                "representation": system_data
            })

dataset = Dataset.from_list(all_data)

# Split into train and test
dataset = dataset.train_test_split(test_size=0.1, shuffle=True, seed=42)

# print one row of the dataset
print(dataset["train"][0]["text"])

dataset.push_to_hub("sumuks/maze-problem-multi-size-grid")