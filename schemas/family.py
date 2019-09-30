class Family(object):
    def __init__(self, name):
        self.name = name
        self.token = ""
        self.members = []
        self.items = []

    @staticmethod
    def from_dict(source):
        family = Family(source[u'name'])
        return family

    def to_dict(self):

        family = {
                u'name':    self.name,
                u'token':   self.token,
                u'members': self.token,
                u'items':   self.items
                }
        return family
    def __repr__(self):
        return (
                u'Family(name={}, token={}, members={}, items={})'.format(self.name, self.token, self.members, self.items)
                )
