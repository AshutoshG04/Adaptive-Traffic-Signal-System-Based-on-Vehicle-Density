class QueueEstimator:

    def __init__(self, line_y=300):
        self.line_y = line_y
        self.counted_ids = set()

    def estimate(self, tracked_objects):
        count = 0

        for obj in tracked_objects:
            x1,y1,x2,y2 = obj["bbox"]
            cy = (y1+y2)//2

            if cy > self.line_y:
                if obj["id"] not in self.counted_ids:
                    self.counted_ids.add(obj["id"])
                    count += 1

        return count