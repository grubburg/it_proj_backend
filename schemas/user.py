class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.currentfamily = ""
        self.families = []


    @staticmethod
    def from_dict(source):
        user = User(source[u'name'], source[u'email'])

        return user

    def to_dict(self):

        user = {
                u'name':            self.name,
                u'email':           self.email,
                u'currentfamily':   self.currentfamily
                u'families':        self.families
            }
        return user

    def __repr__(self):
       return(
               u'User(name={}, email={}, currentfamily={}, families={})'.format(self.name,self.email,self.currentfamily,self.families)
               )
