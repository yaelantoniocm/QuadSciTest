from helpers.logger import logger
from helpers.query_sort_filter import apply_filtering, apply_sorting
from sqlalchemy.orm import Session
from databases.models import Rockets

def get_filter_sort_rocket(session: Session, sort_param=None, sort_order='asc', filter_field=None, filter_value=None):
    """
    Retrieve rocket data with optional sorting and filtering.

    Args:
        session (Session): SQLAlchemy session object.
        sort_param (str, optional): Field to sort by.
        sort_order (str, optional): Sort order ('asc' or 'desc'). Default is 'asc'.
        filter_field (str, optional): Field to filter by.
        filter_value (str, optional): Value to filter by.

    Returns:
        list: List of rocket data records.
    """
    # Create the sesion for the query
    query = session.query(Rockets)
    
    # Check if both filter parameters are present.
    if (filter_field and not filter_value) or (not filter_field and filter_value):
        logger.error("Both filter_field and filter_value must be provided for filtering.")
        raise ValueError("Both filter_field and filter_value for Rocket must be provided for filtering.")
    # Applies filtering if both the filter field and value are specified.
    if filter_field and filter_value:
        query = apply_filtering(query, Rockets, filter_field, filter_value)
    # Applies the sorting if the sort parameter is specified.
    if sort_param:
        query = apply_sorting(query, Rockets, sort_param, sort_order)
    return query.all()