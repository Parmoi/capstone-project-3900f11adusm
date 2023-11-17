def rows_to_list(rows):
    """Takes in a list of tuples (that represent our rows), and returns them as 
       a list of dictionaries
    
    NOTES:
        - If our row has a SQL date column, we will convert it into a normal
          string, which is the desired format for the frontend
        - (Specific to db_trade): if a key is "post_images", we want to
          convert the string of image urls to a list of strings
          E.g. "google.com,geeksforgeeks.org" --> ["google.com", "geeksforgeeks.org"]

    Args:
        rows ([tuples]) / row (tuple): a list of tuples representing our rows

    Returns:
        [dictionary]: a list of dictionaries representing our rows
    """
    result_list = []
    for row in rows:
        new_dict = row._asdict()

        # If key has "date" substring in it, convert it to string
        for key, value in new_dict.items():
            if ("date" in key) or (key == "post_created"):
                new_dict[key] = value.strftime('%d/%m/%Y')
        
        result_list.append(new_dict)
    
    return result_list