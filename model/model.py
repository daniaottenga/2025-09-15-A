import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMap = {}
        self._optPath = []
        self._optCost = 10000000000000
        self._driversOrdinati = None
        self._flag = False


    def getAllAnni(self):
        return DAO.getAllAnni()


    def creaGrafo(self, inizio, fine):
        self._graph.clear()

        self._nodes = DAO.getPiloti(inizio, fine)
        self._graph.add_nodes_from(self._nodes)

        for n in self._nodes:
            self._idMap[n.driverId] = n

        edges = DAO.getEdges(inizio, fine, self._idMap) # (driver1, driver2) => peso

        for drivers, peso in edges.items():
            self._graph.add_edge(drivers[0], drivers[1], weight=peso)


    def getNumNodi(self):
        return len(self._nodes)


    def getNumArchi(self):
        return len(self._graph.edges)


    def getTop3(self):
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:3]


    def getCompConnessa(self):
        num = len([len(c) for c in sorted(nx.connected_components(self._graph), key=len, reverse=True)])
        largestCC = max(nx.connected_components(self._graph), key=len)
        ordinata = sorted(largestCC, key=self._graph.degree, reverse=True)

        ris = []
        for o in ordinata:
            ris.append((o, self._graph.degree(o)))

        return num, largestCC, ris


    def getRange(self, num):
        self._optPath = []
        self._optCost = 10000000000000
        self._flag = False
        self._driversOrdinati = sorted(self._nodes, key=lambda x: x.dob) # piloti ordinati dal più grande al più piccolo

        for d in self._driversOrdinati:
            parziale = [d]
            self.ricorsione(parziale, num)
            parziale.pop()

        return self._optPath, self._optCost


    def ricorsione(self, parziale, num):
        if len(parziale) == num:
            if self.rangeEta(parziale) < self._optCost: # non posso aggiungere piloti
                self._optPath = copy.deepcopy(parziale)
                self._optCost = self.rangeEta(parziale)
                self._flag = True

        else:
            for d in self._driversOrdinati:
                if d.dob < parziale[-1].dob or d in parziale:
                    continue

                if self._flag:
                    self._flag = False
                    break

                elif self.controlloConnessione(parziale, d):
                    parziale.append(d)
                    self.ricorsione(parziale, num)
                    parziale.pop()


    def rangeEta(self, parziale):
        return (parziale[-1].dob - parziale[0].dob).days


    def controlloConnessione(self, parziale, d):
        for elem in parziale:
            if self._graph.has_edge(elem, d) or self._graph.has_edge(d, elem):
                return False
            else:
                continue
        return True

