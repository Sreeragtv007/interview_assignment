import datetime
import requests
import sqlite3

api_key = "f0c4123dd73731cafac7d7e9"
# API URL for currency conversion
url = "https://v6.exchangerate-api.com/v6/{}/pair/{}/{}"


# creating new data base
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
            currency_rate REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# converting currency using external api


def convert_currency(amount, from_curency, to_currency):
    conn = sqlite3.connect('currency_converter.db')
    c = conn.cursor()
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    c.execute('''SELECT * FROM conversion_history WHERE from_currency = ? AND to_currency = ? AND timestamp = ? ''',
              (from_curency, to_currency, date))
    data = c.fetchall()
    c.close()

    if data:
        print("fetched through database for increasing performance")
        print("------------------")
        data = data[-1]
        rate = data[-2] * amount
        return rate

    else:

        response = requests.get(url.format(api_key, from_curency, to_currency))
        data = response.json()
        if data['result'] == "success":

            rate = data['conversion_rate'] * amount
            print('fetched through external api')
            print("------------------")

            date = datetime.datetime.now().strftime("%d/%m/%Y")
            save_conversion(amount, from_curency, to_currency,
                            rate, data['conversion_rate'], date)
            return rate
        else:
            print(
                "invalid currency code  please enter valid currency code like AED,USD,EUR,INR")
 
            return False


# fetching saved data from data base
def get_conversion_history():
    conn = sqlite3.connect('currency_converter.db')
    c = conn.cursor()
    c.execute(''' SELECT * FROM conversion_history ORDER BY timestamp DESC ''')
    rows = c.fetchall()
    conn.close()
    return rows

# after fetching api converted data are saved to data base


def save_conversion(amount, from_currency, to_currency, rate, currency_rate, date):

    conn = sqlite3.connect('currency_converter.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO conversion_history (amount, from_currency, to_currency, rate,timestamp,currency_rate)
        VALUES (?, ?, ?, ?,?,?)
    ''', (amount, from_currency, to_currency, rate, date, currency_rate))
    conn.commit()
    conn.close()


def main():
    create_database()

    amount = input("Enter amount to convert: ")
    try:
        amount = float(amount)
    except:
        print("enter valid amount")
        print("------------------")
        main()

    print("------------------")

    from_currency = input("From currency (e.g., USD,INR): ").upper()
    print("------------------")
    to_currency = input("To currency (e.g., EUR,AED): ").upper()
    print("------------------")

    rate = convert_currency(amount, from_currency, to_currency)

    if rate != False:

        print("CURRENCY CONVERTER")
        print("------------------")

        print(f"{amount} {from_currency} is equal to {rate} {to_currency}")

        print("------------------")
    else:
        main()

    ans = input("if you want  to see your history YES/NO :").upper()

    if ans == 'YES':
        history = get_conversion_history()

        print("previously searched history")
        print("--------------------")
        for record in history:
            print(record)
            print("--------------------")
        exit()


if __name__ == "__main__":
    main()
