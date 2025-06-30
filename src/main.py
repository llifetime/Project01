from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_card

if __name__ == "__main__":
    print(get_mask_card_number("73654108430135874305"))
    print(get_mask_account("73654108430135874305"))
    print(mask_card("Счет 187893747174714974"))
    print(get_date("2024-03-11T02:26:18.671407"))
