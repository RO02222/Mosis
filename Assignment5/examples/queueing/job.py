class Job:
    def __init__(self, size, creation_time):
        # Jobs have a size and creation_time parameter
        self.size = size
        self.creation_time = creation_time

    def __repr__(self):
        return f"Job(size={self.size},creation_time={self.creation_time})"