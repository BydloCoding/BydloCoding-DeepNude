from SDK.database import Struct, ProtectedProperty
class User(Struct):
    def __init__(self, *args, **kwargs):
        self.table_name = ProtectedProperty("users")
        self.save_by = ProtectedProperty("user_id")
        self.user_id = 0
        self.balance = 0
        super().__init__(*args, **kwargs)