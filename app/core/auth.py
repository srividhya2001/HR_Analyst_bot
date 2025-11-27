USER_DIVISION_MAP = {
    "manager_infotech": "InfoTech",
    "manager_executive": "Executive",
    "manager_finance": "FinanceAndAccounting",
    "manager_stores": "Stores",
    "manager_hr": "HumanResources",
    "manager_legal": "Legal",
}


def validate_user(user_id: str) -> str:
    """
    Validate the user and return assigned division.
    """
    if not user_id:
        return ""
    key = user_id.strip()
    return USER_DIVISION_MAP.get(key, "")