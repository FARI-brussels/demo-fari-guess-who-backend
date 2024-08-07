import math

def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def calculate_total_entropy(total_count):
    return calculate_entropy([1 / total_count, (total_count - 1) / total_count])

def calculate_subset_entropy(counts, total_count):
    return calculate_entropy([count / total_count for count in counts]) if total_count > 0 else 0

def calculate_match_counts(data, attribute, value):
    match_count = len([item for item in data if item[attribute] == value])
    non_match_count = len([item for item in data if item[attribute] != value]) 
    return match_count, non_match_count

def calculate_weighted_information_gain(data, match_count, non_match_count):
    total_count = len(data)
    total_entropy = calculate_total_entropy(len(data))   
    match_entropy = calculate_subset_entropy([1, match_count-1], match_count)
    non_match_entropy = calculate_subset_entropy([1, non_match_count-1],  non_match_count)
    info_gain_match = total_entropy - ((match_count / total_count) * match_entropy + (non_match_count / total_count) * 0)
    info_gain_non_match = total_entropy - ((match_count / total_count) * 0 + (non_match_count / total_count) * non_match_entropy)
    weighted_info_gain = ((match_count / total_count) * info_gain_match + (non_match_count / total_count) * info_gain_non_match)/2
    return weighted_info_gain

def evaluate_weighted_information_gain(data, attributes):
    attributes = [a["value"] for a in attributes]
    gains = {}
    for attribute in attributes:
        unique_values = set(item[attribute] for item in data)
        for value in unique_values:
            match_count, non_match_count = calculate_match_counts(data, attribute, value)
            gains[(attribute, value)] = calculate_weighted_information_gain(data, match_count, non_match_count )
    return gains


def generate_best_question(data, attributes):
    gains = evaluate_weighted_information_gain(data,attributes)
    best_attribute_value_pair = max(gains, key=gains.get)
    best_attribute, best_value = best_attribute_value_pair
    max_gain = gains[best_attribute_value_pair]
    if type(best_value) == str:
        return next(item["question"] for item in attributes if item["value"] == best_attribute).replace("_", best_value), best_attribute, best_value, max_gain
    else:
        best_value = True
        return next(item["question"] for item in attributes if item["value"] == best_attribute), best_attribute, best_value, max_gain

def process_question(attribute, value, answer, data):
    # return the remaining characters based on the attribute, value and answer
    if answer == "yes":
        remaining_characters = [item for item in data if item[attribute] == value]
    else:
        remaining_characters = [item for item in data if item[attribute] != value]
    return remaining_characters
    



