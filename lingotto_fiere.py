import csv

class Stand:
    def __init__(self, codice, metri, padiglione, prezzo):
        self.codice = codice
        self.metri = int(metri)
        self.padiglione = padiglione
        self.prezzo = float(prezzo)
        self._associato = None

    def get_prezzo_finale(self):
        return self.prezzo

    def __str__(self):
        stato = "Disponibile" if self._associato is None else f"associato a {self._associato}"
        return f"{self.codice} : {self.metri}mq, padiglione {self.padiglione}, prezzo {self.prezzo}, {stato}"

    def __lt__(self, other):
        return self.get_prezzo_finale() < other.get_prezzo_finale()

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self._stand = None

    def __str__(self):
        if self._stand is None:
            return f"{self.codice} : {self.nome} {self.cognome}"
        else:
            return f"{self.codice} : {self.nome} {self.cognome}, stand associato {self._stand}"


class Prese(Stand):
    def __init__(self, codice, metri, padiglione, prezzo, prese):
        super().__init__(codice, metri, padiglione, prezzo)
        self.prese = int(prese)

    def get_prezzo_finale(self):
        return self.prezzo * (1 + 0.07 * self.prese)

    def __str__(self):
        stato = "Dispoibile" if self._associato is None else f"associato a {self._associato}"
        prezzo = self.get_prezzo_finale()
        return f"Prese extra {self.codice} : {self.metri}mq, padiglione {self.padiglione}, prezzo {prezzo}, prese extra {self.prese}, {stato}"


class Premium(Stand):
    def __init__(self, codice, metri, padiglione, prezzo, posizione):
        super().__init__(codice, metri, padiglione, prezzo)
        self.posizione = posizione

    def get_prezzo_finale(self):
        return self.prezzo * 1.30

    def __str__(self):
        stato = "Disponibile" if self._associato is None else f"associato a {self._associato}"
        prezzo = self.get_prezzo_finale()
        return f"Premium {self.codice} : {self.metri}mq, padiglione {self.padiglione}, prezzo {prezzo}, posizione {self.posizione}, {stato}"


class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self._stand = {}
        self._espositori = {}

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if not row:
                        continue

                    codice = row[0].strip()

                    if codice.startswith("ES"):
                        nome = row[1].strip()
                        cognome = row[2].strip()
                        espositore = Espositore(codice, nome, cognome)
                        self._espositori[codice] = espositore
                    else:
                        metri = int(row[1].strip())
                        padiglione = row[2].strip()
                        prezzo = float(row[3].strip())
                        if len(row) == 4:
                            stand = Stand(codice, metri, padiglione, prezzo)
                            self._stand[codice] = stand
                        else:
                            extra = row[4].strip()
                            if extra.isdigit():
                                stand = Prese(codice, metri, padiglione, prezzo, extra)
                                self._stand[codice] = stand
                            else:
                                stand = Premium(codice, metri, padiglione, prezzo, extra)
                                self._stand[codice] = stand
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} non trovato")


    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self._stand:
            raise Exception("Codice stand non trovato")
        if codice_espositore not in self._espositori:
            raise Exception("Codice espositore non trovato")

        espositore = self._espositori[codice_espositore]
        if espositore._stand is not None:
            raise Exception(f"L'espositore è gia stato associato allo stand {espositore._stand}")

        stand = self._stand[codice_stand]
        if stand._associato is None:
            stand._associato = codice_espositore
            espositore._associato = True
            espositore._stand = (codice_stand)
        else:
            raise Exception(f"Lo stand è già stato associato all'espositore {stand._associato}")


    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        if self._espositori is None:
            print("Non sono presenti espositori")
            return
        for e in self._espositori.values():
            print(e)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self._stand.values())