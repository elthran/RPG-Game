class UseListOn:
    """At some point this will be a decorator that can be added to any class and will
    allow it to use list objects cleanly.
    
    Use:
    MyClass:
        @UseListOn(MyClass, my_list)
        
    should allow me to does
    myclass = MyClass()
    myclass.my_list = [1,2 3]
    and have it stored in the database as a list of BaseListElement's
    
    Oh and it doesn't work yet and may never.
    """
    def __init__(self, cls):
        """Modify class.
        """
        # Add relationship to BaseListElement
        parent = cls.__tablename__
        setattr(BaseListElement, parent + '_id', Column(Integer, ForeignKey(cls.id)))
        
        @hybrid_property
        def get_name(self):
            """Return a list of ids of adjacent locations.
            """
            return [element.value for element in self._name]
            
        @name.setter
        def set_name(self, values):
            """Create list of BaseListElement objects.
            """
            self._name = [BaseListElement(value) for value in values]
        
        #Now how do I pass in a list of names without lossing the value of cls????????
        exit("**********fixme**********")
        for name in listnames:
            setattr(cls, '_' + name, relationship("BaseListElement"))
            setattr(cls, name, get_name)
            setattr(cls, name, set_name)
        self.cls = cls
    
    
    def __call__(self, *args, **kwargs):
        """Return modified class.
        """
        return self.cls