from helpers import logger
from sqlalchemy import func, desc, asc

"""
Class where numbers are created to apply sorting and filtering
Ex: 
launches/json?filter_field=date_utc&filter_value=2022&sort_low=flight_number
We filter the data that the date_utc is in the 2022 year, and sort it from the first flight to the last
The request is literally: Filter launches by year 2022 and sort by flight number in format lowest/first to highest/the last.
"""

def apply_sorting(query, model, sort_param, sort_order):
    """
    Apply sorting to the query based on the sort parameter and order.

    Args:
        query (Query): SQLAlchemy query object.
        model (Base): SQLAlchemy model class.
        sort_param (string): The field to sort by.
        sort_order (string): 'asc' for ascending or 'desc' for descending.
        
    Returns:
        Query: Modified query with sorting applied.
    """
    # The user will not be able to sort to the ID
    if sort_param == 'id':
        logger.critical("Sorting by 'id' is not allowed.")
        raise ValueError("Sorting by 'id' is not allowed.")
    
    # Gets the model attribute that corresponds to the sort field. 
    # If the field does not exist in the model, returns None.
    sort_column = getattr(model, sort_param, None)
    
    # Check if the sort field is valid.
    # If the field is not valid, retunr the query without modifications.
    if sort_column is None:
        return query
    
    # Apply ascending sort to the query if the sort order is 'asc' 'desc' in other case.
    if sort_order == 'asc':
        query = query.order_by(asc(sort_column))
    else: 
        query = query.order_by(desc(sort_column))
    return query

def apply_filtering(query, model, filter_field, filter_value):
    """
    Apply filtering to the query based on the filter field and value.
    Args:
        query (Query): SQLAlchemy query object.
        model (Base): SQLAlchemy model class.
        filter_field (str): The field to filter by.
        filter_value (str): The value to filter by.

    Returns:
        Query: Modified query with filtering applied.
    """
    # Gets the model attribute that corresponds to the sort field. 
    # If the field does not exist in the model, returns None.
    filter_column = getattr(model, filter_field, None)
    
    # Check if the sort field is valid.
    # If the field is not valid, retunr the query without modifications.
    if filter_column is None:
        return query

    # Specific filtering for the 'id' field
    if filter_field == 'id':
        query = query.filter(filter_column == filter_value)

    # Apply filter by year if filter value is a digit.
    if filter_value.isdigit():
        query = query.filter(func.extract('year', filter_column) == int(filter_value))
    # Applies the exact filter if the filter value contains a dash (possibly a date).
    elif '-' in filter_value:
       query = query.filter(filter_column == filter_value)
    # Apply the exact filter 
    # if the value is neither a digit nor contains a hyphen (possibly a text string).
    else:
        query = query.filter(filter_column.ilike(f"%{filter_value}%"))
    return query