class QuadTree:
    def __init__(self, dimension = None, *, width = None, height = None):
        if dimension is None and (width is None or height is None):
            raise ValueError("The shape of the quadtree must be specificed")

        if dimension is not None and (width is not None or height is not None):
            raise ValueError("Either provide the shape as a complex number or as width and height, not both")

        if dimension is None:
            dimension = complex(width, height)

        self.dimension = dimension


