import datetime

from flask import json

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field


def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.
    """
    # Check if 'financials' exists and is a list
    financials = data.get("financials")
    if not isinstance(financials, list) or not financials:
        return -1  # Return -1 if 'financials' is not a list or is empty

    for index, financial in enumerate(financials):
        if financial.get("nature") == "STANDALONE":
            return index
    return -1  # Return -1 if no standalone financial entry is found


def total_revenue(data: dict, financial_index: int):
    """
    Calculate the total revenue from the financial data at the given index.
    """
    # Check if financial_index is valid
    financials = data.get("financials", [])
    if financial_index < 0 or financial_index >= len(financials):
        return 0  # Return 0 if index is out of range

    financial = financials[financial_index]
    pnl = financial.get("pnl", {}).get("lineItems", {})
    return pnl.get("net_revenue", 0)


def total_borrowing(data: dict, financial_index: int):
    """
    Calculate the total borrowing (long-term + short-term) to revenue ratio.
    """
    financials = data.get("financials", [])
    if financial_index < 0 or financial_index >= len(financials):
        return 0  # Return 0 if index is out of range

    financial = financials[financial_index]
    balance_sheet = financial.get("bs", {})
    total_borrowing = balance_sheet.get("liabilities", {}).get("long_term_borrowings", 0) + \
                      balance_sheet.get("liabilities", {}).get("short_term_borrowings", 0)

    total_revenue_value = total_revenue(data, financial_index)
    if total_revenue_value == 0:
        return 0  # Avoid division by zero

    borrowing_to_revenue = total_borrowing / total_revenue_value
    return borrowing_to_revenue


def iscr(data: dict, financial_index: int):
    """
    Calculate Interest Service Coverage Ratio (ISCR).
    ISCR = (Profit before interest + depreciation + 1) / (Interest + 1)
    """
    financials = data.get("financials", [])
    if financial_index < 0 or financial_index >= len(financials):
        return 0  # Return 0 if index is out of range

    financial = financials[financial_index]
    pnl = financial.get("pnl", {}).get("lineItems", {})

    profit_before_interest = pnl.get("profit_before_interest_and_tax", 0)
    depreciation = pnl.get("depreciation", 0)
    interest = pnl.get("interest", 0)

    # ISCR formula with +1 to avoid division by zero
    return (profit_before_interest + depreciation + 1) / (interest + 1)


def iscr_flag(data: dict, financial_index: int):
    """
    Assign a flag based on ISCR.
    If ISCR >= 2: GREEN flag
    Otherwise: RED flag
    """
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED


def total_revenue_5cr_flag(data: dict, financial_index: int):
    """
    Assign a flag based on total revenue exceeding 50 million (5 crore).
    """
    revenue_value = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue_value >= 50000000 else FLAGS.RED


def borrowing_to_revenue_flag(data: dict, financial_index: int):
    """
    Assign a flag based on the borrowing to revenue ratio.
    If the ratio <= 0.25: GREEN flag
    Otherwise: AMBER flag
    """
    borrowing_to_revenue_ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if borrowing_to_revenue_ratio <= 0.25 else FLAGS.AMBER


# Example usage:
if __name__ == '__main__':
    # Sample data input
    with open('data.json', 'r') as f:
        data = json.load(f)

    # Get the latest financial index
    financial_index = latest_financial_index(data)

    # Calculate total revenue
    revenue = total_revenue(data, financial_index)
    print(f"Total Revenue: {revenue}")

    # Calculate borrowing to revenue ratio and its flag
    borrowing_flag = borrowing_to_revenue_flag(data, financial_index)
    print(f"Borrowing to Revenue Flag: {borrowing_flag}")

    # Check ISCR flag
    iscr_check_flag = iscr_flag(data, financial_index)
    print(f"ISCR Flag: {iscr_check_flag}")

    # Check if total revenue exceeds 5 crore
    revenue_5cr_flag = total_revenue_5cr_flag(data, financial_index)
    print(f"Revenue 5 Crore Flag: {revenue_5cr_flag}")
