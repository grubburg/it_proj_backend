class Item(object):
    def __init__(self, name, image, description, tags):
        self.name = name
        self.image = image
        self.description = description
        self.tags = tags
        self.users = []
    
    @staticmethod
    def from_dict(source):
        item = Item(source[u'name'], source[u'image'], source[u'description'], source[u'tags'])
        return item
    
    def to_dict(self):
        item = {
                u'name':        self.name,
                u'image':       self.image,
                u'description': self.description,
                u'tags':        self.tags
                }
        return item

    def __repr__(self):
        return(
                u'User(name={}, image={}, description={}, tags={}'.format(self.name, self.image, self.description, self.tags)
                )
