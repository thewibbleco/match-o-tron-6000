import codecs
import numpy
import config
import difflib
import json
from config import CATS, EVAL

#BEGINNING OF CLASSES

class Collaborations:

    def __init__(self, DATA):
        self.data = DATA
        self.results = {}
        self.all()

    def all(self):
        for key_a in self.data:
            if DATA[key_a]["Artist:Role"] != "A literary artist / author":
                self.results[key_a] = {}
                for key_b in self.data:
                    if DATA[key_b]["Artist:Role"] == "A literary artist / author":
                        self.results[key_a][key_b] = {}
                        for cat in CATS:
                            dims = self.dimension(self.data[key_a], cat)
                            self.results[key_a][key_b][cat] = self.compare(key_a, key_b, dims)

    def dimension(self, data, dim):
        return [d for d in data if (d.startswith(dim) and d in EVAL)]

    def compare(self, a, b, dims):
        s = {}
        for dim in dims:
            s[dim] = 0
            r = Router().route(dim, self.data[a], self.data[b])
            s[dim] = r
        return s

class Router:

    def __init__(self):
        pass

    @staticmethod
    def route(dim, a, b):
        if dim.startswith("Artist"):
            r = Artist(a, dim).get_score(b)
        if dim.startswith("Topic"):
            r = Topic(dim).get_score(a, b)
        if dim.startswith("Project"):
            r = Project(dim).get_score(a, b)
        if dim.startswith("Sched"):
            r = Schedule(a, b).get_score(dim)
        return r

class Topic:

    def __init__(self, dim):
        self.dim = dim

    def get_score(self, a, b):
        rubric = {'Similar to mine':'A', 'Different than mine':'B', 'No preference':'C'}
        metric_a, metric_b = self.get_metric(a[self.dim]), self.get_metric(b[self.dim])
        similarity = ''.join(sorted(rubric[a["Artist:DifferentSubjects"]] +
                                    rubric[b["Artist:DifferentSubjects"]]))
        if similarity == "AA":
            if metric_a == metric_b:
                return CATS["Topic"]
            else: return 0.0
        elif similarity == "AB":
            return 0.0
        elif similarity == "AC":
            return CATS["Topic"]
        elif similarity == "BB":
            if metric_a == 0 and metric_b > 0:
                return CATS["Topic"]
            else: return 0.0
        elif similarity == "BC":
            if metric_a == 0 and metric_b > 0:
                return CATS["Topic"]
            else: return 0.0
        elif similarity == "CC":
            return CATS["Topic"]
        else:
            #NO REAL POSSIBILITY OF GETTING HERE.
            return (metric_a * metric_b) * CATS["Topic"]

    def get_metric(self, response):
        sum = 0
        rubric = {'Never':0.0, 'Occasionally':.5, 'Frequently':1.0}
        if response: response = response.split(", ")
        else: response = ["Never"]
        for i in range(len(response)):
            sum += rubric[response[i].strip()]
        return sum

class Artist:

    def __init__(self, a, dim):
        self.a = a
        self.dim = dim
        self.trait = dim.split(":")[1]

    def get_score(self, b):
        if self.trait == "Role":
            return self.role(b)
        elif self.trait == "Experimental":
            return self.method(b)
        else:
            return self.differences(b)

    def method(self, b):
        rubric = {'Similar to mine':'A', 'Different than mine':'B', 'No preference':'C'}
        similarity = ''.join(sorted(rubric[self.a["Artist:DifferentStyle"]] +
                                    rubric[b["Artist:DifferentStyle"]]))
        diff = [int(self.a[self.dim]),
                int(b[self.dim])]
        diff = numpy.std(diff)
        if similarity == "AA":
            if diff <= 0.5:
                return float(CATS["Artist"])
            else: return 0.0
        elif similarity == "AB":
            return 0.0
        elif similarity == "AC":
            if diff <= 0.5: return float(CATS["Artist"])
            else: return 0.0
        elif similarity == "BB":
            if diff >= 1.0: float(CATS["Artist"])
            else: return 0.0
        elif similarity == "BC":
            if diff >= 1.0: return float(CATS["Artist"])
            else: return 0.0
        elif similarity == "CC":
            return float(CATS["Artist"])
        else:
            #NO REAL POSSIBILITY OF GETTING HERE.
            return 0.0

class Project:

    def __init__(self, dim):
        self.dim = dim
        self.trait = dim.split(":")[1]

    def get_score(self, a, b):
        similarity = difflib.SequenceMatcher(None, a[self.dim], b[self.dim])
        return similarity.ratio() * CATS["Project"]

class Schedule:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_score(self, dim):
        def parse(dim):
            return [x.strip() for x in str(dim).split(", ")]
        sched_a, sched_b = parse(self.a[dim]), parse(self.b[dim])
        similarity = difflib.SequenceMatcher(None, sched_a, sched_b)
        return similarity.ratio() * CATS["Sched"]

class Metrics:

    def __init__(self):
        pass

    @staticmethod
    def single_score(pool):
        def readable(score):
            score = (score/140) * 100
            score = round(score, 2)
            return str(score) + "%"
        p, w = {}, {}
        for n in pool:
            p[n] = {}
            for cat in CATS:
                p[n][cat] = sum([float(pool[n][cat][dim]) for dim in pool[n][cat]])
            w[n] = readable(sum([p[n][val] for val in p[n]]))
        return w

class Table:

    def __init__(self):
        self.cols = []
        self.rows = {}

    def create(self, data):
        for d in data:
            self.cols.append(d)
            self.rows[d] = Metrics.single_score(data[d])
        return self.format()

    def format(self):
        table = [["NAME"] + sorted([d.encode('utf-8', 'replace')
                                    for d in DATA
                                    if DATA[d]["Artist:Role"] == "A literary artist / author"
                                   ])]
        for col in sorted(self.cols):
            line = [col]
            for match in sorted(self.rows[col]):
                line.append(self.rows[col][match])
            table.append(line)
        return table

#END CLASSES

#OPEN FILE

with open(config.DATA_SOURCE_FILE, 'r') as f:
    contents = f.read()

DATA = json.loads(contents)

#GET DATA OBJECT PARTICIPANT->COLLABORATOR->SCORES BY CATEGORY

collaborations = Collaborations(DATA)
pairings_table = Table().create(collaborations.results)

with codecs.open(config.MATCH_CSV_FILE, "w", encoding="utf8") as f:
    for pairing in pairings_table:
        f.write(', '.join(pairing)+"\r\n")

with codecs.open(config.MATCH_SOURCE_FILE, "w", encoding="Windows-1252") as f:
    json.dump(collaborations.results, f)
