"""

Module containg helper functions to obtain months difference and 
to extrapolate the array into a given length

"""

from typing import Any, Iterable, Union
from datetime import datetime


def calculate_months_difference(current_month: Union[str, int], target_month: int) -> int:
    """
    The interest rate on the loan is set on 1 September each year, based on the Retail Price Index of the previous March.
    The function returns the number of months until next 

    :param current_month: Expressed as integer or str
    :type current_month: Union[str, int]
    """
    if isinstance(current_month, str):
        current_month = datetime.strptime(current_month, "%B").month
    if isinstance(target_month, str):
        target_month = datetime.strptime(target_month, "%B").month
    months_remaining =  (target_month - current_month) % 12
    
    # If we pass september, we assume the salary is valid for 12 months, not 0
    if months_remaining == 0:
        months_remaining += 12
    return months_remaining


def extrapolate_array(arr: Iterable, length: int) -> Iterable[Any]:
    """
    Extrapolates given array to a desired length based on the last value

    :param arr: Array to extrapolate
    :type arr: Iterable
    :param length: Desired length
    :type length: int
    """
    if len(arr) < length:
        arr += (length - len(arr) + 1) * [arr[-1]]
    return arr