"""
Module containing functions calculating key metrics such as interest rate,
interest payments and installments
"""

from typing import Union


LOWER_INCOME_THRESHOLD = 27295 # Threshold above which the interest is calculated
UPPER_INCOME_THRESHOLD = 49130 # Threshold above which annualized interest reaches maximum
INTEREST_PREMIUM = 3.0 # Maximum precentage premium by which the interest can increase 
STUDENT_TAX = 9.0 # Percentage of salary above the threshold deducted


def calculate_annual_interest_rate(base_salary: Union[int, float], rpi: float, max_interest_cap: float = None) -> float:
    """
    Calculates the annual interest rate based on the RPI and salary earned.
    The interest rate charged is normally the Retail Price Index plus up to 3%, depending on the annual salary.
    For more info see: https://www.gov.uk/repaying-your-student-loan/what-you-pay

    :param base_salary: Annual salary from the preceding year
    :type base_salary: Union[int, float]
    :param rpi: Retail Price Index as of March on a given year (in %)
    :type rpi: float
    :param max_interest_cap: Max interest rate imposed on a given year (in %), defaults to None
    :type max_interest_cap: float
    :return: Interest rate
    """
    interest_rate = rpi
    if base_salary > LOWER_INCOME_THRESHOLD:
        interest_rate += INTEREST_PREMIUM * min(1, (base_salary - LOWER_INCOME_THRESHOLD) / (UPPER_INCOME_THRESHOLD - LOWER_INCOME_THRESHOLD))
    if max_interest_cap is not None:
        interest_rate = min(interest_rate, max_interest_cap)
    return interest_rate


def calculate_monthly_installment(monthly_salary: float) -> float:
    """
    Calculates the monthly installment amount. The installment amount is equal to 
    9% of the salary earned above the minium threshold.
    For more info see: https://www.gov.uk/repaying-your-student-loan/what-you-pay

    :param monthly_salary: Monthly salary
    :type monthly_salary: float
    """
    taxable_salary = max(0, monthly_salary - LOWER_INCOME_THRESHOLD / 12)
    return taxable_salary * STUDENT_TAX / 100


def calculate_monthly_interest(total_balance: float, monthly_interest: float) -> float:
    """
    Calcualtes the amount of interest added to the balance each months

    :param total_balance: Total debt left
    :type total_balance: float
    :param monthly_interest: Monthly interest in %
    :type monthly_interest: float
    """
    return total_balance * monthly_interest / 100