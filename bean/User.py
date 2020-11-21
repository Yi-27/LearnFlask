# 用户类
class User(object):
    
    def __init__(self, name="纪莜", age=22):
        self.name = name
        self.age = age
        
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age
        }

