import ast


class Item(object):
    def __init__(self, name, image, description, tags=[], visibility=[]):
        self.name = name
        self.image = image
        self.description = description
        self.tags = tags
        self.visibility = visibility

    @staticmethod
    def from_dict(source):
        item = Item(source[u'name'], source[u'image'],
                    source[u'description'], source[u'tags'], source[u'visibility'])
        return item

    def to_dict(self):
        item = {
            u'name':        self.name,
            u'image':       self.image,
            u'description': self.description,
            u'tags':        self.tags,
            u'visibility':  self.visibility
        }
        return item

    def __repr__(self):
        return(
            u'User(name={}, image={}, description={}, tags={}, visibility={}'.format(
                self.name, self.image, self.description, self.tags, self.visibility)
        )
