import json
from rules import FLAGS, latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag

def financial_analysis(data: dict):
    """
    Main function to analyze financial data and return results.
    
    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    return probe_model_5l_profit(data)

def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.
    
    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    latest_financial_index_value = latest_financial_index(data)

    if latest_financial_index_value == -1:
        return {
            "flags": {
                "TOTAL_REVENUE_5CR_FLAG": FLAGS.WHITE,
                "BORROWING_TO_REVENUE_FLAG": FLAGS.WHITE,
                "ISCR_FLAG": FLAGS.WHITE,
            }
        }  # Return a flag indicating no valid data

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, latest_financial_index_value
    )

    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, latest_financial_index_value
    )

    iscr_flag_value = iscr_flag(data, latest_financial_index_value)

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }

if __name__ == "__main__":
    # Load data from the provided data.json file
    with open("data.json", "r") as file:
        content = file.read()
        # Convert file content to JSON
        data = json.loads(content)
        # Pass the 'data' key from the loaded JSON to the model
        result = financial_analysis(data)
        print(result)
