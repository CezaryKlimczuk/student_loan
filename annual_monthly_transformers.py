"""

Module containing function transforming array containing annual data into
monthly arrays, taking into account pay and interest rate review, as well
as scaling amounts into monthly equivalents

"""

from typing import Union
from numpy import array, cumprod
from datetime import date

from helpers import calculate_months_difference, extrapolate_array
from calculations import calculate_annual_interest_rate


RELIEF_PERDIOD = 30 # Years until the debt is written off in full


def get_monthly_interest_rate_array(annual_salaries: list[int], 
                                     annual_rpis: list[float],
                                     current_month: Union[str, int]) -> list[float]:
    """
    Calculates the vector of monthly interest rates by which the total debt will increase each month.
    The total debt has monthly capitalization meaning its sum will increase on a monthly basis.

    :param annual_salaries: A vector of projected salaries in the following years
        (if less than 30 items passed, the last one will be extrapolated)
    :type annual_salaries: list[int]
    :param annual_rpis: A vector of projected inflation rates in the following years
        (if less than 30 items passed, the last one will be extrapolated)
    :type annual_rpis: list[float]
    :param current_month: Current month
    :type current_month: Union[str, int]

    """
    # Extrapolating salary and rpi vectors towards the end of the relief period
    annual_salaries = extrapolate_array(annual_salaries, RELIEF_PERDIOD + 1)
    annual_rpis = extrapolate_array(annual_rpis, RELIEF_PERDIOD + 1)

    # calculating the interest rate for each year of repayment
    # for details, see *calculate_annual_interest_rate()*
    annual_interest_rates: list[float] = []
    for i in range(RELIEF_PERDIOD + 1):
        annual_interest_rate = calculate_annual_interest_rate(annual_salaries[i], annual_rpis[i])
        annual_interest_rates.append(annual_interest_rate)

    # calculating the monthly rate for each month
    monthly_interest_rates: list[float] = []

    # the first interest rate is valid only up until the next september
    months_to_sept = calculate_months_difference(current_month, 'september')
    monthly_interest_rates += months_to_sept * [annual_interest_rates[0] / 12]

    # the next interest rates are valid for the whole year
    for interest_rate in annual_interest_rates[1:]:
        monthly_interest_rates += 12 * [interest_rate / 12]
    
    return monthly_interest_rates


def get_monthly_salary_array(annual_salaries: list[int], 
                             current_month: Union[str, int],
                             salary_revision_month: Union[str, int] = 'april') -> list[float]:
    """
    Calculates the vector of monthly salaries based on annual salary figures given

    :param annual_salaries: A vector of projected salaries in the following years
        (if less than 30 items passed, the last one will be extrapolated)
    :type annual_salaries: list[int]
    :param current_month: Current month
    :type current_month: Union[str, int]
    :param salary_revision_month: The month at which the pay is revised, defaults to 'april'
    :type salary_revision_month: Union[str, int], optional
    """
    # extrapolating salary and rpi vectors
    if len(annual_salaries) < RELIEF_PERDIOD + 1:
        annual_salaries += (RELIEF_PERDIOD - len(annual_salaries) + 1) * [annual_salaries[-1]]

    # calculating monthly salaries before tax
    monthly_salaries: list[int, float] = []

    # the first interest rate is valid only up until the next pay review month
    months_to_pay_review = calculate_months_difference(current_month, salary_revision_month)
    monthly_salaries += months_to_pay_review * [annual_salaries[0] / 12]

    # the next salaries are valid for the whole year
    for annual_salary in annual_salaries[1:]:
        monthly_salaries += 12 * [annual_salary / 12]
    
    return monthly_salaries
    

def get_monthly_discount_factor(annual_rpis: list[float],
                                current_month: Union[str, int] = date.today().month) -> list[float]:
    """
    Calculates the Present Value (PV) discount factor for each month since the beginning of the repayment period.
    E.g. calculates how much should the money 20 months from now be scaled to arrive at the PV

    :param annual_rpis: A vector of projected inflation rates in the following years
        (if less than 30 items passed, the last one will be extrapolated)
    :type annual_rpis: list[float]
    :param current_month: Current month
    :type current_month: Union[str, int]
    """
    annual_rpis = extrapolate_array(annual_rpis, RELIEF_PERDIOD + 1)

    # calculating monthly RPI for each month
    monthly_rpis: list[float] = []

    # the RPI will only be valid until the next september
    months_to_sept = calculate_months_difference(current_month, 'september')
    monthly_rpis += months_to_sept * [annual_rpis[0] / 12]

    # the next RPI metrics are valid for the whole year
    for annual_rpi in annual_rpis[1:]:
        monthly_rpis += 12 * [annual_rpi / 12]

    # as RPIs are given in %'s, let's convert to scalars
    monthly_rpis = 1 + array(monthly_rpis) / 100

    # calculating the cumulative product (PV discount factor for each month)
    monthly_discount_factors = list(cumprod(monthly_rpis))
    
    return monthly_discount_factors