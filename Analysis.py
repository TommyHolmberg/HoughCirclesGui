

class Analysis:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def distanceBetweenEverySecondCircle(self, circleDetector, filelist):
        circles = circleDetector.accCirclesRaw
        x = []
        y = []
        filea = []
        fileb = []
        x0acc = []
        y0acc = []
        x1acc = []
        y1acc = []
        dist = []
        for i in range(0, len(circles), 2):
            filea.append(filelist[i])
            fileb.append(filelist[i+1])
            x0, y0, r0 = circles[i][0]
            x0acc.append(x0)
            y0acc.append(y0)
            x1, y1, r1 = circles[i+1][0]
            x1acc.append(x1)
            y1acc.append(y1)
            x.append(x1-x0)
            y.append(y1-y0)
            dist.append(((((x1 - x0) ** 2) + ((y1 - y0) ** 2)) ** 0.5))
        return dist




