def get_mask_card_number(card_number: str) -> str:
    """Маскирует 6 цифр и номера карты и

    разбивает на 4 блока."""

    masked_card_show = card_number[:4] + " " + card_number[4:6] + "**" + " **** " + card_number[-4:]

    # Проверка на пустую строку
    if not card_number:
        return "Неверный номер счета"

    # Проверка, что все символы - цифры
    if not card_number.isdigit():
        return "Неверный номер счета"

    return masked_card_show


def get_mask_account(account_number: str) -> str:
    """
    маскировки номера банковского счета
    :return: замаскированный счет
    """
    account_can_be_show = "**" + account_number[-4:]
    return account_can_be_show


print(get_mask_account("73654108430135874305"))
