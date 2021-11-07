"""

This module contains a function performing a simulation of the loan repayment depending on the amount
of loan outstanding, projected annual salaries and inflation rates

"""

from typing import Union
from datetime import date

from annual_monthly_transformers import get_monthly_interest_rate_array, get_monthly_salary_array
from calculations import calculate_monthly_interest, calculate_monthly_installment


def simulate_repayment(loan_outstanding: Union[int, float], annual_rpis: list[float], 
                       annual_salaries: list[int], current_month: Union[str, int] = date.today().month,
                       months_to_relief: int = 360, discretionary_repayments: dict = dict()):
    """
    Simulates the repayment process given the size of the debt outstanding, 
    annual salary projection and the RPI projection. Returns arrays containing:
    - The debt outstanding for each month
    - Interest accumulated for each month
    - The repayment sum for each month

    :param loan_outstanding: The total debt at the beginning of simulation
    :type loan_outstanding: Union[int, float]
    :param annual_rpis: The list of annual RPI projections
    :type annual_rpis: list[float]
    :param annual_salaries: The list of annual salaries projections
    :type annual_salaries: list[int]
    :param current_month: Current month, defaults to date.today().month
    :type current_month: Union[str, int], optional
    :param months_to_relief: The number of months until the debt is written off, defaults to 360
    :type months_to_relief: int, optional
    :param discretionary_repayments: A dictionary of month:amount pairs indicating
        how much additional payment we wish to make, defaults to dict()
    :type discretionary_repayments: dict, optional
    """
    monthly_salaries = get_monthly_salary_array(annual_salaries, current_month)
    monthly_interest_rates = get_monthly_interest_rate_array(annual_salaries, annual_rpis, current_month)

    # lists to store values for each month
    monthly_repayments: list[float] = []
    monthly_interest: list[float] = []
    monthly_balance: list[float] = []

    # iterating through each month up until the debt relief 
    # and updating the outstanding balance along the way
    for i in range(months_to_relief):

        # calculating the interest and installment for a given month
        interest = calculate_monthly_interest(loan_outstanding, monthly_interest_rates[i])
        installment = calculate_monthly_installment(monthly_salaries[i])

        # adding any discretionary repayments to the monthly payment
        if i in discretionary_repayments.keys():
            installment += discretionary_repayments[i]
        
        # making sure the repayment is less than total loan outstanding 
        # and updating the balance based on interest added and repayment made
        repayment = min(installment, loan_outstanding + interest)
        loan_outstanding = loan_outstanding + interest - repayment

        # updating lists
        monthly_repayments.append(repayment)
        monthly_interest.append(interest)
        monthly_balance.append(loan_outstanding)

    return monthly_repayments, monthly_interest, monthly_balance