from constants import DepositPlanTypes


def deposit_plan_case(
    deposit_plans,
    customer_portfolios,
    fund_deposits,
):

    # Sort deposit plans to clear one time deposit plan follow by montly deposit plan
    deposit_plans.sort(key=lambda x: x["type"])
    fund_deposit = 0
    count = 0

    while count < len(deposit_plans):
        deposit_plan = deposit_plans[count].copy()
        if deposit_plan["high_risk"] == 0 and deposit_plan["retirement"] == 0:
            # Skip deposit plans if both high risk and retirement is 0
            count += 1
            continue

        while (
            (
                customer_portfolios["high_risk"] != deposit_plan["high_risk"]
                or customer_portfolios["retirement"] != deposit_plan["retirement"]
            )
            and deposit_plan["type"] == DepositPlanTypes.ONE_TIME
        ) or deposit_plan["type"] == DepositPlanTypes.MONTHLY:
            if fund_deposit == 0 and len(fund_deposits) > 0:
                fund_deposit = fund_deposits.pop(0)

            for k, v in customer_portfolios.items():

                remainder = fund_deposit - deposit_plan[k]
                if remainder < 0:
                    allocate_fund_deposit = deposit_plan[k] - abs(remainder)
                else:
                    allocate_fund_deposit = fund_deposit - remainder

                if deposit_plan["type"] == DepositPlanTypes.ONE_TIME:
                    if deposit_plan[k] < customer_portfolios[k] + allocate_fund_deposit:
                        excess_fund = (
                            customer_portfolios[k] + allocate_fund_deposit
                        ) - deposit_plan[k]
                        allocate_fund_deposit = allocate_fund_deposit - excess_fund

                customer_portfolios[k] = customer_portfolios[k] + allocate_fund_deposit
                fund_deposit = fund_deposit - allocate_fund_deposit

            if fund_deposit == 0 and len(fund_deposits) == 0:
                break

        # Ensure the fund deposits is empty
        while (
            len(deposit_plans) == 1
            and deposit_plan["type"] == DepositPlanTypes.ONE_TIME
        ):
            if fund_deposit == 0 and len(fund_deposits) > 0:
                fund_deposit = fund_deposits.pop(0)

            for k, v in customer_portfolios.items():
                remainder = fund_deposit - deposit_plan[k]
                if remainder < 0:
                    allocate_fund_deposit = deposit_plan[k] - abs(remainder)
                else:
                    allocate_fund_deposit = fund_deposit - remainder

                customer_portfolios[k] = customer_portfolios[k] + allocate_fund_deposit
                fund_deposit = fund_deposit - allocate_fund_deposit

            if fund_deposit == 0 and len(fund_deposits) == 0:
                break

        count += 1
    return customer_portfolios
