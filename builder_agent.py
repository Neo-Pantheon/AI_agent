
from collections import defaultdict, deque
import os
import openai
from PIL import Image
import base64

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "#####")

# Sample block ID → type mapping
BLOCK_ID_TYPE_MAP = {
    "3": "floor",
    "4": "wall",
    "47": "roof",
    "14": "door"
}

ESSENTIAL_COMPONENTS = {"floor", "wall", "roof", "door"}


# Function to evaluate house from image using GPT-4 Vision
def query_llm_for_structure_rating_from_image(image_path: str) -> float:
    prompt = """
You are an AI architect evaluating a house structure from the image below.
Determine how structurally sound, realistic, and complete the house appears.
Give a score between 0 and 10. Respond with the score only.
"""
    try:
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                ]}
            ],
            max_tokens=10
        )
        content = response.choices[0].message.content.strip()
        score = float(content)
        return score
    except Exception as e:
        print(f"[OpenAI Vision ERROR]: {e}")
        return 0.0


# Main house evaluation function
def evaluate_house_advanced(blocks, image_path=None):
    score = 0
    block_types = set()
    occupied = set()
    support_map = defaultdict(list)
    for b in blocks:
        x, y, z = b["x"], b["y"], b["z"]
        ID = b["ID"]
        b_type = BLOCK_ID_TYPE_MAP.get(ID, "unknown")
        block_types.add(b_type)
        occupied.add((x, y, z))
        support_map[(x, y - 1, z)].append((x, y, z))
    score += len(blocks) * 2
    score += len(set(b["ID"] for b in blocks)) * 1.5
    missing_components = ESSENTIAL_COMPONENTS - block_types
    if not missing_components:
        score += 10
    else:
        score -= len(missing_components) * 2
    floating_penalty = 0
    for b in blocks:
        if b["y"] == 0:
            continue
        if (b["x"], b["y"] - 1, b["z"]) not in occupied:
            floating_penalty += 1
    score -= floating_penalty * 3
    def bfs_connected(start):
        visited = set()
        queue = deque([start])
        while queue:
            current = queue.popleft()
            visited.add(current)
            for dx, dy, dz in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
                neighbor = (current[0]+dx, current[1]+dy, current[2]+dz)
                if neighbor in occupied and neighbor not in visited:
                    queue.append(neighbor)
        return visited
    connected_set = bfs_connected(next(iter(occupied)))
    disconnected_blocks = len(occupied) - len(connected_set)
    if disconnected_blocks > 0:
        score -= disconnected_blocks * 2
    # OpenAI Vision scoring from image
    if image_path:
        learned_score = query_llm_for_structure_rating_from_image(image_path)
    else:
        print("[INFO] No image provided for OpenAI LLM evaluation.")
        learned_score = 0.0
    score += learned_score
    return {
        "final_score": round(score, 2),
        "components_present": list(block_types),
        "missing_components": list(missing_components),
        "floating_blocks": floating_penalty,
        "disconnected_blocks": disconnected_blocks,
        "llm_score": learned_score
    }




import random

# Function to randomize block positions
def randomize_block_positions(blocks, grid_size=(5, 3, 5)):
    used_positions = set()
    randomized_blocks = []
    for block in blocks:
        while True:
            x = random.randint(0, grid_size[0] - 1)
            y = random.randint(0, grid_size[1] - 1)
            z = random.randint(0, grid_size[2] - 1)
            if (x, y, z) not in used_positions:
                used_positions.add((x, y, z))
                break
        new_block = {
            "x": x,
            "y": y,
            "z": z,
            "ID": block["ID"]
        }
        if block.get("orientation"):
            new_block["orientation"] = random.choice(["north", "south", "east", "west"])
        randomized_blocks.append(new_block)
    return randomized_blocks



import random

# Function to randomize block positions with Minecraft-style support rules
def randomize_block_positions_2(blocks, grid_size=(5, 5, 5)):
    used_positions = set()
    randomized_blocks = []
    for block in blocks:
        attempts = 0
        while True:
            x = random.randint(0, grid_size[0] - 1)
            y = random.randint(0, grid_size[1] - 1)
            # Height logic:
            # z=0 is always valid
            # z>0 only if (x, y, z-1) is occupied
            valid_z_values = [0]
            for z in range(1, grid_size[2]):
                if (x, y, z - 1) in used_positions:
                    valid_z_values.append(z)
            if not valid_z_values:
                continue  # no support
            z = random.choice(valid_z_values)
            if (x, y, z) not in used_positions:
                used_positions.add((x, y, z))
                break
            attempts += 1
            if attempts > 20:
                print(f"⚠️ Too many attempts to place block: {block['ID']}")
                break
        new_block = {
            "x": x,
            "y": y,
            "z": z,
            "ID": block["ID"]
        }
        if block.get("orientation"):
            new_block["orientation"] = random.choice(["north", "south", "east", "west"])
        randomized_blocks.append(new_block)
    return randomized_blocks



import random

# Function to randomize block positions with Minecraft-style support rules
def randomize_block_positions_with_duplicates(blocks, grid_size=(5, 5, 5), copies_per_block=3):
    used_positions = set()
    randomized_blocks = []

    for block in blocks:
        for _ in range(copies_per_block):
            attempts = 0
            while True:
                x = random.randint(0, grid_size[0] - 1)
                y = random.randint(0, grid_size[1] - 1)
                # Height logic:
                # z=0 is always valid
                # z>0 only if (x, y, z-1) is occupied
                valid_z_values = [0]
                for z in range(1, grid_size[2]):
                    if (x, y, z - 1) in used_positions:
                        valid_z_values.append(z)
                if not valid_z_values:
                    attempts += 1
                    if attempts > 20:
                        print(f"⚠️ Too many attempts to place block: {block['ID']}")
                        break
                    continue  # Try another position
                z = random.choice(valid_z_values)

                if (x, y, z) not in used_positions:
                    used_positions.add((x, y, z))
                    new_block = {
                        "x": x,
                        "y": y,
                        "z": z,
                        "ID": block["ID"]
                    }
                    if block.get("orientation"):
                        new_block["orientation"] = random.choice(["north", "south", "east", "west"])
                    randomized_blocks.append(new_block)
                    break
    return randomized_blocks



# Optimization Loop
def optimize_block_positions(base_blocks, image_path=None, iterations=30):
    best_score = float('-inf')
    best_blocks = None
    best_result = None
    for i in range(iterations):
        new_blocks = randomize_block_positions_with_duplicates(base_blocks)
        result = evaluate_house_advanced(new_blocks, image_path=image_path)
        score = result["final_score"]
        print(f"Iteration {i+1}: Score = {score}")
        if score > best_score:
            best_score = score
            best_blocks = new_blocks
            best_result = result
    return best_blocks, best_result




# MAIN EXECUTION
if __name__ == "__main__":
    base_blocks = [
        {"x": 0, "y": 0, "z": 0, "ID": "3"},
        {"x": 1, "y": 0, "z": 0, "ID": "4", "orientation": "south"},
        {"x": 0, "y": 1, "z": 0, "ID": "47"},
        {"x": 2, "y": 0, "z": 0, "ID": "14", "orientation": "north"}
    ]
    best_blocks, best_result = optimize_block_positions(base_blocks, image_path="camera_view.png", iterations=200)
    print("\n✅ Best Scoring Blocks:")
    for b in best_blocks:
        print(b)
    print("\n📊 Best Evaluation Result:")
    print(best_result)
    
