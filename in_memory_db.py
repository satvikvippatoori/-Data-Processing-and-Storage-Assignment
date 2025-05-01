class TransactionError(Exception):
    pass

class InMemoryDB:
    def __init__(self):
        self._main_store = {}  # committed data
        self._transaction_store = None  # uncommitted data
        self._in_transaction = False

    def get(self, key):
        if self._in_transaction and key in self._transaction_store:
            return self._transaction_store[key]
        return self._main_store.get(key)

    def put(self, key, val):
        if not self._in_transaction:
            raise TransactionError("put() called outside of transaction")
        self._transaction_store[key] = val

    def begin_transaction(self):
        if self._in_transaction:
            raise TransactionError("Transaction already in progress")
        self._transaction_store = {}
        self._in_transaction = True

    def commit(self):
        if not self._in_transaction:
            raise TransactionError("commit() called without an active transaction")
        for key, value in self._transaction_store.items():
            self._main_store[key] = value
        self._transaction_store = None
        self._in_transaction = False

    def rollback(self):
        if not self._in_transaction:
            raise TransactionError("rollback() called without an active transaction")
        self._transaction_store = None
        self._in_transaction = False
        
