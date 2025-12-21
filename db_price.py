import pandas as pd


def get_price() -> str:
    """Return actual price list"""
    spreadsheet_id = "1BrVGUxh_cG2Ym1A7bM8aC1jWegRQjny9"
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"

    df = pd.read_csv(url)
    return df.to_string()  # преобразуем весь DataFrame в строку


if __name__ == "__main__":
    get_price()
