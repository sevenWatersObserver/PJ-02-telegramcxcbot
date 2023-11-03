import requests
import json
import ownerconfig


class APIException(Exception):
    pass


# CurInfoGet - Currency Information Getter
class CurInfoGet:
    # instructed by the documentation to do this
    # this gets ALL the currency data at the time of object creation
    # then parses it to a Python dict
    # good for future expansion of the bot? task only requires 3 currencies
    url = "https://api.currencyapi.com/v3/latest"
    headers = {'apikey': ownerconfig.curapi_token}
    raw_response = requests.request("GET", url, headers=headers)
    saved_parse = json.loads(raw_response.text)

    # function that does the conversion
    @staticmethod
    def get_price(base, quote, amount):
        # here goes the error checker
        if base not in ownerconfig.uik.keys():
            raise APIException("Первая валюта указана неправильно.")
        if quote not in ownerconfig.uik.keys():
            raise APIException("Вторая валюта указана неправильно.")
        try:
            amount = int(amount)
        except Exception:
            raise APIException("Количество введено неправильно. Вводите целые числа.")
        if amount <= 0:
            raise APIException("Количество не должно быть меньше нуля.")
        if base == quote:
            raise APIException("Введённые валюты не должны быть одинаковыми.")
        inbase = CurInfoGet.saved_parse["data"][ownerconfig.uik.get(base)]["value"]
        inquote = CurInfoGet.saved_parse["data"][ownerconfig.uik.get(quote)]["value"]
        # cheeky bit of math, and round to 2 decimals
        result = round(((amount * inquote) / inbase), 2)
        return result


# debugging instance
if __name__ == "__main__":
    test = CurInfoGet
    base = input()
    quote = input()
    amount = input()
    print(CurInfoGet.get_price(base, quote, amount))
