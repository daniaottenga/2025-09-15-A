import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDAnno(self):
        anni = self._model.getAllAnni()
        anniDD = list(map(lambda x: ft.dropdown.Option(x), anni))
        self._view._ddAnno1.options = anniDD
        self._view._ddAnno2.options = anniDD

        self._view.update_page()


    def handleCreaGrafo(self,e):
        self._view.txt_result.controls.clear()

        if self._view._ddAnno1.value is None:
            self._view.create_alert("Errore, inserisci un anno di inizio")
            self._view.update()
            return

        if self._view._ddAnno2.value is None:
            self._view.create_alert("Errore, inserisci un anno di fine")
            self._view.update()
            return

        self._model.creaGrafo(self._view._ddAnno1.value, self._view._ddAnno2.value)

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color = "green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._btnstampa.disabled = False
        self._view._btnCerca.disabled = False

        self._view.update_page()


    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore", color="green"))
        top3 = self._model.getTop3()
        for e in top3:
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} -> {e[1]} ({e[2]["weight"]})"))

        lun, topConn, ordinata = self._model.getCompConnessa()

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {lun} componenti connesse",
                                                      color="green"))

        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(topConn)}) nodi",
                                                      color="green"))
        for c in topConn:
            self._view.txt_result.controls.append(ft.Text(f"{c.driverRef} ({c.driverId}) -- DoB: {c.dob}"))

        self._view.txt_result.controls.append(ft.Text(f"Componente connessa in ordine decrescente:",
                                                      color="green"))
        for c in ordinata:
            self._view.txt_result.controls.append(ft.Text(
                f"{c[0].driverRef} ({c[0].driverId}) -- DoB: {c[0].dob} (grado={c[1]})"))

        self._view.update_page()


    def handleCerca(self, e):
        self._view.txt_result.controls.clear()

        try:
            num = int(self._view._txtInK.value)
        except ValueError:
            self._view.create_alert("Errore, inserisci un numero")
            self._view.update_page()
            return

        set, range = self._model.getRange(num)

        if len(set) == 0:
            self._view.txt_result.controls.append(ft.Text(f"Nessun set trovato in questo range", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(
            f"Di seguito il set di piloti trovati con range di età di {range} giorni:", color="green"))

        for c in set:
            self._view.txt_result.controls.append(ft.Text(f"{c.driverRef} ({c.driverId}) -- DoB: {c.dob}"))

        self._view.update_page()


