import requests
import pprint


class Client:
    def __init__(self, url):
        self.url = url
        self.queries = {
            1: [
                {
                    "name": "uid",
                    "help_string": "string with user id"
                }
            ],
            2: [
                {
                    "name": "uid",
                    "help_string": "string with user id"
                }
            ],
            3: [
                {
                    "name": "uid",
                    "help_string": "string with user id"
                },
                {
                    "name": "start_date",
                    "help_string": "date in format yyyy-mm-dd"
                },
                {
                    "name": "end_date",
                    "help_string": "date in format yyyy-mm-dd"
                }
            ]
        }

    def get_request(self):
        query_number = int(input("1: Return all transactions for specified *`uid`*(nameOrig) which are fraud \n"
                                 "2: Return three transactions for specified *`uid`*(nameOrig) with the most amount  \n"
                                 "3: Return money amount received by specified *`uid`*(nameDest) from *`start_date`*"
                                 " to *`end_date`*\n"
                                 "0: exit\n"))
        query_body = {
            "query_number": 0,
            "params": {}
        }
        if query_number == 0:
            return None
        if 0 < query_number < 4:
            query_body["query_number"] = query_number
            for param in self.queries[query_number]:
                p = input("Enter %s (%s):" % (param["name"], param["help_string"]))
                query_body["params"][param["name"]] = p
            return query_body

        raise AttributeError("Wrong query number")

    def send_query(self, query_body):
        try:
            response = requests.get(self.url, json=query_body)
        except requests.exceptions.RequestException as err:
            return 0, err
        return response.status_code, response.json()


def main():
    host = 'http://localhost'
    port = 8080
    url = host + ":" + str(port)
    client = Client(url)
    while True:
        try:
            query_body = client.get_request()
        except AttributeError as err:
            print(err)
            continue
        if query_body is None:
            break
        else:
            pprint.pprint(query_body)
            code, json = client.send_query(query_body)
            print("Code: %d" % code)
            pprint.pprint(json)


if __name__ == "__main__":
    main()
