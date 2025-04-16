def flip_dict(dictionary: dict) -> dict:
    """
    Flips a dictionary, swapping keys and values.
    
    Args:
        dictionary (dict): The dictionary to flip.
        
    Returns:
        dict: The flipped dictionary.
    """
    return {v: k for k, v in dictionary.items()}
