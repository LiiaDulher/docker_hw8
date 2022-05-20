import datetime

from cassandra.cluster import Cluster
from cassandra.query import named_tuple_factory
from flask import jsonify, request, Flask


class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)
        self.session.row_factory = named_tuple_factory

    def execute(self, query):
        self.session.execute(query)

    def close(self):
        self.session.shutdown()

    def query1(self, uid):
        """
        Return all transactions for specified *`uid`*(nameOrig) which are fraud
        :param uid: string
        :return: Rows
        """
        query = "SELECT step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, " \
                "newbalanceDest, isFraud, transaction_date FROM transactions WHERE nameOrig='%s' AND isFraud = true"\
                % uid
        rows = self.session.execute(query)
        return rows

    def query2(self, uid):
        """
        Return three transactions for specified *`uid`*(nameOrig) with the most amount
        :param uid: string
        :return: Rows
        """
        query = "SELECT step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, " \
                "newbalanceDest, isFraud, transaction_date FROM transactions WHERE nameOrig='%s'"\
                % uid
        rows = self.session.execute(query)
        return rows

    def query3(self, uid, start_date, end_date):
        """
        Return money amount received by specified *`uid`*(nameDest) from *`start_date`* to *`end_date`*
        :param uid: string
        :param start_date: date in string
        :param end_date: date in string
        :return: Rows
        """
        query = "SELECT amount FROM amount_only_transactions WHERE nameDest='%s' AND transaction_date >= '%s' AND" \
                " transaction_date <= '%s' ALLOW FILTERING" % (uid, start_date, end_date)
        rows = self.session.execute(query)
        return rows


class CassandraAPI:

    def __init__(self, name="CassandraAPI"):
        self.app = Flask(name)
        self.name = name
        self.client = self.create_client()
        self.client.connect()

        @self.app.route('/', methods=['GET'])
        def get_request():
            if request.method == 'GET':
                query_body = request.get_json()
                try:
                    result = self.execute_query(query_body)
                    return jsonify(result)
                except AttributeError as err:
                    return jsonify(err=str(err)), 400

    def run(self, host, port):
        self.app.run(host=host, port=port)

    def __del__(self):
        self.client.close()

    def execute_query(self, query_body):
        if len(query_body.keys()) != 2 or "query_number" not in query_body.keys() or "params" not in query_body.keys():
            raise AttributeError("Wrong body: it should only have fields 'query_number' and 'params'")

        try:
            query_number = int(query_body["query_number"])
        except ValueError:
            raise AttributeError("Wrong query_number: it should be int between 1 and 3")
        if query_number < 1 or query_number > 3:
            raise AttributeError("Wrong query_number: it should be int between 1 and 3")

        params = query_body["params"]
        if 1 <= query_number <= 2:

            if len(params.keys()) != 1 or "uid" not in params.keys():
                raise AttributeError("Wrong params for query %d: it should only have field 'uid'"
                                     % query_number)

            uid = params["uid"]

            if query_number == 1:
                rows = self.client.query1(uid)
            else:
                rows = self.client.query2(uid)

            result_json = {"columns_names": ("step", "type", "amount", "nameOrig", "oldbalanceOrg", "newbalanceOrig",
                                             "nameDest", "oldbalanceDest", "newbalanceDest", "isFraud",
                                             "transaction_date"),
                           "rows": []}
            for row in rows:
                result_json["rows"].append((row.step, row.type, str(row.amount), row.nameorig, str(row.oldbalanceorg),
                                            str(row.newbalanceorig), row.namedest, str(row.oldbalancedest),
                                            str(row.newbalancedest), row.isfraud, str(row.transaction_date)))
            if query_number == 1:
                return result_json
            else:
                result_json["rows"].sort(key=lambda x: x[2], reverse=True)
                result_json["rows"] = result_json["rows"][:3]
                return result_json
        else:
            if len(params.keys()) != 3 or "uid" not in params.keys() or "start_date" not in params.keys() \
                    or "end_date" not in params.keys():
                raise AttributeError("Wrong params for query %d: it should only have fields 'uid', 'start_date' and "
                                     "'end_date'" % query_number)

            start_date = params["start_date"]
            end_date = params["end_date"]
            uid = params["uid"]

            try:
                datetime.datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise AttributeError("Wrong params for query %d: field 'start_date' should be in format 'yyyy-mm-dd'"
                                     % query_number)
            try:
                datetime.datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise AttributeError("Wrong params for query %d: field 'end_date' should be in format 'yyyy-mm-dd'"
                                     % query_number)

            rows = self.client.query3(uid, start_date, end_date)

            result_json = {"columns_names": "total amount",
                           "rows": []}
            result_json["rows"].append(sum([row.amount for row in rows]))

            return result_json

    @staticmethod
    def create_client():
        host = 'cassandra-node'
        port = 9042
        keyspace = 'transactions_dulher'

        client = CassandraClient(host, port, keyspace)
        return client


def main():
    app = CassandraAPI()
    app.run("0.0.0.0", 8080)


if __name__ == '__main__':
    main()
