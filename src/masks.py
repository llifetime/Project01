from Logs.logger_config import masks_logger as logger


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


def mask_credit_card(card_number: str) -> str:
    try:
        logger.info(f"Masking credit card: {card_number}")
        # Ваша логика маскирования
        masked = f"{card_number[:4]} **** **** {card_number[-4:]}"
        logger.info(f"Card successfully masked. Result: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Error masking card {card_number}: {str(e)}")
        raise
