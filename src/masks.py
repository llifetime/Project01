def get_mask_card_number(card_numder: str) -> str:
    """Маскирует 6 цифр и номера карты и

    разбивает на 4 блока."""

    masked_card_show = card_numder[:4] + " " + card_numder[4:6] + "**" + " **** " + card_numder[-4:]

    return masked_card_show


def get_mask_account(account_number: str) -> str:
    """
    маскировки номера банковского счета
    :return: замаскированный счет
    """
    account_can_be_show = "**" + account_number[-4:]
    return account_can_be_show


print(get_mask_account("73654108430135874305"))
