def has_true_value(dictionary: dict) -> bool:
    """
    Checks if any value in the dictionary is True.
    
    Args:
        dictionary (dict): The dictionary to check.
        
    Returns:
        bool: True if any value is True, False otherwise.
    """
    return any(dictionary.values())
