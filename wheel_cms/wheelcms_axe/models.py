from django.db import models, IntegrityError
import re

class NodeException(Exception):
    pass

class DuplicatePathException(NodeException):
    pass

class InvalidPathException(NodeException):
    pass

class NodeBase(models.Model):
    ROOT_PATH = ""
    ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789_-"
    MAX_PATHLEN = 20
    POSITION_INTERVAL = 100

    validpathre = re.compile("^[%s]{1,%d}$" % (ALLOWED_CHARS, MAX_PATHLEN))

    path = models.CharField(max_length=MAX_PATHLEN, blank=False, unique=True)
    position = models.IntegerField(default=0)


    class Meta:
        abstract = True

    @classmethod
    def root(cls):
        return cls.objects.get_or_create(path=cls.ROOT_PATH)[0]

    def isroot(self):
        return self.path == self.ROOT_PATH

    def add(self, path, position=-1, after=None, before=None):
        """ handle invalid paths (invalid characters, empty, too long) """
        ## lowercasing is the only normalization we do
        path = path.lower()

        if not self.validpathre.match(path):
            raise InvalidPathException(path)

        children = self.children()
        positions = (c.position for c in self.children())

        if after:
            try:
                afterafter_all = self.childrenq(position__gt=after.position,
                                            order="position")
                afterafter = afterafter_all.get()
                position = (after.position + afterafter.position) / 2
                if position == after.position:
                    ## there's a conflict. the new position will be 
                    ## "after.position + POSITION_INTERVAL", renumber
                    ## everything else
                    position = after.position + self.POSITION_INTERVAL
                    for i, n in enumerate(afterafter_all):
                        n.position = position + ((i + 1) * self.POSITION_INTERVAL)
                        n.save()
                    # XXX self.debug("repositioning children")
            except Node.DoesNotExist:
                ## after is the last childnode
                position = after.position + self.POSITION_INTERVAL
        elif before:
            try:
                beforebefore_all = self.childrenq(position__lt=before.position,
                                            order="position")
                beforebefore = beforebefore_all.reverse().get()
                position = (before.position + beforebefore.position) / 2
                if position == beforebefore.position:
                    ## there's a conflict. the new position will be 
                    ## "before.position", renumber before and everything
                    ## else after it.
                    position = before.position
                    everything_after = self.childrenq(position__gte=before.position,
                                                      order="position")
                    for i, n in enumerate(everything_after):
                        n.position = position + ((i + 1) * self.POSITION_INTERVAL)
                        n.save()
                    # XXX self.debug("repositioning children")
            except Node.DoesNotExist:
                ## before is the first childnode
                position = before.position - self.POSITION_INTERVAL
        elif position == -1:
            if children.count():
                position = max(positions) + self.POSITION_INTERVAL
            else:
                position = 0

        child = self.__class__(path=self.path + "/" + path,
                               position=position)
        try:
            child.save()
            # XXX child.info(action=create)
        except IntegrityError:
            raise DuplicatePathException(path)
        return child

    def parent(self):
        """ return the parent for this node """
        if self.isroot():
            return self
        parentpath, mypath = self.path.rsplit("/", 1)
        parent = self.__class__.objects.get(path=parentpath)
        return parent

    def childrenq(self, order="position", **kw):
        """ return the raw query for children """
        return self.__class__.objects.filter(
                  path__regex="^%s/[%s]+$" % (self.path, self.ALLOWED_CHARS),
                  **kw
                  ).order_by(order)

    def children(self, order="position"):
        return self.childrenq(order=order)

    def __unicode__(self):
        """ readable representation """
        return u"path %s pos %d" % (self.path, self.position)

WHEEL_NODE_BASECLASS = NodeBase
class Node(WHEEL_NODE_BASECLASS):
    pass

class ContentBase(models.Model):
    node = models.OneToOneField(Node, related_name="%(app_label)s_%(class)s_related")
    title = models.TextField(blank=False)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)
    publication = models.DateTimeField(null=True)
    expire = models.DateTimeField(null=True)
    
    type = models.CharField(max_length=20)

    class Meta:
        abstract = True
    @classmethod
    def register_spoke(cls, spoke):
        cls.registry[spoke.content.related_name]

    def spoke(self):
        return getattr(self, self.spoke_registry[self.type].related_name)
    ## owner, ?

WHEEL_CONTENT_BASECLASS = models.Model

class Content(WHEEL_CONTENT_BASECLASS):
    pass

