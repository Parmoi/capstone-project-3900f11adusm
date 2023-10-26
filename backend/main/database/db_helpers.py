def rows_to_list(rows):
    """Takes in a list of tuples (that represent our rows), and returns them as 
       a list of dictionaries

    Args:
        rows ([tuples]): a list of tuples representing our rows

    Returns:
        [dictionary]: a list of dictionaries representing our rows
    """
    result_list = []
    for row in rows:
        result_list.append(row._asdict())
    
    return result_list