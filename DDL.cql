CREATE  KEYSPACE transactions_dulher WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE transactions_dulher;

CREATE TABLE transactions (transaction_id UUID, step int, type text, amount decimal, nameOrig text, oldbalanceOrg decimal, newbalanceOrig decimal, nameDest text,
                           oldbalanceDest decimal, newbalanceDest decimal, isFraud boolean, transaction_date date, PRIMARY KEY (nameOrig, isFraud, transaction_id));

CREATE TABLE amount_only_transactions (transaction_id UUID, amount decimal, nameDest text, transaction_date date, PRIMARY KEY (nameDest, transaction_date, transaction_id));

