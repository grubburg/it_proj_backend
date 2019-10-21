class User(object):
    def __init__(self, name, email, image="false", currentfamily="", families=[]):
        self.name = name
        self.image = image
        self.email = email
        self.currentfamily = currentfamily
        self.families = families

    @staticmethod
    def from_dict(source):
        user = User(source[u'name'], source[u'image'], source[u'email'],
                    source[u'currentfamily'], source[u'families'])

        return user

    def to_dict(self):

        user = {
            u'name':            self.name,
            u'image':           self.image,
            u'email':           self.email,
            u'currentfamily':   self.currentfamily,
            u'families':        self.families
        }
        return user

    def __repr__(self):
        return(
            u'User(name={}, image={}, email={}, currentfamily={}, families={})'.format(
                self.name, self.image, self.email, self.currentfamily, self.families)
        )
