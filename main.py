# 1. OUR ITEMS CATALOGUE (The Database)
# Each item contains a unique ID, a title, and a list of normalized tags.
item_catalogue = [
    {
        "id": 1, 
        "title": "Web Development Foundations", 
        "tags": ["HTML", "CSS", "JavaScript", "Frontend"]
    },
    {
        "id": 2, 
        "title": "Data Science with Python", 
        "tags": ["Python", "Numpy", "Pandas", "Algorithms"]
    },
    {
        "id": 3, 
        "title": "Modern Web Applications", 
        "tags": ["JavaScript", "React", "Frontend", "NodeJS"]
    },
    {
        "id": 4, 
        "title": "Introduction to Deep Learning", 
        "tags": ["Python", "Machine Learning", "Neural Networks", "Algorithms"]
    },
    {
        "id": 5, 
        "title": "Automation and Scripting", 
        "tags": ["Python", "Scripts", "Automation"]
    }
]

print(f"Catalogue loaded successfully with {len(item_catalogue)} items.")

# 2. BUILDING THE MASTER VOCABULARY
# We automatically extract every unique tag across our database to build our mathematical space.
master_vocabulary = set()

for item in item_catalogue:
    for tag in item["tags"]:
        master_vocabulary.add(tag)

# Convert to a sorted list so the index/position of each tag remains strictly identical
master_vocabulary = sorted(list(master_vocabulary))

print("\n--- MASTER VOCABULARY ---")
print(master_vocabulary)
print(f"Total unique features (Dimensions): {len(master_vocabulary)}")

# 3. VECTORIZATION FUNCTION
def vectorize_tags(tags_list, vocabulary):
    """
    Converts a list of tags into a binary vector (1s and 0s) 
    based on the master vocabulary.
    """
    # Start with a vector of all zeros, matching the size of the vocabulary
    vector = [0] * len(vocabulary)
    
    # Loop through each word in our master vocabulary
    for index, vocabulary_word in enumerate(vocabulary):
        # If the word exists in our item's tags, set the value at this index to 1
        if vocabulary_word in tags_list:
            vector[index] = 1
            
    return vector

# --- Let's test it on our catalogue! ---
print("\n--- VECTORIZING OUR CATALOGUE ---")

# We will store our items along with their newly created vectors
vectorized_database = []

for item in item_catalogue:
    binary_vector = vectorize_tags(item["tags"], master_vocabulary)
    
    # Save the vectorized item
    vectorized_database.append({
        "id": item["id"],
        "title": item["title"],
        "vector": binary_vector
    })
    
    # Print the result to see how it looks
    print(f"Title: {item['title']}")
    print(f"Tags  : {item['tags']}")
    print(f"Vector: {binary_vector}\n")
    
    # 4. CAPTURING AND VECTORIZING USER STATE (Input Stage)
def get_user_preferences(vocabulary):
    """
    Displays a numbered list of all unique tags to the user,
    captures their choices from the terminal, and returns a binary vector.
    """
    print("\n=========================================")
    print("      WELCOME TO THE RECOMMANDER SYSTEM  ")
    print("=========================================")
    print("Please select your areas of interest by entering their numbers.")
    print("Separate multiple choices with commas (e.g., 1, 4, 12).\n")
    
    # 1. Display the numbered vocabulary options
    for index, tag in enumerate(vocabulary):
        # We display indices starting from 1 (instead of 0) to be user-friendly
        print(f"[{index + 1}] {tag}")
    
    print("=========================================")
    
    user_choices = []
    
    # 2. Terminal Input Loop with Validation
    while True:
        user_input = input("\nEnter your choices (numbers): ").strip()
        
        if not user_input:
            print("You didn't select anything. Please choose at least one option!")
            continue
            
        try:
            # Split the input string by commas, convert to integers, and adjust for 0-based indexing
            selected_indices = [int(num.strip()) - 1 for num in user_input.split(",") if num.strip()]
            
            # Validate that all chosen indices fall within our vocabulary range
            valid = True
            for idx in selected_indices:
                if idx < 0 or idx >= len(vocabulary):
                    print(f"Error: Choice {idx + 1} is out of bounds. Please select numbers between 1 and {len(vocabulary)}.")
                    valid = False
                    break
            
            if not valid:
                continue
                
            # If everything is valid, map indices back to the actual string tags
            user_choices = [vocabulary[idx] for idx in selected_indices]
            break
            
        except ValueError:
            print("Invalid input! Please enter only numbers separated by commas (e.g., 2, 5).")
            
    # 3. Print out the raw text choices selected by the user
    print(f"\nYour Selected Interests: {user_choices}")
    
    # 4. Transform these text choices into our 1s and 0s vector
    user_vector = vectorize_tags(user_choices, vocabulary)
    print(f"Your User Profile Vector : {user_vector}")
    
    return user_vector

# --- Run the Input Collector ---
user_profile_vector = get_user_preferences(master_vocabulary)

# 5. RECOMMENDATION SCORING

def compute_similarity(item_vector, user_vector):
    """Computes a normalized similarity score from 0.0 to 1.0."""
    if sum(user_vector) == 0:
        return 0.0
    match_count = sum(a * b for a, b in zip(item_vector, user_vector))
    return match_count / sum(user_vector)

recommendations_pool = []
for item in vectorized_database:
    score = compute_similarity(item["vector"], user_profile_vector)
    recommendations_pool.append({
        "id": item["id"],
        "title": item["title"],
        "score": score
    })

# 6. SORT AND TRUNCATE (Output Stage)
def display_top_recommendations(pool, top_n=3):
    """
    Filters out zero-match items, sorts the recommendations by similarity score 
    in descending order, and displays the top N results.
    """
    # Filter out items that have a score of 0.0 (no alignment with user interests)
    filtered_pool = [item for item in pool if item["score"] > 0.0]
    
    # Sort the list in descending order (highest score first)
    sorted_recommendations = sorted(filtered_pool, key=lambda x: x["score"], reverse=True)
    
    print("\n=========================================")
    print(f"     YOUR PERSONALIZED RECOMMENDATIONS   ")
    print("=========================================\n")
    
    if not sorted_recommendations:
        print("No matches found! Try selecting more or different interests.")
    else:
        # Get only the top N items (e.g., top 3)
        top_matches = sorted_recommendations[:top_n]
        
        for rank, item in enumerate(top_matches, start=1):
            # Print the recommendation details
            # We match back to the original database to show tags as well
            original_item = next(x for x in item_catalogue if x["id"] == item["id"])
            print(f"Rank #{rank} | {item['title']}")
            print(f"  -> Match Confidence: {item['score'] * 100:.2f}%")
            print(f"  -> Tags: {original_item['tags']}\n")
            
    print("=========================================")

# --- Run the Output Generator ---
display_top_recommendations(recommendations_pool, top_n=3)