class CelestialObject:
    def __init__(self, declination,
                 ra,
                 dt,
                 constellation,
                 category,
                 visibilities,
                 imagePath, image):
        super().__init__()
        self.declination = declination
        self.ra = ra
        self.dt = dt
        self.constellation = constellation
        self.category = category
        self.visibilities = visibilities
        self.imagePath = imagePath
        self.image = image
