from datetime import datetime, timedelta
import requests
import sqlite3
url = "https://v6.exchangerate-api.com/v6/f0c4123dd73731cafac7d7e9/pair/{}/{}"


def convert_currency(amount, from_curency, to_currency):

    response = requests.get(url.format(from_curency, to_currency))
    data = response.json()

    rate = data['conversion_rate'] * amount
    return rate, data


def create_database():
    conn = sqlite3.connect('currency_converter.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversion_history (
            id INTEGER PRIMARY KEY,
            amount REAL,
            from_currency TEXT,
            to_currency TEXT,
            rate REAL,
            timestamp DATETIME 
        )
    ''')
    conn.commit()
    conn.close()


def get_conversion_history():
    conn = sqlite3.connect('currency_converter.db')
    c = conn.cursor()
    c.execute('SELECT * FROM conversion_history ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows


def save_conversion(amount, from_currency, to_currency, rate, timestamp):
    conn = sqlite3.connect('currency_converter.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO conversion_history (amount, from_currency, to_currency, rate,timestamp)
        VALUES (?, ?, ?, ?,?)
    ''', (amount, from_currency, to_currency, rate, timestamp))
    conn.commit()
    conn.close()


def main():
    create_database()

    amount = float(input("Enter amount to convert: "))
    print("------------------")

    from_currency = input("From currency (e.g., USD,INR): ").upper()
    print("------------------")
    to_currency = input("To currency (e.g., EUR,AED): ").upper()
    print("------------------")

    try:
        rate, data = convert_currency(amount, from_currency, to_currency)
    except:
        print("enter currect currency code eg : USD,INR and enter valid amount")
        main()
    timestamp = datetime.now()

    print("CURRENCY CONVERTER")
    print("------------------")

    print(f"{amount} {from_currency} is equal to {rate} {to_currency}")

    print("------------------")

    save_conversion(amount, from_currency, to_currency, rate, timestamp)

    history = get_conversion_history()
    print("conversion history")
    print("------------------")
    for record in history:
        print(record)


if __name__ == "__main__":
    main()
