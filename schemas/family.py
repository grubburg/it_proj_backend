class Family(object):
    def __init__(self, name, token="", members=[], items=[]):
        self.name = name
        self.token = token
        self.members = members
        self.items = items

    @staticmethod
    def from_dict(source):
        family = Family(source[u'name'], source[u'token'],
                        source[u'members'], source[u'items'])
        return family

    def to_dict(self):

        family = {
            u'name':    self.name,
            u'token':   self.token,
            u'members': self.members,
            u'items':   self.items
        }
        return family

    def __repr__(self):
        return (
            u'Family(name={}, token={}, members={}, items={})'.format(
                self.name, self.token, self.members, self.items)
        )
