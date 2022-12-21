from constants import DepositPlanTypes
from deposit_plan_case import deposit_plan_case

customer_portfolios = {
    "high_risk": 0,
    "retirement": 0,
}

deposit_plans = [
    {
        "type": DepositPlanTypes.ONE_TIME,
        "high_risk": 10000,
        "retirement": 500,
    },
    {
        "type": DepositPlanTypes.MONTHLY,
        "high_risk": 0,
        "retirement": 100,
    },
]

fund_deposits = [10500, 100]


print(deposit_plan_case(deposit_plans, customer_portfolios, fund_deposits))
