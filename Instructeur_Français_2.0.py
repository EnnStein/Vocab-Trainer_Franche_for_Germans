from random import shuffle
import time
import sys
from PyQt6.QtWidgets import * #verschiedene Klassen für Oberfläche (Managementsysem, Fenster, Textfelder, Knöpfe, Schreibzeile)
from PyQt6.QtGui import * #Schriftarten, für Bild
from PyQt6.QtCore import * #Klassen für Optik

#Funktionen für Tolleranz; Groß-/Kleinschreibung wird angepasst & "Dächer" intern entfernt
def grossKlein(Text):
    Grossbuchstaben = ["A", "À", "B", "C", "Ç", "D", "E", "É", "È", "Ê", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    Kleinbuchstaben = ["a", "à", "b", "c", "ç", "d", "e", "é", "è", "ê", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    Ausgabe = ""
    for x in Text:
        if x in Grossbuchstaben:
            Ausgabe += Kleinbuchstaben[Grossbuchstaben.index(x)]
        else:
            Ausgabe += x
    return Ausgabe

def ohneDach(Text):
    A = ["À", "à"]
    C = ["Ç", "ç"]
    E = ["É", "È", "Ê", "é", "è", "ê"]
    O = ["Ô", "ô"]
    U = ["Ù", "Û", "ù", "û"]
    Ausgabe = ""
    for x in Text:
        if x in A:
            Ausgabe += "a"
        elif x in E:
            Ausgabe += "e"
        elif x in O:
            Ausgabe += "o"
        elif x in U:
            Ausgabe += "u"
        else:
            Ausgabe += x
    return Ausgabe

#interne Wörterbücher als Listen (ergeben eine virtuelle Tabelle)
Artikel = []
Franzoesisch = []
Deutsch = []
Deutsch_alt = []
Presens_Infinitiv = []
Presens_Je = []
Presens_Tu = []
Presens_Il = []
Presens_Nous = []
Presens_Vous = []
Presens_Ils = []
Imparfait_Infinitiv = []
Imparfait_Je = []
Imparfait_Tu = []
Imparfait_Il = []
Imparfait_Nous = []
Imparfait_Vous = []
Imparfait_Ils = []
Futur_Infinitiv = []
Futur_Je = []
Futur_Tu = []
Futur_Il = []
Futur_Nous = []
Futur_Vous = []
Futur_Ils = []
Conditionnel_Infinitiv = []
Conditionnel_Je = []
Conditionnel_Tu = []
Conditionnel_Il = []
Conditionnel_Nous = []
Conditionnel_Vous = []
Conditionnel_Ils = []
Subjontif_Infinitiv = []
Subjontif_Je = []
Subjontif_Tu = []
Subjontif_Il = []
Subjontif_Nous = []
Subjontif_Vous = []
Subjontif_Ils = []
Passe_Compose_Infinitiv = []
Passe_Compose_Modalverb = []
Passe_Compose_Partizip = []

#Funktion, die setup.txt in Liste überführt
Setup = []
def setupLaden():
    try:
        with open("files/setup.txt", "r", encoding =" utf-8") as f:
            for line in f:
                wort = line.split(" ")
                Setup.append(wort[0])
                Setup.append(wort[1])
                Setup.append(wort[2])
                Setup.append(wort[3])
                Setup.append(wort[4])
                Setup.append(wort[5])
                Setup.append(wort[6])
    except FileNotFoundError:
        print("Datei konnte nicht geladen werden.")

#globale Funktionen, die Wörterbücher von der Datei (.txt) in die globalen Listen überführt
def vokabelnAbfrageLaden(file):

    del Artikel[:]
    del Franzoesisch[:]
    del Deutsch[:]
    del Deutsch_alt[:]
    laden_erfolgriech = False

    try:
        with open(file, "r", encoding = "utf-8") as f:
            for line in f:
                wort = line.split(" ")
                #Artikel
                artikel = wort[0]
                if artikel == "--":
                    artikel = " "
                #Französisch
                franzoesisch = wort[1].strip()
                Franzoesisch_Pruefung = []
                for x in franzoesisch:
                    Franzoesisch_Pruefung.append(x)
                franzoesisch_wort = ""
                for x in Franzoesisch_Pruefung:
                    if x == "_":
                        Franzoesisch_Pruefung[Franzoesisch_Pruefung.index(x)] = " "
                for x in Franzoesisch_Pruefung:
                    franzoesisch_wort += x
                #Deutsch
                deutsch = wort[2].strip()
                Deutsch_Pruefung = []
                for x in deutsch:
                    Deutsch_Pruefung.append(x)
                deutsch_wort = ""
                for x in Deutsch_Pruefung:
                    if x == "_":
                        Deutsch_Pruefung[Deutsch_Pruefung.index(x)] = " "
                for x in Deutsch_Pruefung:
                    deutsch_wort += x
                #Deutsch alternativ
                deutsch_alt = wort[3].strip("\n")
                if deutsch_alt == "--":
                    deutsch_wort_alt = " "
                else:
                    Deutsch_Pruefung_alt = []
                    for x in deutsch_alt:
                        Deutsch_Pruefung_alt.append(x)
                    deutsch_wort_alt = ""
                    for x in Deutsch_Pruefung_alt:
                        if x == "_":
                            Deutsch_Pruefung_alt[Deutsch_Pruefung_alt.index(x)] = " "
                    for x in Deutsch_Pruefung_alt:
                        deutsch_wort_alt += x
                #Einfügen der Vokabeln
                Artikel.append(artikel)
                Franzoesisch.append(franzoesisch_wort)
                Deutsch.append(deutsch_wort)
                Deutsch_alt.append(deutsch_wort_alt)
        laden_erfolgriech = True
        return laden_erfolgriech
    except FileNotFoundError:
        laden_erfolgriech = False
        return laden_erfolgriech

def verbenPresensLaden(file):

    del Presens_Infinitiv[:]
    del Presens_Je[:]
    del Presens_Tu[:]
    del Presens_Il[:]
    del Presens_Nous[:]
    del Presens_Vous[:]
    del Presens_Ils[:]
    laden_erfolgriech = False

    try:
        with open(file, "r", encoding = "utf-8") as f:
            for line in f:
                wort = line.split(" ")
                infinitiv = wort[0]
                je = wort[1].strip()
                tu = wort[2].strip()
                il = wort[3].strip()
                nous = wort[4].strip()
                vous = wort[5].strip()
                ils = wort[6].strip("\n")
                Presens_Infinitiv.append(infinitiv)
                Presens_Je.append(je)
                Presens_Tu.append(tu)
                Presens_Il.append(il)
                Presens_Nous.append(nous)
                Presens_Vous.append(vous)
                Presens_Ils.append(ils)
        laden_erfolgriech = True
        return laden_erfolgriech
    except FileNotFoundError:
        laden_erfolgriech = False
        return laden_erfolgriech

def verbenImparfaitLaden(file):

    del Imparfait_Infinitiv[:]
    del Imparfait_Je[:]
    del Imparfait_Tu[:]
    del Imparfait_Il[:]
    del Imparfait_Nous[:]
    del Imparfait_Vous[:]
    del Imparfait_Ils[:]
    laden_erfolgriech = False

    try:
        with open(file, "r", encoding = "utf-8") as f:
            for line in f:
                wort = line.split(" ")
                infinitiv = wort[0]
                je = wort[1].strip()
                tu = wort[2].strip()
                il = wort[3].strip()
                nous = wort[4].strip()
                vous = wort[5].strip()
                ils = wort[6].strip("\n")
                Imparfait_Infinitiv.append(infinitiv)
                Imparfait_Je.append(je)
                Imparfait_Tu.append(tu)
                Imparfait_Il.append(il)
                Imparfait_Nous.append(nous)
                Imparfait_Vous.append(vous)
                Imparfait_Ils.append(ils)
        laden_erfolgriech = True
        return laden_erfolgriech
    except FileNotFoundError:
        laden_erfolgriech = False
        return laden_erfolgriech

def verbenFuturLaden(file):

    del Futur_Infinitiv[:]
    del Futur_Je[:]
    del Futur_Tu[:]
    del Futur_Il[:]
    del Futur_Nous[:]
    del Futur_Vous[:]
    del Futur_Ils[:]
    laden_erfolgriech = False

    try:
        with open(file, "r", encoding = "utf-8") as f:
            for line in f:
                wort = line.split(" ")
                infinitiv = wort[0]
                je = wort[1].strip()
                tu = wort[2].strip()
                il = wort[3].strip()
                nous = wort[4].strip()
                vous = wort[5].strip()
                ils = wort[6].strip("\n")
                Futur_Infinitiv.append(infinitiv)
                Futur_Je.append(je)
                Futur_Tu.append(tu)
                Futur_Il.append(il)
                Futur_Nous.append(nous)
                Futur_Vous.append(vous)
                Futur_Ils.append(ils)
        laden_erfolgriech = True
        return laden_erfolgriech
    except FileNotFoundError:
        laden_erfolgriech = False
        return laden_erfolgriech

def verbenConditionnelLaden(file):

    del Conditionnel_Infinitiv[:]
    del Conditionnel_Je[:]
    del Conditionnel_Tu[:]
    del Conditionnel_Il[:]
    del Conditionnel_Nous[:]
    del Conditionnel_Vous[:]
    del Conditionnel_Ils[:]
    laden_erfolgriech = False

    try:
        with open(file, "r", encoding = "utf-8") as f:
            for line in f:
                wort = line.split(" ")
                infinitiv = wort[0]
                je = wort[1].strip()
                tu = wort[2].strip()
                il = wort[3].strip()
                nous = wort[4].strip()
                vous = wort[5].strip()
                ils = wort[6].strip("\n")
                Conditionnel_Infinitiv.append(infinitiv)
                Conditionnel_Je.append(je)
                Conditionnel_Tu.append(tu)
                Conditionnel_Il.append(il)
                Conditionnel_Nous.append(nous)
                Conditionnel_Vous.append(vous)
                Conditionnel_Ils.append(ils)
        laden_erfolgriech = True
        return laden_erfolgriech
    except FileNotFoundError:
        laden_erfolgriech = False
        return laden_erfolgriech

def verbenSubjontifLaden(file):

    del Subjontif_Infinitiv[:]
    del Subjontif_Je[:]
    del Subjontif_Tu[:]
    del Subjontif_Il[:]
    del Subjontif_Nous[:]
    del Subjontif_Vous[:]
    del Subjontif_Ils[:]
    laden_erfolgriech = False

    try:
        with open(file, "r", encoding = "utf-8") as f:
            for line in f:
                wort = line.split(" ")
                infinitiv = wort[0]
                je = wort[1].strip()
                tu = wort[2].strip()
                il = wort[3].strip()
                nous = wort[4].strip()
                vous = wort[5].strip()
                ils = wort[6].strip("\n")
                Subjontif_Infinitiv.append(infinitiv)
                Subjontif_Je.append(je)
                Subjontif_Tu.append(tu)
                Subjontif_Il.append(il)
                Subjontif_Nous.append(nous)
                Subjontif_Vous.append(vous)
                Subjontif_Ils.append(ils)
        laden_erfolgriech = True
        return laden_erfolgriech
    except FileNotFoundError:
        laden_erfolgriech = False
        return laden_erfolgriech

def verbenPasseComposeLaden(file):

    del Passe_Compose_Infinitiv[:]
    del Passe_Compose_Modalverb[:]
    del Passe_Compose_Partizip[:]
    laden_erfolgreich = False

    try:
        with open(file, "r", encoding = "utf-8") as f:
            for line in f:
                wort = line.split(" ")
                infinitiv = wort[0]
                hilfsverb = wort[1].strip()
                partizip = wort[2].strip("\n")
                Passe_Compose_Infinitiv.append(infinitiv)
                Passe_Compose_Modalverb.append(hilfsverb)
                Passe_Compose_Partizip.append(partizip)
        laden_erfolgriech = True
        return laden_erfolgriech
    except FileNotFoundError:
        laden_erfolgriech = False
        return laden_erfolgreich

#Startfenster
class Startfenster(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI() #siehe unten
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800) #Größe des Fensters
        self.setWindowTitle("Start") #Bezeichnung
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster() #siehe unten
        self.show() #zeigt sich selbst
    def setUpFenster(self):
        #Titeltext
        Titel_Label = QLabel("Instructeur Français")
        Titel_Label.setFont(QFont("Arial", 44))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Versionslabel
        Version_Label = QLabel("Version 2.0")
        Version_Label.setFont(QFont("Arial", 18))
        Version_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Startknopf
        self.Start_Knopf = QPushButton()
        self.Start_Knopf.clicked.connect(self.start)
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(90, 90))
                self.Start_Knopf.setFixedSize(QSize(100, 100))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(100, 35))

        H_Box = QHBoxLayout() #Layout-Klasse
        D_Flagge_Label = QLabel()
        D_Flagge_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        H_Box.addWidget(D_Flagge_Label)
        V_Box = QVBoxLayout()
        V_Box.addWidget(Titel_Label)
        V_Box.addWidget(Version_Label)
        H_Box.addLayout(V_Box)
        image = "images/Allemagne.png"
        try:
            with open(image):
                pixmap = QPixmap(image).scaled(300,200)
                transform = QTransform()
                transform.rotate(0)
                rotated_pixmap = pixmap.transformed(transform)
                D_Flagge_Label.setPixmap(rotated_pixmap)
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Allemagne.png wurde nicht gefunden.")

        F_Flagge_Label = QLabel()
        F_Flagge_Label.setAlignment(Qt.AlignmentFlag.AlignRight)
        H_Box.addWidget(F_Flagge_Label)
        image = "images/France.png"
        try:
            with open(image):
                pixmap = QPixmap(image).scaled(300,200)
                transform = QTransform()
                transform.rotate(0)
                rotated_pixmap = pixmap.transformed(transform)
                F_Flagge_Label.setPixmap(rotated_pixmap)
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild France wurde nicht gefunden.")
        V_Box = QVBoxLayout()
        V_Box.addLayout(H_Box)
        V_Box.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(V_Box)
    
    def start(self):
        self.hide()
        HM.show()
        #print("Startfenster wurde geschlossen.")

class Hilfefenster(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI() #siehe unten

    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800) #Größe des Fensters
        self.setWindowTitle("Hilfe") #Bezeichnung
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster() #siehe unten

    def setUpFenster(self):
        #Titeltext
        Titel_Label = QLabel("Hilfe")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        intro = "Auf dieser Seite werden für den Nutzer relevante technische Besonderheiten und Fehlerquellen erklärt.\n"
        intro += "Bei besonders anfälligen Stellen finden sich auch 'Hilfe/Anleitung-Knöpfe', die die gleichen Texte enthalten.\n"
        intro += "Sollten Fragen oder Probleme auftreten, hilft der Entwickler gerne."
        Einleitungs_Text = QLabel(intro)
        Einleitungs_Text.setFont(QFont("Arial", 15))
        Einleitungs_Text.setWordWrap(True)
        Einleitungs_Text.setAlignment(Qt.AlignmentFlag.AlignLeft)

        vm_text = "Im Vokabelmenü können .txt-Datei als Wörterbücher ausgewählt werden, indem man den Namen der Datei in das Feld eingibt.\n"
        vm_text += "Achtung: Der vollständige Dateiname (also mit Datentyp .txt) muss angegeben werden, weil sie sonst nicht geladen werden kann.\n"
        vm_text += "Außerdem muss die Datei im Arbeitsverzeichnis gespeichert werden. Das ist in diesem Fall das Verzeichnis mit der .exe-Datei für dieses Programm.\n"
        vm_text += "Die ausgewählte Datei muss per Knopfdruck bestätigt werden, damit sie geladen wird.\n"
        vm_text += "Für Deutsch-Französisch und Französisch-Deutsch wird die gleiche Datei verwendet und wird unter 'einfache Abfrage' eingegeben."
        VM_Text = QLabel(vm_text)
        VM_Text.setFont(QFont("Arial", 15))
        VM_Text.setWordWrap(True)
        VM_Text.setAlignment(Qt.AlignmentFlag.AlignLeft)

        ve_text = "Gib in der Textzeile des Editors den Namen der Datei nach dem Schema '[Dateiname].txt' ein, die geladen werden soll.\n"
        ve_text += "Falls es eine Datei mit dem Namen nicht geben sollte, wird sie automatisch beim Speichern erstellt.\n"
        ve_text += "Der bereits bestehende Text wird nach dem Laden im Schreibbereich angezeigt und kann bearbeitet werden.\n"
        ve_text += "Achte auf das richtige Schema bei der Eingabe.\nBei Vokabeln für die einfache Abfrage gilt: "
        ve_text += "[französischer bestimmter Artikel] [Französisch] [Deutsch] [alternatives Wort auf Deutsch].\n"
        ve_text += "Falls es kein Wort für etwas gibt, schreib '--'. Dies ist aus technischen Gründen notwendig.\n"
        ve_text += "Bei Dateien für Verbformen (außer Passé Composé) gilt: [Infinitiv] [Je-Form] [Tu-Form] [Il/Elle-Form] [Nous-Form] [Vous-Form] [Ils/Elles-Form]."
        ve_text += "Für Passé Composé verwende: [Infinitiv] [Modal-/Hilfsverb] [Partizip]."
        VE_Text = QLabel(ve_text)
        VE_Text.setFont(QFont("Arial", 15))
        VE_Text.setWordWrap(True)
        VE_Text.setAlignment(Qt.AlignmentFlag.AlignLeft)

        absturz = "Abstürze des Programms können aus verschiedenen Gründen auftreten. Hier werden kurz die wahrscheinlichsten Probleme erklärt.\n"
        absturz += "Wenn man selbst erstellte Dateien als Wörterbücher verwendet, ist es möglich, dass sie zum Absturz führen, wenn das Schema"
        absturz += " nicht genau eingehalten wurde.\nSiehe hierfür auch den Hilfe-Text für den Editor."
        absturz += " Auch muss man darauf achten, diese Dateien im Arbeitsverzeichnis zu speichern.\n"
        absturz += "Wenn die .zip-Datei nicht ausgepackt wird, kann es zu Problemen kommen."
        Absturz_Text = QLabel(absturz)
        Absturz_Text.setFont(QFont("Arial", 15))
        Absturz_Text.setWordWrap(True)
        Absturz_Text.setAlignment(Qt.AlignmentFlag.AlignLeft)

        Seite_Combo = QComboBox()
        Seite_Combo.setFont(QFont("Arial", 15))
        Seite_Combo.addItems(["Einleitung", "Vokabelmenü", "Vokabeleditor", "Absturz"])
        Seite_Combo.activated.connect(self.seiteAnpassen)

        self.Ende_Knopf = QPushButton("zurück")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        self.Ende_Knopf.clicked.connect(self.ende)

        #Layout
        self.Stacked = QStackedLayout()
        self.Stacked.addWidget(Einleitungs_Text)
        self.Stacked.addWidget(VM_Text)
        self.Stacked.addWidget(VE_Text)
        self.Stacked.addWidget(Absturz_Text)

        VBox = QVBoxLayout()
        VBox.addWidget(Titel_Label)
        VBox.addWidget(Seite_Combo)
        VBox.addLayout(self.Stacked)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(VBox)

    def seiteAnpassen(self, index):
        self.Stacked.setCurrentIndex(index)

    def ende(self):
        self.hide()
        HM.show()

#Mitwirkende
class Mitwirkende(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI() #siehe unten
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800) #Größe & Position des Fensters
        self.setWindowTitle("Mitwirkende") #Bezeichnung
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster() #siehe unten
    def setUpFenster(self):
        Titel_Label = QLabel("Mitwirkende")
        Titel_Label.setFont(QFont("Arial", 40))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        text = "Die Beteiligten wollen unbekannt bleiben.\n"
        text += "Schlange: Python 3.14.2 \n"
        text += "GUI: PyQt6"
        Text_Label = QLabel(text)
        Text_Label.setFont(QFont("Arial", 18))
        self.Ende_Knopf = QPushButton("zurück")
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.clicked.connect(self.ende)
        VBox = QVBoxLayout()
        VBox.addWidget(Titel_Label)
        VBox.addWidget(Text_Label)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox)
        
    def ende(self):
        #print("Mitwirkende-Fenster wurde geschlossen.")
        self.hide()
        HM.show()

#Hauptmenü
class Hauptmenue(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI() #siehe unten
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800) #Größe des Fensters
        self.setWindowTitle("Hauptmenü") #Bezeichnung
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster() #siehe unten
    def setUpFenster(self):
        #Titeltext
        Titel_Label = QLabel("Hauptmenü")
        Titel_Label.setFont(QFont("Arial", 44))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        Abfrage_Label = QLabel("Abfrage-Modi")
        Abfrage_Label.setFont(QFont("Arial", 20))
        Abfrage_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        Weiteres_Label = QLabel("Weiteres")
        Weiteres_Label.setFont(QFont("Arial", 20))
        Weiteres_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.VM_Knopf = QPushButton("Vokabelmenü")
        self.VM_Knopf.setFont(QFont("Arial", 16))
        self.VM_Knopf.setStyleSheet("background-color: lightblue")
        self.VM_Knopf.clicked.connect(self.vm)
        self.VE_Knopf = QPushButton("Vokabeleditor")
        self.VE_Knopf.setFont(QFont("Arial", 16))
        self.VE_Knopf.setStyleSheet("background-color: lightblue")
        self.VE_Knopf.clicked.connect(self.ve)
        self.DF_Knopf = QPushButton("Deutsch-Französisch")
        self.DF_Knopf.setFont(QFont("Arial", 16))
        self.DF_Knopf.clicked.connect(self.df)
        self.DF_Knopf.setStyleSheet("background-color: lightblue")
        self.FD_Knopf = QPushButton("Französisch-Deutsch")
        self.FD_Knopf.setFont(QFont("Arial", 16))
        self.FD_Knopf.setStyleSheet("background-color: lightblue")
        self.FD_Knopf.clicked.connect(self.fd)

        self.Presens_Knopf = QPushButton("Présent")
        self.Presens_Knopf.setFont(QFont("Arial", 16))
        self.Presens_Knopf.setFixedWidth(220)
        self.Presens_Knopf.setStyleSheet("background-color: lightblue")
        self.Presens_Knopf.clicked.connect(self.presens)
        self.Passe_Compose_Knopf = QPushButton("Passé Composé")
        self.Passe_Compose_Knopf.setFont(QFont("Arial", 16))
        self.Passe_Compose_Knopf.setFixedWidth(220)
        self.Passe_Compose_Knopf.setStyleSheet("background-color: lightblue")
        self.Passe_Compose_Knopf.clicked.connect(self.passeCompose)
        self.Imparfait_Knopf = QPushButton("Imparfait")
        self.Imparfait_Knopf.setFont(QFont("Arial", 16))
        self.Imparfait_Knopf.setFixedWidth(220)
        self.Imparfait_Knopf.setStyleSheet("background-color: lightblue")
        self.Imparfait_Knopf.clicked.connect(self.imparfait)
        self.Futur_Knopf = QPushButton("Futur Simple")
        self.Futur_Knopf.setFont(QFont("Arial", 16))
        self.Futur_Knopf.setFixedWidth(220)
        self.Futur_Knopf.setStyleSheet("background-color: lightblue")
        self.Futur_Knopf.clicked.connect(self.futur)
        self.Conditionnel_Knopf = QPushButton("Conditionnel")
        self.Conditionnel_Knopf.setFont(QFont("Arial", 16))
        self.Conditionnel_Knopf.setFixedWidth(220)
        self.Conditionnel_Knopf.setStyleSheet("background-color: lightblue")
        self.Conditionnel_Knopf.clicked.connect(self.conditionnel)
        self.Subjontif_Knopf = QPushButton("Subjontif")
        self.Subjontif_Knopf.setFont(QFont("Arial", 16))
        self.Subjontif_Knopf.setFixedWidth(220)
        self.Subjontif_Knopf.setStyleSheet("background-color: lightblue")
        self.Subjontif_Knopf.clicked.connect(self.subjontif)
        
        self.Hilfe_Knopf = QPushButton("Hilfe")
        self.Hilfe_Knopf.setFont(QFont("Arial", 16))
        self.Hilfe_Knopf.setStyleSheet("background-color: lightblue")
        self.Hilfe_Knopf.setFixedWidth(70)
        self.Hilfe_Knopf.clicked.connect(self.hilfe)
        self.Credits_Knopf = QPushButton("Mitwirkende")
        self.Credits_Knopf.setFont(QFont("Arial", 16))
        self.Credits_Knopf.setStyleSheet("background-color: lightblue")
        self.Credits_Knopf.setFixedWidth(130)
        self.Credits_Knopf.clicked.connect(self.credits)
        self.Beenden_Knopf = QPushButton("Programm beenden")
        self.Beenden_Knopf.setFont(QFont("Arial", 16))
        self.Beenden_Knopf.setStyleSheet("background-color: lightblue")
        self.Beenden_Knopf.clicked.connect(self.beenden)

        #Layout
        V_Box_Haupt = QVBoxLayout()
        V_Box_Haupt.addWidget(Titel_Label)
        V_Box_1 = QVBoxLayout()
        V_Box_1.addWidget(Abfrage_Label)
        V_Box_1.addWidget(self.DF_Knopf)
        V_Box_1.addWidget(self.FD_Knopf)
        V_Box_1.addWidget(self.Presens_Knopf)
        V_Box_1.addWidget(self.Passe_Compose_Knopf)
        V_Box_1.addWidget(self.Imparfait_Knopf)
        V_Box_1.addWidget(self.Futur_Knopf)
        V_Box_1.addWidget(self.Conditionnel_Knopf)
        V_Box_1.addWidget(self.Subjontif_Knopf)
        V_Box_2 = QVBoxLayout()
        V_Box_2.addWidget(Weiteres_Label)
        V_Box_2.addWidget(self.VM_Knopf)
        V_Box_2.addWidget(self.VE_Knopf)
        V_Box_2.addWidget(self.Hilfe_Knopf)
        V_Box_2.addWidget(self.Credits_Knopf)
        H_Box_1 = QHBoxLayout()
        H_Box_1.addLayout(V_Box_1)
        H_Box_1.addLayout(V_Box_2)
        V_Box_Haupt.addLayout(H_Box_1)
        V_Box_Haupt.addWidget(self.Beenden_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(V_Box_Haupt)

    #Methoden; überwiegend zum Aufrufen anderer Fenster
    def credits(self):
        self.hide()
        Credits.show()

    def df(self):
        self.hide()
        DF.show()

    def fd(self):
        self.hide()
        FD.show()

    def presens(self):
        self.hide()
        Presens.show()

    def passeCompose(self):
        self.hide()
        Passe_Compose.show()

    def imparfait(self):
        self.hide()
        Imparfait.show()

    def futur(self):
        self.hide()
        Futur.show()

    def conditionnel(self):
        self.hide()
        Conditionnel.show()

    def subjontif(self):
        self.hide()
        Subjontif.show()

    def ve(self):
        self.hide()
        VE.show()

    def vm(self):
        self.hide()
        VM.show()

    def hilfe(self):
        self.hide()
        Hilfe.show()

    def beenden(self):
        print("Das Programm wurde beendet")
        self.close()

#Deutsch-Französisch
class Deutsch_Franzoesisch_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Deutsch-Französisch Abfrage")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Oberflächenelemente

        #Titel
        Titel_Label = QLabel("Deutsch-Französisch")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Anzeige der zu übersetzenden Vokabel
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 15))

        #Anzeige-Label (fix)
        Deutsch_Label = QLabel("Deutsch:")
        Deutsch_Label.setFont(QFont("Arial", 15))
        Franzoesisch_Label = QLabel("Französisch:")
        Franzoesisch_Label.setFont(QFont("Arial", 15))
        Artikel_Label = QLabel("(Artikel: )")
        Artikel_Label.setFont(QFont("Arial", 15))
        R_F_Label = QLabel("Richtig/Falsch:")
        R_F_Label.setFont(QFont("Arial", 15))
        Rueckmeldungs_Label = QLabel("Rückmeldung:")
        Rueckmeldungs_Label.setFont(QFont("Arial", 15))

        #Felder für Rückmeldung
        self.Richtig_Falsch_Label = QLabel() #richtig/falsch
        self.Richtig_Falsch_Label.setFont(QFont("Arial", 15))
        self.Rueckmeldung_Label = QLabel() #mehr Details zu Fehler
        self.Rueckmeldung_Label.setFont(QFont("Arial", 15))

        #Eingabefelder
        self.Eingabe_Edit = QLineEdit()
        self.Eingabe_Edit.setFont(QFont("Arial", 16))
        self.Eingabe_Edit.setFixedWidth(300)
        self.Eingabe_Edit.setClearButtonEnabled(True)
        self.Eingabe_Edit.setEnabled(False)

        self.Artikel_CB = QComboBox()
        self.Artikel_CB.setMaximumWidth(60)
        self.Artikel_CB.setFont(QFont("Arial", 15))
        self.Artikel_CB.addItem(" ")
        self.Artikel_CB.addItem("le")
        self.Artikel_CB.addItem("la")
        self.Artikel_CB.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png" #Nicht richtig; muss 'Start.png' heißen. Bild wird nicht richtig positioniert.
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        #Bestätigenknopf; löst Prüfung (Methode) aus
        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.clicked.connect(self.startPruefung)
        self.Bestaetigen_Knopf.setEnabled(False)
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")

        #Weitetknopf; nächste Vokabel wird angezeigt; Lösung, um Verbesserungen anbringen zu können
        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setEnabled(False)
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")

        #man kehrt ins voherige Menü zurück
        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")

        #Layout
        Haupt_VBox = QVBoxLayout()
        Form = QFormLayout()
        Haupt_VBox.addWidget(Titel_Label)
        Form.addRow(Deutsch_Label, self.Wort_Label)
        Form.addRow(Franzoesisch_Label, self.Eingabe_Edit)
        Form.addRow(Artikel_Label, self.Artikel_CB)
        Form.addRow(R_F_Label, self.Richtig_Falsch_Label)
        Form.addRow(Rueckmeldungs_Label, self.Rueckmeldung_Label)
        Haupt_VBox.addLayout(Form)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        Haupt_VBox.addLayout(HBox)
        Haupt_VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        Haupt_VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(Haupt_VBox)

        #Tastenkombination
        self.shortcut = QShortcut(QKeySequence("Return"), self)
        self.shortcut.activated.connect(self.startPruefung)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Franzoesisch)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            if Deutsch_alt[self.vokabeln[self.vokabel_index]] == " ":
                text = Deutsch[self.vokabeln[self.vokabel_index]]
            else:
                text = Deutsch[self.vokabeln[self.vokabel_index]] + " oder " + Deutsch_alt[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Eingabe_Edit.setEnabled(True)
            self.Artikel_CB.setEnabled(True)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Eingabe_Edit.setFocus()
            self.gestartet = True

    def startPruefung(self):
        self.pruefen(Artikel, Franzoesisch, Deutsch, Deutsch_alt, self.vokabel_index)
    def pruefen(self, Artikel, Franzoesisch, Deutsch, Deutsch_alt, vokabel_index):
        uebersetzung = self.Eingabe_Edit.text()
        try:
            rueckmeldung = ""
            if Artikel[self.vokabeln[self.vokabel_index]] == " ":
                if uebersetzung == Franzoesisch[self.vokabeln[self.vokabel_index]]:
                    self.Richtig_Falsch_Label.setText("Die Vokabel ist richtig!")
                else:
                    vokabel = ohneDach(Franzoesisch[self.vokabeln[self.vokabel_index]])
                    uebersetzung = ohneDach(uebersetzung)
                    if uebersetzung == vokabel:
                        self.Richtig_Falsch_Label.setText("Die Vokabel ist fast richtig!")
                        rueckmeldung += "Es fehlen die 'Dächer'."
                    else:
                        self.Richtig_Falsch_Label.setText("Die Vokabel ist falsch!")
                        rueckmeldung += "Richtig wäre: " + Franzoesisch[self.vokabeln[self.vokabel_index]]
            else:
                r_f = "" #richtig_falsch (?)
                if uebersetzung == Franzoesisch[self.vokabeln[self.vokabel_index]]:
                    r_f += "Die Vokabel ist richtig!\n"
                else:
                    vokabel = ohneDach(Franzoesisch[self.vokabeln[self.vokabel_index]])
                    uebersetzung = ohneDach(uebersetzung)
                    if uebersetzung == vokabel:
                        r_f += "Die Vokabel ist fast richtig!\n"
                        rueckmeldung += "Es fehlen die sogennanten 'Dächer'.\n"
                    else:
                        r_f += "Die Vokabel ist falsch!\n"
                        rueckmeldung += "Richtig wäre: " + Franzoesisch[self.vokabeln[self.vokabel_index]] + "\n"
                artikel = self.Artikel_CB.currentText()
                if artikel == Artikel[self.vokabeln[self.vokabel_index]]:
                    r_f += "Der Artikel stimmt!"
                else:
                    r_f += "Der Artikel stimmt nicht!"
                    rueckmeldung += "Der richtige Artikel wäre: " + Artikel[self.vokabeln[self.vokabel_index]]
                self.Richtig_Falsch_Label.setText(r_f)
            if rueckmeldung == "":
                rueckmeldung = "Keine Fehler!"
            self.Rueckmeldung_Label.setText(rueckmeldung)
        except IndexError:
            print("Fehler")
        
    def weiter(self):
        self.Eingabe_Edit.clear()
        self.Richtig_Falsch_Label.clear()
        self.Rueckmeldung_Label.clear()
        self.Artikel_CB.setCurrentIndex(0)
        self.vokabel_index += 1
        if (len(Franzoesisch)-1) >= self.vokabel_index:
            if Deutsch_alt[self.vokabeln[self.vokabel_index]] == " ":
                text = Deutsch[self.vokabeln[self.vokabel_index]]
            else:
                text = Deutsch[self.vokabeln[self.vokabel_index]]+ " oder " + Deutsch_alt[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Eingabe_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Vokabeln wurden abgefragt.")
            self.Eingabe_Edit.setEnabled(False)
            self.Artikel_CB.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.gestartet = False
            self.vokabeln = []
            self.vokabel_index = 0
    
    def ende(self):
        #print("Deutsch-Französisch-Abfrage beendet und Fenster geschlossen.")
        self.hide()
        HM.show()

#Französisch-Deutsch
class Franzoesisch_Deutsch_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Französisch-Deutsch Abfrage")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Oberflächenelemente

        #Titel
        Titel_Label = QLabel("Französisch-Deutsch")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Anzeige der zu übersetzenden Vokabel
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 15))

        #Anzeige-Label (fix)
        Deutsch_Label = QLabel("Französisch:")
        Deutsch_Label.setFont(QFont("Arial", 15))
        Franzoesisch_Label = QLabel("Deutsch:")
        Franzoesisch_Label.setFont(QFont("Arial", 15))
        R_F_Label = QLabel("Richtig/Falsch:")
        R_F_Label.setFont(QFont("Arial", 15))
        Rueckmeldungs_Label = QLabel("Rückmeldung:")
        Rueckmeldungs_Label.setFont(QFont("Arial", 15))

        #Felder für Rückmeldung
        self.Richtig_Falsch_Label = QLabel() #richtig/falsch
        self.Richtig_Falsch_Label.setFont(QFont("Arial", 15))
        self.Rueckmeldung_Label = QLabel() #mehr Details zu Fehler
        self.Rueckmeldung_Label.setFont(QFont("Arial", 15))

        #Eingabefelder
        self.Eingabe_Edit = QLineEdit()
        self.Eingabe_Edit.setFont(QFont("Arial", 16))
        self.Eingabe_Edit.setFixedWidth(300)
        self.Eingabe_Edit.setClearButtonEnabled(True)
        self.Eingabe_Edit.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        #Bestätigenknopf; löst Prüfung (Methode) aus
        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.clicked.connect(self.startPruefung)
        self.Bestaetigen_Knopf.setEnabled(False)
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")

        #Weitetknopf; nächste Vokabel wird angezeigt; Lösung, um Verbesserungen anbringen zu können
        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setEnabled(False)
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")

        #man kehrt ins voherige Menü zurück
        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")

        #Layout
        Haupt_VBox = QVBoxLayout()
        Form = QFormLayout()
        Haupt_VBox.addWidget(Titel_Label)
        Form.addRow(Deutsch_Label, self.Wort_Label)
        Form.addRow(Franzoesisch_Label, self.Eingabe_Edit)
        Form.addRow(R_F_Label, self.Richtig_Falsch_Label)
        Form.addRow(Rueckmeldungs_Label, self.Rueckmeldung_Label)
        Haupt_VBox.addLayout(Form)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        Haupt_VBox.addLayout(HBox)
        Haupt_VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        Haupt_VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(Haupt_VBox)

        #Tastenkombination
        self.shortcut = QShortcut(QKeySequence("Return"), self)
        self.shortcut.activated.connect(self.startPruefung)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Deutsch)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            if Artikel[self.vokabeln[self.vokabel_index]] == " ":
                text = Franzoesisch[self.vokabeln[self.vokabel_index]]
            else:
                text = Artikel[self.vokabeln[self.vokabel_index]] + " " + Franzoesisch[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Eingabe_Edit.setEnabled(True)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Eingabe_Edit.setFocus()
            self.gestartet = True

    def startPruefung(self):
        self.pruefen(Artikel, Franzoesisch, Deutsch, Deutsch_alt, self.vokabel_index)
    def pruefen(self, Artikel, Franzoesisch, Deutsch, Deutsch_alt, vokabel_index):
        uebersetzung = self.Eingabe_Edit.text()
        try:
            rueckmeldung = ""
            if Deutsch_alt[self.vokabeln[self.vokabel_index]] == " ":
                if uebersetzung == Deutsch[self.vokabeln[self.vokabel_index]]:
                    self.Richtig_Falsch_Label.setText("Die Vokabel ist richtig!")
                else:
                    vokabel = grossKlein(Deutsch[self.vokabeln[self.vokabel_index]])
                    uebersetzung = grossKlein(uebersetzung)
                    if uebersetzung == vokabel:
                        self.Richtig_Falsch_Label.setText("Die Vokabel ist fast richtig!")
                        rueckmeldung += "Beachte die Groß-/Kleinschreibung."
                    else:
                        self.Richtig_Falsch_Label.setText("Die Vokabel ist falsch!")
                        rueckmeldung += "Richt wäre: " + Deutsch[self.vokabeln[self.vokabel_index]]
            else:
                if uebersetzung == Deutsch[self.vokabeln[self.vokabel_index]] or uebersetzung == Deutsch_alt[self.vokabeln[self.vokabel_index]]:
                    self.Richtig_Falsch_Label.setText("Die Vokabel ist richtig!")
                else:
                    vokabel = grossKlein(Deutsch[self.vokabeln[self.vokabel_index]])
                    vokabel_alt = grossKlein(Deutsch_alt[self.vokabeln[self.vokabel_index]])
                    uebersetzung = grossKlein(uebersetzung)
                    if uebersetzung == vokabel or uebersetzung == vokabel_alt:
                        self.Richtig_Falsch_Label.setText("Die Vokabel ist fast richtig!")
                        rueckmeldung += "Beachte die Groß-/Kleinschreibung."
                    else:
                        self.Richtig_Falsch_Label.setText("Die Vokabel ist falsch!")
                        rueckmeldung += "Richtig wäre: " + Deutsch[self.vokabeln[self.vokabel_index]] + " oder " + Deutsch_alt[self.vokabeln[self.vokabel_index]]
            if rueckmeldung == "":
                rueckmeldung = "Keine Fehler!"
            self.Rueckmeldung_Label.setText(rueckmeldung)
        except IndexError:
            print("Fehler bei Prüfung")
        
    def weiter(self):
        self.Eingabe_Edit.clear()
        self.Richtig_Falsch_Label.clear()
        self.Rueckmeldung_Label.clear()
        self.vokabel_index += 1
        if (len(Deutsch)-1) >= self.vokabel_index:
            if Artikel[self.vokabeln[self.vokabel_index]] == " ":
                text = Franzoesisch[self.vokabeln[self.vokabel_index]]
            else:
                text = Artikel[self.vokabeln[self.vokabel_index]]+ " " + Franzoesisch[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Eingabe_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Vokabeln wurden abgefragt.")
            self.Eingabe_Edit.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.gestartet = False
            self.vokabeln = []
            self.vokabel_index = 0

    def ende(self):
        #print("Französisch-Deutsch-Abfrage beendet und Fenster geschlossen.")
        self.hide()
        HM.show()

#Verben-Modi

#Abfrage Verben im Présent; Rechtschreibung wird aus Fehleranfälligkeit nicht korrigiert
class Verben_Presens_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Verben im Présent")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Titel
        Titel_Label = QLabel("Verben im Présent")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        #Beschreibung
        Beschreibung_Label = QLabel("Unten erscheint, nachdem du 'Start' gedrückt hast, ein Verb. Schreibe in jede Zeile die angepasste Form und drücke auf'bestätigen', wenn alle Formen eingetragen sind.")
        Beschreibung_Label.setFont(QFont("Arial", 16))
        Beschreibung_Label.setWordWrap(True)
        #Anzeige der Vokabel
        Wort_Anzeige_Label = QLabel("Infinitiv:")
        Wort_Anzeige_Label.setFont(QFont("Arial", 16))
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 16))
        
        #weitere Stichworte
        Eingabe_Anzeige_Label = QLabel("Eingabefläche")
        Eingabe_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label = QLabel("Richtig/Falsch")
        R_F_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Verbesserung_Anzeige_Label = QLabel("Verbesserung")
        Verbesserung_Anzeige_Label.setFont(QFont("Arial", 15))
        Verbesserung_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Anzeigen der Pronomen
        Je_Label = QLabel("Je/J':")
        Je_Label.setFont(QFont("Arial", 15))
        Tu_Label = QLabel("Tu:")
        Tu_Label.setFont(QFont("Arial", 15))
        Il_Label = QLabel("Il/Elle/On:")
        Il_Label.setFont(QFont("Arial", 15))
        Nous_Label = QLabel("Nous:")
        Nous_Label.setFont(QFont("Arial", 15))
        Vous_Label = QLabel("Vous:")
        Vous_Label.setFont(QFont("Arial", 15))
        Ils_Label = QLabel("Ils/Elles:")
        Ils_Label.setFont(QFont("Arial", 15))
        
        #Richtig/Falsch-Anzeigen je Pronomen
        self.Je_R_F_Label = QLabel()
        self.Je_R_F_Label.setFont(QFont("Arial", 15))
        self.Tu_R_F_Label = QLabel()
        self.Tu_R_F_Label.setFont(QFont("Arial", 15))
        self.Il_R_F_Label = QLabel()
        self.Il_R_F_Label.setFont(QFont("Arial", 15))
        self.Nous_R_F_Label = QLabel()
        self.Nous_R_F_Label.setFont(QFont("Arial", 15))
        self.Vous_R_F_Label = QLabel()
        self.Vous_R_F_Label.setFont(QFont("Arial", 15))
        self.Ils_R_F_Label = QLabel()
        self.Ils_R_F_Label.setFont(QFont("Arial", 15))
        
        #Labels zur Verbesserung von Fehlern
        self.Je_V_Label = QLabel()
        self.Je_V_Label.setFont(QFont("Arial", 15))
        self.Tu_V_Label = QLabel()
        self.Tu_V_Label.setFont(QFont("Arial", 15))
        self.Il_V_Label = QLabel()
        self.Il_V_Label.setFont(QFont("Arial", 15))
        self.Nous_V_Label = QLabel()
        self.Nous_V_Label.setFont(QFont("Arial", 15))
        self.Vous_V_Label = QLabel()
        self.Vous_V_Label.setFont(QFont("Arial", 15))
        self.Ils_V_Label = QLabel()
        self.Ils_V_Label.setFont(QFont("Arial", 15))
        
        #Zeilen zur Eingabe der Antworten
        breite = 400
        self.Je_Edit = QLineEdit()
        self.Je_Edit.setFont(QFont("Arial", 15))
        self.Je_Edit.setFixedWidth(breite)
        self.Je_Edit.setClearButtonEnabled(True)
        self.Je_Edit.setEnabled(False)
        self.Tu_Edit = QLineEdit()
        self.Tu_Edit.setFont(QFont("Arial", 15))
        self.Tu_Edit.setFixedWidth(breite)
        self.Tu_Edit.setClearButtonEnabled(True)
        self.Tu_Edit.setEnabled(False)
        self.Il_Edit = QLineEdit()
        self.Il_Edit.setFont(QFont("Arial", 15))
        self.Il_Edit.setFixedWidth(breite)
        self.Il_Edit.setClearButtonEnabled(True)
        self.Il_Edit.setEnabled(False)
        self.Nous_Edit = QLineEdit()
        self.Nous_Edit.setFont(QFont("Arial", 15))
        self.Nous_Edit.setFixedWidth(breite)
        self.Nous_Edit.setClearButtonEnabled(True)
        self.Nous_Edit.setEnabled(False)
        self.Vous_Edit = QLineEdit()
        self.Vous_Edit.setFont(QFont("Arial", 15))
        self.Vous_Edit.setFixedWidth(breite)
        self.Vous_Edit.setClearButtonEnabled(True)
        self.Vous_Edit.setEnabled(False)
        self.Ils_Edit = QLineEdit()
        self.Ils_Edit.setFont(QFont("Arial", 15))
        self.Ils_Edit.setFixedWidth(breite)
        self.Ils_Edit.setClearButtonEnabled(True)
        self.Ils_Edit.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.clicked.connect(self.bestaetigen)
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Bestaetigen_Knopf.setEnabled(False)

        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")
        self.Weiter_Knopf.setEnabled(False)

        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        
        #Layout
        VBox = QVBoxLayout()
        VBox.addWidget(Titel_Label)
        VBox.addWidget(Beschreibung_Label)
        Form = QFormLayout()
        Form.addRow(Wort_Anzeige_Label, self.Wort_Label)
        Form.addRow(Je_Label, self.Je_Edit)
        Form.addRow(Tu_Label, self.Tu_Edit)
        Form.addRow(Il_Label, self.Il_Edit)
        Form.addRow(Nous_Label, self.Nous_Edit)
        Form.addRow(Vous_Label, self.Vous_Edit)
        Form.addRow(Ils_Label, self.Ils_Edit)
        Grid = QGridLayout()
        Grid.addWidget(Eingabe_Anzeige_Label, 0, 0)
        Grid.addWidget(R_F_Anzeige_Label, 0, 2)
        Grid.addWidget(self.Je_R_F_Label, 2, 2)
        Grid.addWidget(self.Tu_R_F_Label, 3, 2)
        Grid.addWidget(self.Il_R_F_Label, 4, 2)
        Grid.addWidget(self.Nous_R_F_Label, 5, 2)
        Grid.addWidget(self.Vous_R_F_Label, 6, 2)
        Grid.addWidget(self.Ils_R_F_Label, 7, 2)
        Grid.addWidget(Verbesserung_Anzeige_Label, 0, 3)
        Grid.addWidget(self.Je_V_Label, 2, 3)
        Grid.addWidget(self.Tu_V_Label, 3, 3)
        Grid.addWidget(self.Il_V_Label, 4, 3)
        Grid.addWidget(self.Nous_V_Label, 5, 3)
        Grid.addWidget(self.Vous_V_Label, 6, 3)
        Grid.addWidget(self.Ils_V_Label, 7, 3)
        Grid.addLayout(Form, 1, 0, 7, 2)
        VBox.addLayout(Grid)
        VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        VBox.addLayout(HBox)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Presens_Infinitiv)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            text = Presens_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Je_Edit.setEnabled(True)
            self.Tu_Edit.setEnabled(True)
            self.Il_Edit.setEnabled(True)
            self.Nous_Edit.setEnabled(True)
            self.Vous_Edit.setEnabled(True)
            self.Ils_Edit.setEnabled(True)
            self.Je_Edit.setFocus()
            self.gestartet = True
            
    def bestaetigen(self):
        if self.gestartet == True:
            #Sammlung der Daten
            antwort_je = self.Je_Edit.text()
            antwort_tu = self.Tu_Edit.text()
            antwort_il = self.Il_Edit.text()
            antwort_nous = self.Nous_Edit.text()
            antwort_vous = self.Vous_Edit.text()
            antwort_ils = self.Ils_Edit.text()
            #Prüfung und Ausgabe der Ergebnisse mit eventueller Berichtigung
            if antwort_je == Presens_Je[self.vokabeln[self.vokabel_index]]:
                self.Je_R_F_Label.setText("Richtig!")
                self.Je_V_Label.setText("Kein Fehler!")
            else:
                self.Je_R_F_Label.setText("Falsch!")
                text = Presens_Je[self.vokabeln[self.vokabel_index]]
                self.Je_V_Label.setText(text)
            if antwort_tu == Presens_Tu[self.vokabeln[self.vokabel_index]]:
                self.Tu_R_F_Label.setText("Richtig!")
                self.Tu_V_Label.setText("Kein Fehler!")
            else:
                self.Tu_R_F_Label.setText("Falsch!")
                text = Presens_Tu[self.vokabeln[self.vokabel_index]]
                self.Tu_V_Label.setText(text)
            if antwort_il == Presens_Il[self.vokabeln[self.vokabel_index]]:
                self.Il_R_F_Label.setText("Richtig!")
                self.Il_V_Label.setText("Kein Fehler!")
            else:
                self.Il_R_F_Label.setText("Falsch!")
                text = Presens_Il[self.vokabeln[self.vokabel_index]]
                self.Il_V_Label.setText(text)
            if antwort_nous == Presens_Nous[self.vokabeln[self.vokabel_index]]:
                self.Nous_R_F_Label.setText("Richtig!")
                self.Nous_V_Label.setText("Kein Fehler!")
            else:
                self.Nous_R_F_Label.setText("Falsch!")
                text = Presens_Nous[self.vokabeln[self.vokabel_index]]
                self.Nous_V_Label.setText(text)
            if antwort_vous == Presens_Vous[self.vokabeln[self.vokabel_index]]:
                self.Vous_R_F_Label.setText("Richtig!")
                self.Vous_V_Label.setText("Kein Fehler!")
            else:
                self.Vous_R_F_Label.setText("Falsch!")
                text = Presens_Vous[self.vokabeln[self.vokabel_index]]
                self.Vous_V_Label.setText(text)
            if antwort_ils == Presens_Ils[self.vokabeln[self.vokabel_index]]:
                self.Ils_R_F_Label.setText("Richtig!")
                self.Ils_V_Label.setText("Kein Fehler!")
            else:
                self.Ils_R_F_Label.setText("Falsch!")
                text = Presens_Ils[self.vokabeln[self.vokabel_index]]
                self.Ils_V_Label.setText(text)

    def weiter(self):
        self.Je_Edit.clear()
        self.Je_R_F_Label.clear()
        self.Je_V_Label.clear()
        self.Tu_Edit.clear()
        self.Tu_R_F_Label.clear()
        self.Tu_V_Label.clear()
        self.Il_Edit.clear()
        self.Il_R_F_Label.clear()
        self.Il_V_Label.clear()
        self.Nous_Edit.clear()
        self.Nous_R_F_Label.clear()
        self.Nous_V_Label.clear()
        self.Vous_Edit.clear()
        self.Vous_R_F_Label.clear()
        self.Vous_V_Label.clear()
        self.Ils_Edit.clear()
        self.Ils_R_F_Label.clear()
        self.Ils_V_Label.clear()

        self.vokabel_index += 1
        if (len(Presens_Infinitiv)-1) >= self.vokabel_index:
            text = Presens_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Je_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Verben wurde abgefragt.")
            self.Je_Edit.setEnabled(False)
            self.Tu_Edit.setEnabled(False)
            self.Il_Edit.setEnabled(False)
            self.Nous_Edit.setEnabled(False)
            self.Vous_Edit.setEnabled(False)
            self.Ils_Edit.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.gestartet = False
            self.vokabeln = []
            self.vokabel_index = 0

    def ende(self):
        #print("Verbenfenster wurde geschlossen.")
        self.hide()
        HM.show()

#Passé Composé
class Passe_Compose_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Verben im Passé Composé")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Oberflächenelemente

        #Titel
        Titel_Label = QLabel("Verben im Passé Composé")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Anzeige der zu übersetzenden Vokabel
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 15))

        #Anzeige-Label (fix)
        Infinitiv_Label = QLabel("Infinitiv:")
        Infinitiv_Label.setFont(QFont("Arial", 15))
        Partizip_Label = QLabel("Partizip:")
        Partizip_Label.setFont(QFont("Arial", 15))
        Modal_Label = QLabel("Modalverb")
        Modal_Label.setFont(QFont("Arial", 15))
        R_F_Label = QLabel("Richtig/Falsch:")
        R_F_Label.setFont(QFont("Arial", 15))
        Rueckmeldungs_Label = QLabel("Rückmeldung:")
        Rueckmeldungs_Label.setFont(QFont("Arial", 15))

        #Felder für Rückmeldung
        self.Richtig_Falsch_Label = QLabel() #richtig/falsch
        self.Richtig_Falsch_Label.setFont(QFont("Arial", 15))
        self.Rueckmeldung_Label = QLabel() #mehr Details zu Fehler
        self.Rueckmeldung_Label.setFont(QFont("Arial", 15))

        #Eingabefelder
        self.Eingabe_Edit = QLineEdit()
        self.Eingabe_Edit.setFont(QFont("Arial", 16))
        self.Eingabe_Edit.setFixedWidth(300)
        self.Eingabe_Edit.setClearButtonEnabled(True)
        self.Eingabe_Edit.setEnabled(False)

        self.Modal_CB = QComboBox()
        self.Modal_CB.setMaximumWidth(80)
        self.Modal_CB.setFont(QFont("Arial", 15))
        self.Modal_CB.addItem(" ")
        self.Modal_CB.addItem("être")
        self.Modal_CB.addItem("avoir")
        self.Modal_CB.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        #Bestätigenknopf; löst Prüfung (Methode) aus
        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.clicked.connect(self.startPruefung)
        self.Bestaetigen_Knopf.setEnabled(False)
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")

        #Weitetknopf; nächste Vokabel wird angezeigt; Lösung, um Verbesserungen anbringen zu können
        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setEnabled(False)
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")

        #man kehrt ins voherige Menü zurück
        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")

        #Layout
        Haupt_VBox = QVBoxLayout()
        Form = QFormLayout()
        Haupt_VBox.addWidget(Titel_Label)
        Form.addRow(Infinitiv_Label, self.Wort_Label)
        Form.addRow(Partizip_Label, self.Eingabe_Edit)
        Form.addRow(Modal_Label, self.Modal_CB)
        Form.addRow(R_F_Label, self.Richtig_Falsch_Label)
        Form.addRow(Rueckmeldungs_Label, self.Rueckmeldung_Label)
        Haupt_VBox.addLayout(Form)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        Haupt_VBox.addLayout(HBox)
        Haupt_VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        Haupt_VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(Haupt_VBox)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Passe_Compose_Infinitiv)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            text = Passe_Compose_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Eingabe_Edit.setEnabled(True)
            self.Modal_CB.setEnabled(True)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Eingabe_Edit.setFocus()
            self.gestartet = True

    def startPruefung(self):
        self.pruefen(Passe_Compose_Modalverb, Passe_Compose_Partizip, Passe_Compose_Infinitiv, self.vokabel_index)
    def pruefen(self, Passe_Compose_Modalverb, Passe_Compose_Partizip, Passe_Compose_Infinitiv, vokabel_index):
        uebersetzung = self.Eingabe_Edit.text()
        try:
            r_f = "" #richtig_falsch (?)
            rueckmeldung = ""
            if uebersetzung == Passe_Compose_Partizip[self.vokabeln[self.vokabel_index]]:
                r_f += "Die Partizip ist richtig!\n"
            else:
                vokabel = ohneDach(Passe_Compose_Partizip[self.vokabeln[self.vokabel_index]])
                uebersetzung = ohneDach(uebersetzung)
                if uebersetzung == vokabel:
                    r_f += "Das Partizip ist fast richtig!\n"
                    rueckmeldung += "Es fehlen die sogennanten 'Dächer'.\n"
                else:
                    r_f += "Das Partizip ist falsch!\n"
                    rueckmeldung += "Richtig wäre: " + Passe_Compose_Partizip[self.vokabeln[self.vokabel_index]] + "\n"
            modalverb = self.Modal_CB.currentText()
            if modalverb == Passe_Compose_Modalverb[self.vokabeln[self.vokabel_index]]:
                r_f += "Das Modalverb stimmt!"
            else:
                r_f += "Das Modalberverb stimmt nicht!"
                rueckmeldung += "Das richtige Modalverb wäre: " + Passe_Compose_Modalverb[self.vokabeln[self.vokabel_index]]
            self.Richtig_Falsch_Label.setText(r_f)
            if rueckmeldung == "":
                rueckmeldung = "Keine Fehler!"
            self.Rueckmeldung_Label.setText(rueckmeldung)
        except IndexError:
            print("Fehler")

    def weiter(self):
        self.Eingabe_Edit.clear()
        self.Richtig_Falsch_Label.clear()
        self.Rueckmeldung_Label.clear()
        self.Modal_CB.setCurrentIndex(0)
        self.vokabel_index += 1
        if (len(Passe_Compose_Infinitiv)-1) >= self.vokabel_index:
            text = Passe_Compose_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Eingabe_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Verben wurden abgefragt.")
            self.Eingabe_Edit.setEnabled(False)
            self.Modal_CB.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.vokabel_index = 0
            self.gestartet = False

    def ende(self):
        #print("Passé-Composé-Abfrage beendet und Fenster geschlossen.")
        self.hide()
        HM.show()

#Abfrage Verben im Imparfait (Quiz)
class Verben_Imparfait_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Verben im Imparfait")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Titel
        Titel_Label = QLabel("Verben im Imparfait")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        #Beschreibung
        Beschreibung_Label = QLabel("Unten erscheint, nachdem du 'Start' gedrückt hast, ein Verb. Schreibe in jede Zeile die angepasste Form und drücke auf'bestätigen', wenn alle Formen eingetragen sind.")
        Beschreibung_Label.setFont(QFont("Arial", 16))
        Beschreibung_Label.setWordWrap(True)
        #Anzeige der Vokabel
        Wort_Anzeige_Label = QLabel("Infinitiv:")
        Wort_Anzeige_Label.setFont(QFont("Arial", 16))
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 16))
        
        #weitere Stichworte
        Eingabe_Anzeige_Label = QLabel("Eingabefläche")
        Eingabe_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label = QLabel("Richtig/Falsch")
        R_F_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Verbesserung_Anzeige_Label = QLabel("Verbesserung")
        Verbesserung_Anzeige_Label.setFont(QFont("Arial", 15))
        Verbesserung_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Anzeigen der Pronomen
        Je_Label = QLabel("Je/J':")
        Je_Label.setFont(QFont("Arial", 15))
        Tu_Label = QLabel("Tu:")
        Tu_Label.setFont(QFont("Arial", 15))
        Il_Label = QLabel("Il/Elle/On:")
        Il_Label.setFont(QFont("Arial", 15))
        Nous_Label = QLabel("Nous:")
        Nous_Label.setFont(QFont("Arial", 15))
        Vous_Label = QLabel("Vous:")
        Vous_Label.setFont(QFont("Arial", 15))
        Ils_Label = QLabel("Ils/Elles:")
        Ils_Label.setFont(QFont("Arial", 15))
        
        #Richtig/Falsch-Anzeigen je Pronomen
        self.Je_R_F_Label = QLabel()
        self.Je_R_F_Label.setFont(QFont("Arial", 15))
        self.Tu_R_F_Label = QLabel()
        self.Tu_R_F_Label.setFont(QFont("Arial", 15))
        self.Il_R_F_Label = QLabel()
        self.Il_R_F_Label.setFont(QFont("Arial", 15))
        self.Nous_R_F_Label = QLabel()
        self.Nous_R_F_Label.setFont(QFont("Arial", 15))
        self.Vous_R_F_Label = QLabel()
        self.Vous_R_F_Label.setFont(QFont("Arial", 15))
        self.Ils_R_F_Label = QLabel()
        self.Ils_R_F_Label.setFont(QFont("Arial", 15))
        
        #Labels zur Verbesserung von Fehlern
        self.Je_V_Label = QLabel()
        self.Je_V_Label.setFont(QFont("Arial", 15))
        self.Tu_V_Label = QLabel()
        self.Tu_V_Label.setFont(QFont("Arial", 15))
        self.Il_V_Label = QLabel()
        self.Il_V_Label.setFont(QFont("Arial", 15))
        self.Nous_V_Label = QLabel()
        self.Nous_V_Label.setFont(QFont("Arial", 15))
        self.Vous_V_Label = QLabel()
        self.Vous_V_Label.setFont(QFont("Arial", 15))
        self.Ils_V_Label = QLabel()
        self.Ils_V_Label.setFont(QFont("Arial", 15))
        
        #Zeilen zur Eingabe der Antworten
        breite = 400
        self.Je_Edit = QLineEdit()
        self.Je_Edit.setFont(QFont("Arial", 15))
        self.Je_Edit.setFixedWidth(breite)
        self.Je_Edit.setClearButtonEnabled(True)
        self.Je_Edit.setEnabled(False)
        self.Tu_Edit = QLineEdit()
        self.Tu_Edit.setFont(QFont("Arial", 15))
        self.Tu_Edit.setFixedWidth(breite)
        self.Tu_Edit.setClearButtonEnabled(True)
        self.Tu_Edit.setEnabled(False)
        self.Il_Edit = QLineEdit()
        self.Il_Edit.setFont(QFont("Arial", 15))
        self.Il_Edit.setFixedWidth(breite)
        self.Il_Edit.setClearButtonEnabled(True)
        self.Il_Edit.setEnabled(False)
        self.Nous_Edit = QLineEdit()
        self.Nous_Edit.setFont(QFont("Arial", 15))
        self.Nous_Edit.setFixedWidth(breite)
        self.Nous_Edit.setClearButtonEnabled(True)
        self.Nous_Edit.setEnabled(False)
        self.Vous_Edit = QLineEdit()
        self.Vous_Edit.setFont(QFont("Arial", 15))
        self.Vous_Edit.setFixedWidth(breite)
        self.Vous_Edit.setClearButtonEnabled(True)
        self.Vous_Edit.setEnabled(False)
        self.Ils_Edit = QLineEdit()
        self.Ils_Edit.setFont(QFont("Arial", 15))
        self.Ils_Edit.setFixedWidth(breite)
        self.Ils_Edit.setClearButtonEnabled(True)
        self.Ils_Edit.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.clicked.connect(self.bestaetigen)
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Bestaetigen_Knopf.setEnabled(False)

        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")
        self.Weiter_Knopf.setEnabled(False)

        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        
        #Layout
        VBox = QVBoxLayout()
        VBox.addWidget(Titel_Label)
        VBox.addWidget(Beschreibung_Label)
        Form = QFormLayout()
        Form.addRow(Wort_Anzeige_Label, self.Wort_Label)
        Form.addRow(Je_Label, self.Je_Edit)
        Form.addRow(Tu_Label, self.Tu_Edit)
        Form.addRow(Il_Label, self.Il_Edit)
        Form.addRow(Nous_Label, self.Nous_Edit)
        Form.addRow(Vous_Label, self.Vous_Edit)
        Form.addRow(Ils_Label, self.Ils_Edit)
        Grid = QGridLayout()
        Grid.addWidget(Eingabe_Anzeige_Label, 0, 0)
        Grid.addWidget(R_F_Anzeige_Label, 0, 2)
        Grid.addWidget(self.Je_R_F_Label, 2, 2)
        Grid.addWidget(self.Tu_R_F_Label, 3, 2)
        Grid.addWidget(self.Il_R_F_Label, 4, 2)
        Grid.addWidget(self.Nous_R_F_Label, 5, 2)
        Grid.addWidget(self.Vous_R_F_Label, 6, 2)
        Grid.addWidget(self.Ils_R_F_Label, 7, 2)
        Grid.addWidget(Verbesserung_Anzeige_Label, 0, 3)
        Grid.addWidget(self.Je_V_Label, 2, 3)
        Grid.addWidget(self.Tu_V_Label, 3, 3)
        Grid.addWidget(self.Il_V_Label, 4, 3)
        Grid.addWidget(self.Nous_V_Label, 5, 3)
        Grid.addWidget(self.Vous_V_Label, 6, 3)
        Grid.addWidget(self.Ils_V_Label, 7, 3)
        Grid.addLayout(Form, 1, 0, 7, 2)
        VBox.addLayout(Grid)
        VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        VBox.addLayout(HBox)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Imparfait_Infinitiv)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            self.gestartet = True
            text = Imparfait_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Je_Edit.setEnabled(True)
            self.Tu_Edit.setEnabled(True)
            self.Il_Edit.setEnabled(True)
            self.Nous_Edit.setEnabled(True)
            self.Vous_Edit.setEnabled(True)
            self.Ils_Edit.setEnabled(True)
            self.Je_Edit.setFocus()
            
    def bestaetigen(self):
        if self.gestartet == True:
            #Sammlung der Daten
            antwort_je = self.Je_Edit.text()
            antwort_tu = self.Tu_Edit.text()
            antwort_il = self.Il_Edit.text()
            antwort_nous = self.Nous_Edit.text()
            antwort_vous = self.Vous_Edit.text()
            antwort_ils = self.Ils_Edit.text()
            #Prüfung und Ausgabe der Ergebnisse mit eventueller Berichtigung
            if antwort_je == Imparfait_Je[self.vokabeln[self.vokabel_index]]:
                self.Je_R_F_Label.setText("Richtig!")
                self.Je_V_Label.setText("Kein Fehler!")
            else:
                self.Je_R_F_Label.setText("Falsch!")
                text = Imparfait_Je[self.vokabeln[self.vokabel_index]]
                self.Je_V_Label.setText(text)
            if antwort_tu == Imparfait_Tu[self.vokabeln[self.vokabel_index]]:
                self.Tu_R_F_Label.setText("Richtig!")
                self.Tu_V_Label.setText("Kein Fehler!")
            else:
                self.Tu_R_F_Label.setText("Falsch!")
                text = Imparfait_Tu[self.vokabeln[self.vokabel_index]]
                self.Tu_V_Label.setText(text)
            if antwort_il == Imparfait_Il[self.vokabeln[self.vokabel_index]]:
                self.Il_R_F_Label.setText("Richtig!")
                self.Il_V_Label.setText("Kein Fehler!")
            else:
                self.Il_R_F_Label.setText("Falsch!")
                text = Imparfait_Il[self.vokabeln[self.vokabel_index]]
                self.Il_V_Label.setText(text)
            if antwort_nous == Imparfait_Nous[self.vokabeln[self.vokabel_index]]:
                self.Nous_R_F_Label.setText("Richtig!")
                self.Nous_V_Label.setText("Kein Fehler!")
            else:
                self.Nous_R_F_Label.setText("Falsch!")
                text = Imparfait_Nous[self.vokabeln[self.vokabel_index]]
                self.Nous_V_Label.setText(text)
            if antwort_vous == Imparfait_Vous[self.vokabeln[self.vokabel_index]]:
                self.Vous_R_F_Label.setText("Richtig!")
                self.Vous_V_Label.setText("Kein Fehler!")
            else:
                self.Vous_R_F_Label.setText("Falsch!")
                text = Imparfait_Vous[self.vokabeln[self.vokabel_index]]
                self.Vous_V_Label.setText(text)
            if antwort_ils == Imparfait_Ils[self.vokabeln[self.vokabel_index]]:
                self.Ils_R_F_Label.setText("Richtig!")
                self.Ils_V_Label.setText("Kein Fehler!")
            else:
                self.Ils_R_F_Label.setText("Falsch!")
                text = Imparfait_Ils[self.vokabeln[self.vokabel_index]]
                self.Ils_V_Label.setText(text)

    def weiter(self):
        self.Je_Edit.clear()
        self.Je_R_F_Label.clear()
        self.Je_V_Label.clear()
        self.Tu_Edit.clear()
        self.Tu_R_F_Label.clear()
        self.Tu_V_Label.clear()
        self.Il_Edit.clear()
        self.Il_R_F_Label.clear()
        self.Il_V_Label.clear()
        self.Nous_Edit.clear()
        self.Nous_R_F_Label.clear()
        self.Nous_V_Label.clear()
        self.Vous_Edit.clear()
        self.Vous_R_F_Label.clear()
        self.Vous_V_Label.clear()
        self.Ils_Edit.clear()
        self.Ils_R_F_Label.clear()
        self.Ils_V_Label.clear()

        self.vokabel_index += 1
        if (len(Imparfait_Infinitiv)-1) >= self.vokabel_index:
            text = Imparfait_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Je_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Verben wurde abgefragt.")
            self.Je_Edit.setEnabled(False)
            self.Tu_Edit.setEnabled(False)
            self.Il_Edit.setEnabled(False)
            self.Nous_Edit.setEnabled(False)
            self.Vous_Edit.setEnabled(False)
            self.Ils_Edit.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.gestartet = False
            self.vokabeln = []
            self.vokabel_index = 0

    def ende(self):
        #print("Verbenfenster wurde geschlossen.")
        self.hide()
        HM.show()

#Abfrage Verben im Futur Simple (Quiz)
class Verben_Futur_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Verben im Futur Simple")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Titel
        Titel_Label = QLabel("Verben im Futur Simple")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        #Beschreibung
        Beschreibung_Label = QLabel("Unten erscheint, nachdem du 'Start' gedrückt hast, ein Verb. Schreibe in jede Zeile die angepasste Form und drücke auf'bestätigen', wenn alle Formen eingetragen sind.")
        Beschreibung_Label.setFont(QFont("Arial", 16))
        Beschreibung_Label.setWordWrap(True)
        #Anzeige der Vokabel
        Wort_Anzeige_Label = QLabel("Infinitiv:")
        Wort_Anzeige_Label.setFont(QFont("Arial", 16))
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 16))
        
        #weitere Stichworte
        Eingabe_Anzeige_Label = QLabel("Eingabefläche")
        Eingabe_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label = QLabel("Richtig/Falsch")
        R_F_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Verbesserung_Anzeige_Label = QLabel("Verbesserung")
        Verbesserung_Anzeige_Label.setFont(QFont("Arial", 15))
        Verbesserung_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Anzeigen der Pronomen
        Je_Label = QLabel("Je/J':")
        Je_Label.setFont(QFont("Arial", 15))
        Tu_Label = QLabel("Tu:")
        Tu_Label.setFont(QFont("Arial", 15))
        Il_Label = QLabel("Il/Elle/On:")
        Il_Label.setFont(QFont("Arial", 15))
        Nous_Label = QLabel("Nous:")
        Nous_Label.setFont(QFont("Arial", 15))
        Vous_Label = QLabel("Vous:")
        Vous_Label.setFont(QFont("Arial", 15))
        Ils_Label = QLabel("Ils/Elles:")
        Ils_Label.setFont(QFont("Arial", 15))
        
        #Richtig/Falsch-Anzeigen je Pronomen
        self.Je_R_F_Label = QLabel()
        self.Je_R_F_Label.setFont(QFont("Arial", 15))
        self.Tu_R_F_Label = QLabel()
        self.Tu_R_F_Label.setFont(QFont("Arial", 15))
        self.Il_R_F_Label = QLabel()
        self.Il_R_F_Label.setFont(QFont("Arial", 15))
        self.Nous_R_F_Label = QLabel()
        self.Nous_R_F_Label.setFont(QFont("Arial", 15))
        self.Vous_R_F_Label = QLabel()
        self.Vous_R_F_Label.setFont(QFont("Arial", 15))
        self.Ils_R_F_Label = QLabel()
        self.Ils_R_F_Label.setFont(QFont("Arial", 15))
        
        #Labels zur Verbesserung von Fehlern
        self.Je_V_Label = QLabel()
        self.Je_V_Label.setFont(QFont("Arial", 15))
        self.Tu_V_Label = QLabel()
        self.Tu_V_Label.setFont(QFont("Arial", 15))
        self.Il_V_Label = QLabel()
        self.Il_V_Label.setFont(QFont("Arial", 15))
        self.Nous_V_Label = QLabel()
        self.Nous_V_Label.setFont(QFont("Arial", 15))
        self.Vous_V_Label = QLabel()
        self.Vous_V_Label.setFont(QFont("Arial", 15))
        self.Ils_V_Label = QLabel()
        self.Ils_V_Label.setFont(QFont("Arial", 15))
        
        #Zeilen zur Eingabe der Antworten
        breite = 400
        self.Je_Edit = QLineEdit()
        self.Je_Edit.setFont(QFont("Arial", 15))
        self.Je_Edit.setFixedWidth(breite)
        self.Je_Edit.setClearButtonEnabled(True)
        self.Je_Edit.setEnabled(False)
        self.Tu_Edit = QLineEdit()
        self.Tu_Edit.setFont(QFont("Arial", 15))
        self.Tu_Edit.setFixedWidth(breite)
        self.Tu_Edit.setClearButtonEnabled(True)
        self.Tu_Edit.setEnabled(False)
        self.Il_Edit = QLineEdit()
        self.Il_Edit.setFont(QFont("Arial", 15))
        self.Il_Edit.setFixedWidth(breite)
        self.Il_Edit.setClearButtonEnabled(True)
        self.Il_Edit.setEnabled(False)
        self.Nous_Edit = QLineEdit()
        self.Nous_Edit.setFont(QFont("Arial", 15))
        self.Nous_Edit.setFixedWidth(breite)
        self.Nous_Edit.setClearButtonEnabled(True)
        self.Nous_Edit.setEnabled(False)
        self.Vous_Edit = QLineEdit()
        self.Vous_Edit.setFont(QFont("Arial", 15))
        self.Vous_Edit.setFixedWidth(breite)
        self.Vous_Edit.setClearButtonEnabled(True)
        self.Vous_Edit.setEnabled(False)
        self.Ils_Edit = QLineEdit()
        self.Ils_Edit.setFont(QFont("Arial", 15))
        self.Ils_Edit.setFixedWidth(breite)
        self.Ils_Edit.setClearButtonEnabled(True)
        self.Ils_Edit.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.clicked.connect(self.bestaetigen)
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Bestaetigen_Knopf.setEnabled(False)

        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")
        self.Weiter_Knopf.setEnabled(False)

        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        
        #Layout
        VBox = QVBoxLayout()
        VBox.addWidget(Titel_Label)
        VBox.addWidget(Beschreibung_Label)
        Form = QFormLayout()
        Form.addRow(Wort_Anzeige_Label, self.Wort_Label)
        Form.addRow(Je_Label, self.Je_Edit)
        Form.addRow(Tu_Label, self.Tu_Edit)
        Form.addRow(Il_Label, self.Il_Edit)
        Form.addRow(Nous_Label, self.Nous_Edit)
        Form.addRow(Vous_Label, self.Vous_Edit)
        Form.addRow(Ils_Label, self.Ils_Edit)
        Grid = QGridLayout()
        Grid.addWidget(Eingabe_Anzeige_Label, 0, 0)
        Grid.addWidget(R_F_Anzeige_Label, 0, 2)
        Grid.addWidget(self.Je_R_F_Label, 2, 2)
        Grid.addWidget(self.Tu_R_F_Label, 3, 2)
        Grid.addWidget(self.Il_R_F_Label, 4, 2)
        Grid.addWidget(self.Nous_R_F_Label, 5, 2)
        Grid.addWidget(self.Vous_R_F_Label, 6, 2)
        Grid.addWidget(self.Ils_R_F_Label, 7, 2)
        Grid.addWidget(Verbesserung_Anzeige_Label, 0, 3)
        Grid.addWidget(self.Je_V_Label, 2, 3)
        Grid.addWidget(self.Tu_V_Label, 3, 3)
        Grid.addWidget(self.Il_V_Label, 4, 3)
        Grid.addWidget(self.Nous_V_Label, 5, 3)
        Grid.addWidget(self.Vous_V_Label, 6, 3)
        Grid.addWidget(self.Ils_V_Label, 7, 3)
        Grid.addLayout(Form, 1, 0, 7, 2)
        VBox.addLayout(Grid)
        VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        VBox.addLayout(HBox)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Futur_Infinitiv)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            self.gestartet = True
            text = Futur_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Je_Edit.setEnabled(True)
            self.Tu_Edit.setEnabled(True)
            self.Il_Edit.setEnabled(True)
            self.Nous_Edit.setEnabled(True)
            self.Vous_Edit.setEnabled(True)
            self.Ils_Edit.setEnabled(True)
            self.Je_Edit.setFocus()
            
    def bestaetigen(self):
        if self.gestartet == True:
            #Sammlung der Daten
            antwort_je = self.Je_Edit.text()
            antwort_tu = self.Tu_Edit.text()
            antwort_il = self.Il_Edit.text()
            antwort_nous = self.Nous_Edit.text()
            antwort_vous = self.Vous_Edit.text()
            antwort_ils = self.Ils_Edit.text()
            #Prüfung und Ausgabe der Ergebnisse mit eventueller Berichtigung
            if antwort_je == Futur_Je[self.vokabeln[self.vokabel_index]]:
                self.Je_R_F_Label.setText("Richtig!")
                self.Je_V_Label.setText("Kein Fehler!")
            else:
                self.Je_R_F_Label.setText("Falsch!")
                text = Futur_Je[self.vokabeln[self.vokabel_index]]
                self.Je_V_Label.setText(text)
            if antwort_tu == Futur_Tu[self.vokabeln[self.vokabel_index]]:
                self.Tu_R_F_Label.setText("Richtig!")
                self.Tu_V_Label.setText("Kein Fehler!")
            else:
                self.Tu_R_F_Label.setText("Falsch!")
                text = Futur_Tu[self.vokabeln[self.vokabel_index]]
                self.Tu_V_Label.setText(text)
            if antwort_il == Futur_Il[self.vokabeln[self.vokabel_index]]:
                self.Il_R_F_Label.setText("Richtig!")
                self.Il_V_Label.setText("Kein Fehler!")
            else:
                self.Il_R_F_Label.setText("Falsch!")
                text = Futur_Il[self.vokabeln[self.vokabel_index]]
                self.Il_V_Label.setText(text)
            if antwort_nous == Futur_Nous[self.vokabeln[self.vokabel_index]]:
                self.Nous_R_F_Label.setText("Richtig!")
                self.Nous_V_Label.setText("Kein Fehler!")
            else:
                self.Nous_R_F_Label.setText("Falsch!")
                text = Futur_Nous[self.vokabeln[self.vokabel_index]]
                self.Nous_V_Label.setText(text)
            if antwort_vous == Futur_Vous[self.vokabeln[self.vokabel_index]]:
                self.Vous_R_F_Label.setText("Richtig!")
                self.Vous_V_Label.setText("Kein Fehler!")
            else:
                self.Vous_R_F_Label.setText("Falsch!")
                text = Futur_Vous[self.vokabeln[self.vokabel_index]]
                self.Vous_V_Label.setText(text)
            if antwort_ils == Futur_Ils[self.vokabeln[self.vokabel_index]]:
                self.Ils_R_F_Label.setText("Richtig!")
                self.Ils_V_Label.setText("Kein Fehler!")
            else:
                self.Ils_R_F_Label.setText("Falsch!")
                text = Futur_Ils[self.vokabeln[self.vokabel_index]]
                self.Ils_V_Label.setText(text)

    def weiter(self):
        self.Je_Edit.clear()
        self.Je_R_F_Label.clear()
        self.Je_V_Label.clear()
        self.Tu_Edit.clear()
        self.Tu_R_F_Label.clear()
        self.Tu_V_Label.clear()
        self.Il_Edit.clear()
        self.Il_R_F_Label.clear()
        self.Il_V_Label.clear()
        self.Nous_Edit.clear()
        self.Nous_R_F_Label.clear()
        self.Nous_V_Label.clear()
        self.Vous_Edit.clear()
        self.Vous_R_F_Label.clear()
        self.Vous_V_Label.clear()
        self.Ils_Edit.clear()
        self.Ils_R_F_Label.clear()
        self.Ils_V_Label.clear()

        self.vokabel_index += 1
        if (len(Futur_Infinitiv)-1) >= self.vokabel_index:
            text = Futur_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Je_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Verben wurde abgefragt.")
            self.Je_Edit.setEnabled(False)
            self.Tu_Edit.setEnabled(False)
            self.Il_Edit.setEnabled(False)
            self.Nous_Edit.setEnabled(False)
            self.Vous_Edit.setEnabled(False)
            self.Ils_Edit.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.gestartet = False
            self.vokabeln = []
            self.vokabel_index = 0

    def ende(self):
        #print("Verbenfenster wurde geschlossen.")
        self.hide()
        HM.show()

#Abfrage Verben im Conditionnel (Quiz)
class Verben_Conditionnel_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Verben im Conditionnel")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Titel
        Titel_Label = QLabel("Verben im Conditionnel")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        #Beschreibung
        Beschreibung_Label = QLabel("Unten erscheint, nachdem du 'Start' gedrückt hast, ein Verb. Schreibe in jede Zeile die angepasste Form und drücke auf'bestätigen', wenn alle Formen eingetragen sind.")
        Beschreibung_Label.setFont(QFont("Arial", 16))
        Beschreibung_Label.setWordWrap(True)
        #Anzeige der Vokabel
        Wort_Anzeige_Label = QLabel("Infinitiv:")
        Wort_Anzeige_Label.setFont(QFont("Arial", 16))
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 16))
        
        #weitere Stichworte
        Eingabe_Anzeige_Label = QLabel("Eingabefläche")
        Eingabe_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label = QLabel("Richtig/Falsch")
        R_F_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Verbesserung_Anzeige_Label = QLabel("Verbesserung")
        Verbesserung_Anzeige_Label.setFont(QFont("Arial", 15))
        Verbesserung_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Anzeigen der Pronomen
        Je_Label = QLabel("Je/J':")
        Je_Label.setFont(QFont("Arial", 15))
        Tu_Label = QLabel("Tu:")
        Tu_Label.setFont(QFont("Arial", 15))
        Il_Label = QLabel("Il/Elle/On:")
        Il_Label.setFont(QFont("Arial", 15))
        Nous_Label = QLabel("Nous:")
        Nous_Label.setFont(QFont("Arial", 15))
        Vous_Label = QLabel("Vous:")
        Vous_Label.setFont(QFont("Arial", 15))
        Ils_Label = QLabel("Ils/Elles:")
        Ils_Label.setFont(QFont("Arial", 15))
        
        #Richtig/Falsch-Anzeigen je Pronomen
        self.Je_R_F_Label = QLabel()
        self.Je_R_F_Label.setFont(QFont("Arial", 15))
        self.Tu_R_F_Label = QLabel()
        self.Tu_R_F_Label.setFont(QFont("Arial", 15))
        self.Il_R_F_Label = QLabel()
        self.Il_R_F_Label.setFont(QFont("Arial", 15))
        self.Nous_R_F_Label = QLabel()
        self.Nous_R_F_Label.setFont(QFont("Arial", 15))
        self.Vous_R_F_Label = QLabel()
        self.Vous_R_F_Label.setFont(QFont("Arial", 15))
        self.Ils_R_F_Label = QLabel()
        self.Ils_R_F_Label.setFont(QFont("Arial", 15))
        
        #Labels zur Verbesserung von Fehlern
        self.Je_V_Label = QLabel()
        self.Je_V_Label.setFont(QFont("Arial", 15))
        self.Tu_V_Label = QLabel()
        self.Tu_V_Label.setFont(QFont("Arial", 15))
        self.Il_V_Label = QLabel()
        self.Il_V_Label.setFont(QFont("Arial", 15))
        self.Nous_V_Label = QLabel()
        self.Nous_V_Label.setFont(QFont("Arial", 15))
        self.Vous_V_Label = QLabel()
        self.Vous_V_Label.setFont(QFont("Arial", 15))
        self.Ils_V_Label = QLabel()
        self.Ils_V_Label.setFont(QFont("Arial", 15))
        
        #Zeilen zur Eingabe der Antworten
        breite = 400
        self.Je_Edit = QLineEdit()
        self.Je_Edit.setFont(QFont("Arial", 15))
        self.Je_Edit.setFixedWidth(breite)
        self.Je_Edit.setClearButtonEnabled(True)
        self.Je_Edit.setEnabled(False)
        self.Tu_Edit = QLineEdit()
        self.Tu_Edit.setFont(QFont("Arial", 15))
        self.Tu_Edit.setFixedWidth(breite)
        self.Tu_Edit.setClearButtonEnabled(True)
        self.Tu_Edit.setEnabled(False)
        self.Il_Edit = QLineEdit()
        self.Il_Edit.setFont(QFont("Arial", 15))
        self.Il_Edit.setFixedWidth(breite)
        self.Il_Edit.setClearButtonEnabled(True)
        self.Il_Edit.setEnabled(False)
        self.Nous_Edit = QLineEdit()
        self.Nous_Edit.setFont(QFont("Arial", 15))
        self.Nous_Edit.setFixedWidth(breite)
        self.Nous_Edit.setClearButtonEnabled(True)
        self.Nous_Edit.setEnabled(False)
        self.Vous_Edit = QLineEdit()
        self.Vous_Edit.setFont(QFont("Arial", 15))
        self.Vous_Edit.setFixedWidth(breite)
        self.Vous_Edit.setClearButtonEnabled(True)
        self.Vous_Edit.setEnabled(False)
        self.Ils_Edit = QLineEdit()
        self.Ils_Edit.setFont(QFont("Arial", 15))
        self.Ils_Edit.setFixedWidth(breite)
        self.Ils_Edit.setClearButtonEnabled(True)
        self.Ils_Edit.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.clicked.connect(self.bestaetigen)
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Bestaetigen_Knopf.setEnabled(False)

        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")
        self.Weiter_Knopf.setEnabled(False)

        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        
        #Layout
        VBox = QVBoxLayout()
        VBox.addWidget(Titel_Label)
        VBox.addWidget(Beschreibung_Label)
        Form = QFormLayout()
        Form.addRow(Wort_Anzeige_Label, self.Wort_Label)
        Form.addRow(Je_Label, self.Je_Edit)
        Form.addRow(Tu_Label, self.Tu_Edit)
        Form.addRow(Il_Label, self.Il_Edit)
        Form.addRow(Nous_Label, self.Nous_Edit)
        Form.addRow(Vous_Label, self.Vous_Edit)
        Form.addRow(Ils_Label, self.Ils_Edit)
        Grid = QGridLayout()
        Grid.addWidget(Eingabe_Anzeige_Label, 0, 0)
        Grid.addWidget(R_F_Anzeige_Label, 0, 2)
        Grid.addWidget(self.Je_R_F_Label, 2, 2)
        Grid.addWidget(self.Tu_R_F_Label, 3, 2)
        Grid.addWidget(self.Il_R_F_Label, 4, 2)
        Grid.addWidget(self.Nous_R_F_Label, 5, 2)
        Grid.addWidget(self.Vous_R_F_Label, 6, 2)
        Grid.addWidget(self.Ils_R_F_Label, 7, 2)
        Grid.addWidget(Verbesserung_Anzeige_Label, 0, 3)
        Grid.addWidget(self.Je_V_Label, 2, 3)
        Grid.addWidget(self.Tu_V_Label, 3, 3)
        Grid.addWidget(self.Il_V_Label, 4, 3)
        Grid.addWidget(self.Nous_V_Label, 5, 3)
        Grid.addWidget(self.Vous_V_Label, 6, 3)
        Grid.addWidget(self.Ils_V_Label, 7, 3)
        Grid.addLayout(Form, 1, 0, 7, 2)
        VBox.addLayout(Grid)
        VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        VBox.addLayout(HBox)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Conditionnel_Infinitiv)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            self.gestartet = True
            text = Conditionnel_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Je_Edit.setEnabled(True)
            self.Tu_Edit.setEnabled(True)
            self.Il_Edit.setEnabled(True)
            self.Nous_Edit.setEnabled(True)
            self.Vous_Edit.setEnabled(True)
            self.Ils_Edit.setEnabled(True)
            self.Je_Edit.setFocus()
            
    def bestaetigen(self):
        if self.gestartet == True:
            #Sammlung der Daten
            antwort_je = self.Je_Edit.text()
            antwort_tu = self.Tu_Edit.text()
            antwort_il = self.Il_Edit.text()
            antwort_nous = self.Nous_Edit.text()
            antwort_vous = self.Vous_Edit.text()
            antwort_ils = self.Ils_Edit.text()
            #Prüfung und Ausgabe der Ergebnisse mit eventueller Berichtigung
            if antwort_je == Conditionnel_Je[self.vokabeln[self.vokabel_index]]:
                self.Je_R_F_Label.setText("Richtig!")
                self.Je_V_Label.setText("Kein Fehler!")
            else:
                self.Je_R_F_Label.setText("Falsch!")
                text = Conditionnel_Je[self.vokabeln[self.vokabel_index]]
                self.Je_V_Label.setText(text)
            if antwort_tu == Conditionnel_Tu[self.vokabeln[self.vokabel_index]]:
                self.Tu_R_F_Label.setText("Richtig!")
                self.Tu_V_Label.setText("Kein Fehler!")
            else:
                self.Tu_R_F_Label.setText("Falsch!")
                text = Conditionnel_Tu[self.vokabeln[self.vokabel_index]]
                self.Tu_V_Label.setText(text)
            if antwort_il == Conditionnel_Il[self.vokabeln[self.vokabel_index]]:
                self.Il_R_F_Label.setText("Richtig!")
                self.Il_V_Label.setText("Kein Fehler!")
            else:
                self.Il_R_F_Label.setText("Falsch!")
                text = Conditionnel_Il[self.vokabeln[self.vokabel_index]]
                self.Il_V_Label.setText(text)
            if antwort_nous == Conditionnel_Nous[self.vokabeln[self.vokabel_index]]:
                self.Nous_R_F_Label.setText("Richtig!")
                self.Nous_V_Label.setText("Kein Fehler!")
            else:
                self.Nous_R_F_Label.setText("Falsch!")
                text = Conditionnel_Nous[self.vokabeln[self.vokabel_index]]
                self.Nous_V_Label.setText(text)
            if antwort_vous == Conditionnel_Vous[self.vokabeln[self.vokabel_index]]:
                self.Vous_R_F_Label.setText("Richtig!")
                self.Vous_V_Label.setText("Kein Fehler!")
            else:
                self.Vous_R_F_Label.setText("Falsch!")
                text = Conditionnel_Vous[self.vokabeln[self.vokabel_index]]
                self.Vous_V_Label.setText(text)
            if antwort_ils == Conditionnel_Ils[self.vokabeln[self.vokabel_index]]:
                self.Ils_R_F_Label.setText("Richtig!")
                self.Ils_V_Label.setText("Kein Fehler!")
            else:
                self.Ils_R_F_Label.setText("Falsch!")
                text = Conditionnel_Ils[self.vokabeln[self.vokabel_index]]
                self.Ils_V_Label.setText(text)

    def weiter(self):
        self.Je_Edit.clear()
        self.Je_R_F_Label.clear()
        self.Je_V_Label.clear()
        self.Tu_Edit.clear()
        self.Tu_R_F_Label.clear()
        self.Tu_V_Label.clear()
        self.Il_Edit.clear()
        self.Il_R_F_Label.clear()
        self.Il_V_Label.clear()
        self.Nous_Edit.clear()
        self.Nous_R_F_Label.clear()
        self.Nous_V_Label.clear()
        self.Vous_Edit.clear()
        self.Vous_R_F_Label.clear()
        self.Vous_V_Label.clear()
        self.Ils_Edit.clear()
        self.Ils_R_F_Label.clear()
        self.Ils_V_Label.clear()

        self.vokabel_index += 1
        if (len(Conditionnel_Infinitiv)-1) >= self.vokabel_index:
            text = Conditionnel_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Je_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Verben wurde abgefragt.")
            self.Je_Edit.setEnabled(False)
            self.Tu_Edit.setEnabled(False)
            self.Il_Edit.setEnabled(False)
            self.Nous_Edit.setEnabled(False)
            self.Vous_Edit.setEnabled(False)
            self.Ils_Edit.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.gestartet = False
            self.vokabeln = []
            self.vokabel_index = 0

    def ende(self):
        #print("Verbenfenster wurde geschlossen.")
        self.hide()
        HM.show()

#Abfrage Verben im Subjontif (Quiz)
class Verben_Subjontif_Quiz(QWidget):
    gestartet = False
    vokabeln = []
    vokabel_index = 0
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Verben im Subjontif")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Titel
        Titel_Label = QLabel("Verben im Subjontif")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        #Beschreibung
        Beschreibung_Label = QLabel("Unten erscheint, nachdem du 'Start' gedrückt hast, ein Verb. Schreibe in jede Zeile die angepasste Form und drücke auf'bestätigen', wenn alle Formen eingetragen sind.")
        Beschreibung_Label.setFont(QFont("Arial", 16))
        Beschreibung_Label.setWordWrap(True)
        #Anzeige der Vokabel
        Wort_Anzeige_Label = QLabel("Infinitiv:")
        Wort_Anzeige_Label.setFont(QFont("Arial", 16))
        self.Wort_Label = QLabel()
        self.Wort_Label.setFont(QFont("Arial", 16))
        
        #weitere Stichworte
        Eingabe_Anzeige_Label = QLabel("Eingabefläche")
        Eingabe_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label = QLabel("Richtig/Falsch")
        R_F_Anzeige_Label.setFont(QFont("Arial", 15))
        R_F_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        Verbesserung_Anzeige_Label = QLabel("Verbesserung")
        Verbesserung_Anzeige_Label.setFont(QFont("Arial", 15))
        Verbesserung_Anzeige_Label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Anzeigen der Pronomen
        Je_Label = QLabel("Je/J':")
        Je_Label.setFont(QFont("Arial", 15))
        Tu_Label = QLabel("Tu:")
        Tu_Label.setFont(QFont("Arial", 15))
        Il_Label = QLabel("Il/Elle/On:")
        Il_Label.setFont(QFont("Arial", 15))
        Nous_Label = QLabel("Nous:")
        Nous_Label.setFont(QFont("Arial", 15))
        Vous_Label = QLabel("Vous:")
        Vous_Label.setFont(QFont("Arial", 15))
        Ils_Label = QLabel("Ils/Elles:")
        Ils_Label.setFont(QFont("Arial", 15))
        
        #Richtig/Falsch-Anzeigen je Pronomen
        self.Je_R_F_Label = QLabel()
        self.Je_R_F_Label.setFont(QFont("Arial", 15))
        self.Tu_R_F_Label = QLabel()
        self.Tu_R_F_Label.setFont(QFont("Arial", 15))
        self.Il_R_F_Label = QLabel()
        self.Il_R_F_Label.setFont(QFont("Arial", 15))
        self.Nous_R_F_Label = QLabel()
        self.Nous_R_F_Label.setFont(QFont("Arial", 15))
        self.Vous_R_F_Label = QLabel()
        self.Vous_R_F_Label.setFont(QFont("Arial", 15))
        self.Ils_R_F_Label = QLabel()
        self.Ils_R_F_Label.setFont(QFont("Arial", 15))
        
        #Labels zur Verbesserung von Fehlern
        self.Je_V_Label = QLabel()
        self.Je_V_Label.setFont(QFont("Arial", 15))
        self.Tu_V_Label = QLabel()
        self.Tu_V_Label.setFont(QFont("Arial", 15))
        self.Il_V_Label = QLabel()
        self.Il_V_Label.setFont(QFont("Arial", 15))
        self.Nous_V_Label = QLabel()
        self.Nous_V_Label.setFont(QFont("Arial", 15))
        self.Vous_V_Label = QLabel()
        self.Vous_V_Label.setFont(QFont("Arial", 15))
        self.Ils_V_Label = QLabel()
        self.Ils_V_Label.setFont(QFont("Arial", 15))
        
        #Zeilen zur Eingabe der Antworten
        breite = 400
        self.Je_Edit = QLineEdit()
        self.Je_Edit.setFont(QFont("Arial", 15))
        self.Je_Edit.setFixedWidth(breite)
        self.Je_Edit.setClearButtonEnabled(True)
        self.Je_Edit.setEnabled(False)
        self.Tu_Edit = QLineEdit()
        self.Tu_Edit.setFont(QFont("Arial", 15))
        self.Tu_Edit.setFixedWidth(breite)
        self.Tu_Edit.setClearButtonEnabled(True)
        self.Tu_Edit.setEnabled(False)
        self.Il_Edit = QLineEdit()
        self.Il_Edit.setFont(QFont("Arial", 15))
        self.Il_Edit.setFixedWidth(breite)
        self.Il_Edit.setClearButtonEnabled(True)
        self.Il_Edit.setEnabled(False)
        self.Nous_Edit = QLineEdit()
        self.Nous_Edit.setFont(QFont("Arial", 15))
        self.Nous_Edit.setFixedWidth(breite)
        self.Nous_Edit.setClearButtonEnabled(True)
        self.Nous_Edit.setEnabled(False)
        self.Vous_Edit = QLineEdit()
        self.Vous_Edit.setFont(QFont("Arial", 15))
        self.Vous_Edit.setFixedWidth(breite)
        self.Vous_Edit.setClearButtonEnabled(True)
        self.Vous_Edit.setEnabled(False)
        self.Ils_Edit = QLineEdit()
        self.Ils_Edit.setFont(QFont("Arial", 15))
        self.Ils_Edit.setFixedWidth(breite)
        self.Ils_Edit.setClearButtonEnabled(True)
        self.Ils_Edit.setEnabled(False)

        #Startknopf
        self.Start_Knopf = QPushButton()
        image = "images/Start.png"
        try:
            with open(image):
                Bild = QIcon(image)
                self.Start_Knopf.setIcon(Bild)
                self.Start_Knopf.setIconSize(QSize(60, 60))
                self.Start_Knopf.setFixedSize(QSize(75, 75))
        except FileNotFoundError as error:
            print(f"Image not found. \nError: {error}")
            print("Das Bild Start.png wurde nicht gefunden.")
            self.Start_Knopf.setText("Start")
            self.Start_Knopf.setFont(QFont("Arial", 18))
            self.Start_Knopf.setStyleSheet("background-color: lightblue")
            self.Start_Knopf.setFixedSize(QSize(80, 30))
        self.Start_Knopf.clicked.connect(self.start)

        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Bestaetigen_Knopf.clicked.connect(self.bestaetigen)
        self.Bestaetigen_Knopf.setFixedSize(QSize(120, 30))
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Bestaetigen_Knopf.setEnabled(False)

        self.Weiter_Knopf = QPushButton("weiter")
        self.Weiter_Knopf.setFont(QFont("Arial", 16))
        self.Weiter_Knopf.clicked.connect(self.weiter)
        self.Weiter_Knopf.setFixedSize(QSize(80, 30))
        self.Weiter_Knopf.setStyleSheet("background-color: lightblue")
        self.Weiter_Knopf.setEnabled(False)

        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.clicked.connect(self.ende)
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        
        #Layout
        VBox = QVBoxLayout()
        VBox.addWidget(Titel_Label)
        VBox.addWidget(Beschreibung_Label)
        Form = QFormLayout()
        Form.addRow(Wort_Anzeige_Label, self.Wort_Label)
        Form.addRow(Je_Label, self.Je_Edit)
        Form.addRow(Tu_Label, self.Tu_Edit)
        Form.addRow(Il_Label, self.Il_Edit)
        Form.addRow(Nous_Label, self.Nous_Edit)
        Form.addRow(Vous_Label, self.Vous_Edit)
        Form.addRow(Ils_Label, self.Ils_Edit)
        Grid = QGridLayout()
        Grid.addWidget(Eingabe_Anzeige_Label, 0, 0)
        Grid.addWidget(R_F_Anzeige_Label, 0, 2)
        Grid.addWidget(self.Je_R_F_Label, 2, 2)
        Grid.addWidget(self.Tu_R_F_Label, 3, 2)
        Grid.addWidget(self.Il_R_F_Label, 4, 2)
        Grid.addWidget(self.Nous_R_F_Label, 5, 2)
        Grid.addWidget(self.Vous_R_F_Label, 6, 2)
        Grid.addWidget(self.Ils_R_F_Label, 7, 2)
        Grid.addWidget(Verbesserung_Anzeige_Label, 0, 3)
        Grid.addWidget(self.Je_V_Label, 2, 3)
        Grid.addWidget(self.Tu_V_Label, 3, 3)
        Grid.addWidget(self.Il_V_Label, 4, 3)
        Grid.addWidget(self.Nous_V_Label, 5, 3)
        Grid.addWidget(self.Vous_V_Label, 6, 3)
        Grid.addWidget(self.Ils_V_Label, 7, 3)
        Grid.addLayout(Form, 1, 0, 7, 2)
        VBox.addLayout(Grid)
        VBox.addWidget(self.Start_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        HBox = QHBoxLayout()
        HBox.addWidget(self.Bestaetigen_Knopf)
        HBox.addWidget(self.Weiter_Knopf)
        VBox.addLayout(HBox)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox)

    #Methoden
    def start(self):
        if self.gestartet == False:
            for x in range(0, len(Subjontif_Infinitiv)):
                self.vokabeln.append(x)
            shuffle(self.vokabeln)
            self.gestartet = True
            text = Subjontif_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Bestaetigen_Knopf.setEnabled(True)
            self.Weiter_Knopf.setEnabled(True)
            self.Je_Edit.setEnabled(True)
            self.Tu_Edit.setEnabled(True)
            self.Il_Edit.setEnabled(True)
            self.Nous_Edit.setEnabled(True)
            self.Vous_Edit.setEnabled(True)
            self.Ils_Edit.setEnabled(True)
            self.Je_Edit.setFocus()
            
    def bestaetigen(self):
        if self.gestartet == True:
            #Sammlung der Daten
            antwort_je = self.Je_Edit.text()
            antwort_tu = self.Tu_Edit.text()
            antwort_il = self.Il_Edit.text()
            antwort_nous = self.Nous_Edit.text()
            antwort_vous = self.Vous_Edit.text()
            antwort_ils = self.Ils_Edit.text()
            #Prüfung und Ausgabe der Ergebnisse mit eventueller Berichtigung
            if antwort_je == Subjontif_Je[self.vokabeln[self.vokabel_index]]:
                self.Je_R_F_Label.setText("Richtig!")
                self.Je_V_Label.setText("Kein Fehler!")
            else:
                self.Je_R_F_Label.setText("Falsch!")
                text = Subjontif_Je[self.vokabeln[self.vokabel_index]]
                self.Je_V_Label.setText(text)
            if antwort_tu == Subjontif_Tu[self.vokabeln[self.vokabel_index]]:
                self.Tu_R_F_Label.setText("Richtig!")
                self.Tu_V_Label.setText("Kein Fehler!")
            else:
                self.Tu_R_F_Label.setText("Falsch!")
                text = Subjontif_Tu[self.vokabeln[self.vokabel_index]]
                self.Tu_V_Label.setText(text)
            if antwort_il == Subjontif_Il[self.vokabeln[self.vokabel_index]]:
                self.Il_R_F_Label.setText("Richtig!")
                self.Il_V_Label.setText("Kein Fehler!")
            else:
                self.Il_R_F_Label.setText("Falsch!")
                text = Subjontif_Il[self.vokabeln[self.vokabel_index]]
                self.Il_V_Label.setText(text)
            if antwort_nous == Subjontif_Nous[self.vokabeln[self.vokabel_index]]:
                self.Nous_R_F_Label.setText("Richtig!")
                self.Nous_V_Label.setText("Kein Fehler!")
            else:
                self.Nous_R_F_Label.setText("Falsch!")
                text = Subjontif_Nous[self.vokabeln[self.vokabel_index]]
                self.Nous_V_Label.setText(text)
            if antwort_vous == Subjontif_Vous[self.vokabeln[self.vokabel_index]]:
                self.Vous_R_F_Label.setText("Richtig!")
                self.Vous_V_Label.setText("Kein Fehler!")
            else:
                self.Vous_R_F_Label.setText("Falsch!")
                text = Subjontif_Vous[self.vokabeln[self.vokabel_index]]
                self.Vous_V_Label.setText(text)
            if antwort_ils == Subjontif_Ils[self.vokabeln[self.vokabel_index]]:
                self.Ils_R_F_Label.setText("Richtig!")
                self.Ils_V_Label.setText("Kein Fehler!")
            else:
                self.Ils_R_F_Label.setText("Falsch!")
                text = Subjontif_Ils[self.vokabeln[self.vokabel_index]]
                self.Ils_V_Label.setText(text)

    def weiter(self):
        self.Je_Edit.clear()
        self.Je_R_F_Label.clear()
        self.Je_V_Label.clear()
        self.Tu_Edit.clear()
        self.Tu_R_F_Label.clear()
        self.Tu_V_Label.clear()
        self.Il_Edit.clear()
        self.Il_R_F_Label.clear()
        self.Il_V_Label.clear()
        self.Nous_Edit.clear()
        self.Nous_R_F_Label.clear()
        self.Nous_V_Label.clear()
        self.Vous_Edit.clear()
        self.Vous_R_F_Label.clear()
        self.Vous_V_Label.clear()
        self.Ils_Edit.clear()
        self.Ils_R_F_Label.clear()
        self.Ils_V_Label.clear()

        self.vokabel_index += 1
        if (len(Subjontif_Infinitiv)-1) >= self.vokabel_index:
            text = Subjontif_Infinitiv[self.vokabeln[self.vokabel_index]]
            self.Wort_Label.setText(text)
            self.Je_Edit.setFocus()
        else:
            self.Wort_Label.setText("Alle Verben wurde abgefragt.")
            self.Je_Edit.setEnabled(False)
            self.Tu_Edit.setEnabled(False)
            self.Il_Edit.setEnabled(False)
            self.Nous_Edit.setEnabled(False)
            self.Vous_Edit.setEnabled(False)
            self.Ils_Edit.setEnabled(False)
            self.Bestaetigen_Knopf.setEnabled(False)
            self.Weiter_Knopf.setEnabled(False)
            self.gestartet = False
            self.vokabeln = []
            self.vokabel_index = 0

    def ende(self):
        #print("Verbenfenster wurde geschlossen.")
        self.hide()
        HM.show()

#Vokabel-Editor
class Vokabel_Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Vokabeleditor")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Oberflächenelemente

        #Titel
        Titel_Label = QLabel("Vokabeleditor")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Datei
        Datei_Label = QLabel("Datei:")
        Datei_Label.setFont(QFont("Arial", 15))
        self.Datei_Edit = QLineEdit()
        self.Datei_Edit.setFont(QFont("Arial", 15))
        self.Datei_Edit.setClearButtonEnabled(True)
        self.Datei_Edit.setPlaceholderText("Datei.txt")

        #Bearbeitung
        self.Vokabel_Tedit = QTextEdit()
        self.Vokabel_Tedit.setFont(QFont("Arial", 15))

        #Knöpfe
        self.Laden_Knopf = QPushButton("laden")
        self.Laden_Knopf.setFont(QFont("Arial", 16))
        self.Laden_Knopf.setFixedSize(80, 30)
        self.Laden_Knopf.setStyleSheet("background-color: lightblue")
        self.Laden_Knopf.clicked.connect(self.laden)

        self.Speichern_Knopf = QPushButton("speichern")
        self.Speichern_Knopf.setFont(QFont("Arial", 16))
        self.Speichern_Knopf.setFixedSize(QSize(110, 30))
        self.Speichern_Knopf.setStyleSheet("background-color: lightblue")
        self.Speichern_Knopf.clicked.connect(self.speichern)

        self.Anleit_Knopf = QPushButton("Anleitung")
        self.Anleit_Knopf.setFont(QFont("Arial", 16))
        self.Anleit_Knopf.setFixedSize(110, 30)
        self.Anleit_Knopf.setStyleSheet("background-color: lightblue")
        self.Anleit_Knopf.clicked.connect(self.anleiten)

        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.setFixedSize(QSize(100, 30))
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        self.Ende_Knopf.clicked.connect(self.ende)

        #Layout
        Form = QFormLayout()
        HBox = QHBoxLayout()
        VBox = QVBoxLayout()
        HBox.addWidget(self.Datei_Edit)
        HBox.addWidget(self.Laden_Knopf)
        VBox.addWidget(Titel_Label)
        Form.addRow(Datei_Label, HBox)
        VBox.addLayout(Form)
        VBox.addWidget(self.Vokabel_Tedit)
        VBox.addWidget(self.Speichern_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        VBox.addWidget(self.Anleit_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        VBox.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox)
    
    #Methoden
    def laden(self):
        try:
            file = "files/"+self.Datei_Edit.text()
            with open(file, "r", encoding="utf-8") as f:
                text = ""
                for line in f:
                    text += line
                self.Vokabel_Tedit.setText(text)
        except FileNotFoundError as error:
            anleitung = """<p>Die gesuchte Datei existiert nicht.</p>"""
            QMessageBox.warning(self, "Fehler!", anleitung, QMessageBox.StandardButton.Ok)

    def speichern(self):
        file = "files/"+self.Datei_Edit.text()
        with open(file, "w", encoding="utf-8") as f:
            f.write(self.Vokabel_Tedit.toPlainText())

    def anleiten(self):
        print("Anleitung wird geladen.")
        anleitung = """<p>Gib in der Textzeile oben den Namen der Datei nach dem Schema '[Dateiname].txt' ein, die geladen werden soll.
        Falls es eine Datei mit dem Namen nicht geben sollte, wird sie automatisch erstellt.</p>
        <p>Der bereits bestehende Text wird nach dem Laden im Schreibbereich angezeigt und kann bearbeitet werden.</p>
        <p>Achte auf das richtige Schema bei der Eingabe. Bei Vokabeln für die einfache Abfrage gilt: 
        [französischer bestimmter Artikel] [Französisch] [Deutsch] [alternatives Wort auf Deutsch]. Falls es kein Wort für etwas gibt, schreib '--'.</p>
        <p>Bei Dateien für Verbformen (außer Passé Composé) gilt: [Infinitiv] [Je-Form] [Tu-Form] [Il/Elle-Form] [Nous-Form] [Vous-Form] [Ils/Elles-Form].</p>
        <p>Für Passé Composé verwende: [Infinitiv] [Modal-/Hilfsverb] [Partizip].</p>"""
        QMessageBox.information(self, "Anleitung", anleitung, QMessageBox.StandardButton.Ok)

    def ende(self):
        #print("Editor-Fenster geschlossen.")
        self.hide()
        HM.show()

#Vokabel_Menue
class Vokabel_Menue(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()
    def initializeUI(self):
        self.setGeometry(10, 30, 1200, 800)
        self.setWindowTitle("Vokabelauswahl")
        self.setWindowIcon(QIcon("images/France.png"))
        self.setUpFenster()
    def setUpFenster(self):
        #Oberflächenelemente

        #Titel
        Titel_Label = QLabel("Vokabelauswahl")
        Titel_Label.setFont(QFont("Arial", 36))
        Titel_Label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Auswahl_Label = QLabel("Datei wählen")
        Auswahl_Label.setFont(QFont("Arial", 20))
        Auswahl_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Ist_Label = QLabel("ausgewählte Dateien")
        Ist_Label.setFont(QFont("Arial", 20))
        Ist_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Startet Anleitung
        self.Anleit_Knopf = QPushButton("Anleitung")
        self.Anleit_Knopf.setFont(QFont("Arial", 16))
        self.Anleit_Knopf.setStyleSheet("background-color: lightblue")
        self.Anleit_Knopf.setFixedWidth(110)
        self.Anleit_Knopf.clicked.connect(self.anleiten)

        #Auswahl
        breite = 400 #max.breite für Dateinamen

        #einfache Abfrage
        Abfrage_Label = QLabel("einfache Abfrage:")
        Abfrage_Label.setFont(QFont("Arial", 15))
        self.Abfrage_Edit = QLineEdit()
        self.Abfrage_Edit.setFixedWidth(breite)
        self.Abfrage_Edit.setClearButtonEnabled(True)
        self.Abfrage_Edit.setFont(QFont("Arial", 15))
        self.Abfrage_Bestaetigen_Knopf = QPushButton("laden")
        self.Abfrage_Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Abfrage_Bestaetigen_Knopf.setFixedWidth(70)
        self.Abfrage_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Abfrage_Bestaetigen_Knopf.clicked.connect(self.vokabelnAbfrageLaden)

        #Verben Présens
        Presens_Label = QLabel("Présens:")
        Presens_Label.setFont(QFont("Arial", 15))
        self.Presens_Edit = QLineEdit()
        self.Presens_Edit.setFont(QFont("Arial", 15))
        self.Presens_Edit.setFixedWidth(breite)
        self.Presens_Edit.setClearButtonEnabled(True)
        self.Presens_Bestaetigen_Knopf = QPushButton("laden")
        self.Presens_Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Presens_Bestaetigen_Knopf.setFixedWidth(70)
        self.Presens_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Presens_Bestaetigen_Knopf.clicked.connect(self.verbenPresensLaden)

        #Verben Passé Composé
        Passe_Compose_Label = QLabel("Passé Composé:")
        Passe_Compose_Label.setFont(QFont("Arial", 15))
        self.Passe_Compose_Edit = QLineEdit()
        self.Passe_Compose_Edit.setFont(QFont("Arial", 15))
        self.Passe_Compose_Edit.setFixedWidth(breite)
        self.Passe_Compose_Edit.setClearButtonEnabled(True)
        self.Passe_Compose_Bestaetigen_Knopf = QPushButton("laden")
        self.Passe_Compose_Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Passe_Compose_Bestaetigen_Knopf.setFixedWidth(70)
        self.Passe_Compose_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Passe_Compose_Bestaetigen_Knopf.clicked.connect(self.verbenPasseComposeLaden)

        #Verben Imparfait
        Imparfait_Label = QLabel("Imparfait:")
        Imparfait_Label.setFont(QFont("Arial", 15))
        self.Imparfait_Edit = QLineEdit()
        self.Imparfait_Edit.setFont(QFont("Arial", 15))
        self.Imparfait_Edit.setFixedWidth(breite)
        self.Imparfait_Edit.setClearButtonEnabled(True)
        self.Imparfait_Bestaetigen_Knopf = QPushButton("laden")
        self.Imparfait_Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Imparfait_Bestaetigen_Knopf.setFixedWidth(70)
        self.Imparfait_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Imparfait_Bestaetigen_Knopf.clicked.connect(self.verbenImparfaitLaden)

        #Verben Futur Simple
        Futur_Label = QLabel("Futur Simple:")
        Futur_Label.setFont(QFont("Arial", 15))
        self.Futur_Edit = QLineEdit()
        self.Futur_Edit.setFont(QFont("Arial", 15))
        self.Futur_Edit.setFixedWidth(breite)
        self.Futur_Edit.setClearButtonEnabled(True)
        self.Futur_Bestaetigen_Knopf = QPushButton("laden")
        self.Futur_Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Futur_Bestaetigen_Knopf.setFixedWidth(70)
        self.Futur_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Futur_Bestaetigen_Knopf.clicked.connect(self.verbenFuturLaden)

        #Verben Conditionnel
        Conditionnel_Label = QLabel("Conditionnel:")
        Conditionnel_Label.setFont(QFont("Arial", 15))
        self.Conditionnel_Edit = QLineEdit()
        self.Conditionnel_Edit.setFont(QFont("Arial", 15))
        self.Conditionnel_Edit.setFixedWidth(breite)
        self.Conditionnel_Edit.setClearButtonEnabled(True)
        self.Conditionnel_Bestaetigen_Knopf = QPushButton("laden")
        self.Conditionnel_Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Conditionnel_Bestaetigen_Knopf.setFixedWidth(70)
        self.Conditionnel_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Conditionnel_Bestaetigen_Knopf.clicked.connect(self.verbenConditionnelLaden)

        #Verben Subjontif
        Subjontif_Label = QLabel("Subjontif:")
        Subjontif_Label.setFont(QFont("Arial", 15))
        self.Subjontif_Edit = QLineEdit()
        self.Subjontif_Edit.setFont(QFont("Arial", 15))
        self.Subjontif_Edit.setFixedWidth(breite)
        self.Subjontif_Edit.setClearButtonEnabled(True)
        self.Subjontif_Bestaetigen_Knopf = QPushButton("laden")
        self.Subjontif_Bestaetigen_Knopf.setFont(QFont("Arial", 16))
        self.Subjontif_Bestaetigen_Knopf.setFixedWidth(70)
        self.Subjontif_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Subjontif_Bestaetigen_Knopf.clicked.connect(self.verbenSubjontifLaden)


        #Ist-Anzeigen

        #einfache Abfrage
        Abfrage_ist_Label = QLabel("einfache Abfrage:")
        Abfrage_ist_Label.setFont(QFont("Arial", 15))
        self.Abfrage_ist_Anzeige_Label = QLabel()
        self.Abfrage_ist_Anzeige_Label.setFont(QFont("Arial", 15))

        #Verben Présens
        Presens_ist_Label = QLabel("Présent:")
        Presens_ist_Label.setFont(QFont("Arial", 15))
        self.Presens_ist_Anzeige_Label = QLabel()
        self.Presens_ist_Anzeige_Label.setFont(QFont("Arial", 15))

        #Verben Passé Composé
        Passe_Compose_ist_Label = QLabel("Passé Composé:")
        Passe_Compose_ist_Label.setFont(QFont("Arial", 15))
        self.Passe_Compose_ist_Anzeige_Label = QLabel()
        self.Passe_Compose_ist_Anzeige_Label.setFont(QFont("Arial", 15))

        #Verben Imparfait
        Imparfait_ist_Label = QLabel("Imparfait:")
        Imparfait_ist_Label.setFont(QFont("Arial", 15))
        self.Imparfait_ist_Anzeige_Label = QLabel()
        self.Imparfait_ist_Anzeige_Label.setFont(QFont("Arial", 15))

        #Verben Futur Simple
        Futur_ist_Label = QLabel("Futur Simple:")
        Futur_ist_Label.setFont(QFont("Arial", 15))
        self.Futur_ist_Anzeige_Label = QLabel()
        self.Futur_ist_Anzeige_Label.setFont(QFont("Arial", 15))

        #Verben Conditionnel
        Conditionnel_ist_Label = QLabel("Conditionnel:")
        Conditionnel_ist_Label.setFont(QFont("Arial", 15))
        self.Conditionnel_ist_Anzeige_Label = QLabel()
        self.Conditionnel_ist_Anzeige_Label.setFont(QFont("Arial", 15))

        #Verben Subjontif
        Subjontif_ist_Label = QLabel("Subjontif:")
        Subjontif_ist_Label.setFont(QFont("Arial", 15))
        self.Subjontif_ist_Anzeige_Label = QLabel()
        self.Subjontif_ist_Anzeige_Label.setFont(QFont("Arial", 15))

        self.Ende_Knopf = QPushButton("beenden")
        self.Ende_Knopf.setFont(QFont("Arial", 16))
        self.Ende_Knopf.setFixedWidth(100)
        self.Ende_Knopf.setStyleSheet("background-color: lightblue")
        self.Ende_Knopf.clicked.connect(self.ende)

        #Layout
        HBox1 = QHBoxLayout()
        HBox1.addWidget(self.Abfrage_Edit)
        HBox1.addWidget(self.Abfrage_Bestaetigen_Knopf)
        HBox2 = QHBoxLayout()
        HBox2.addWidget(self.Presens_Edit)
        HBox2.addWidget(self.Presens_Bestaetigen_Knopf)
        HBox3 = QHBoxLayout()
        HBox3.addWidget(self.Passe_Compose_Edit)
        HBox3.addWidget(self.Passe_Compose_Bestaetigen_Knopf)
        HBox4 = QHBoxLayout()
        HBox4.addWidget(self.Imparfait_Edit)
        HBox4.addWidget(self.Imparfait_Bestaetigen_Knopf)
        HBox5 = QHBoxLayout()
        HBox5.addWidget(self.Futur_Edit)
        HBox5.addWidget(self.Futur_Bestaetigen_Knopf)
        HBox6 = QHBoxLayout()
        HBox6.addWidget(self.Conditionnel_Edit)
        HBox6.addWidget(self.Conditionnel_Bestaetigen_Knopf)
        HBox7 = QHBoxLayout()
        HBox7.addWidget(self.Subjontif_Edit)
        HBox7.addWidget(self.Subjontif_Bestaetigen_Knopf)
        VBox_Haupt = QVBoxLayout()
        VBox_Haupt.addWidget(Titel_Label)
        Form1 = QFormLayout()
        Form1.addRow(Abfrage_Label, HBox1)
        Form1.addRow(Presens_Label, HBox2)
        Form1.addRow(Passe_Compose_Label, HBox3)
        Form1.addRow(Imparfait_Label, HBox4)
        Form1.addRow(Futur_Label, HBox5)
        Form1.addRow(Conditionnel_Label, HBox6)
        Form1.addRow(Subjontif_Label, HBox7)
        Form2 = QFormLayout()
        Form2.addRow(Abfrage_ist_Label, self.Abfrage_ist_Anzeige_Label)
        Form2.addRow(Presens_ist_Label, self.Presens_ist_Anzeige_Label)
        Form2.addRow(Passe_Compose_ist_Label, self.Passe_Compose_ist_Anzeige_Label)
        Form2.addRow(Imparfait_ist_Label, self.Imparfait_ist_Anzeige_Label)
        Form2.addRow(Futur_ist_Label, self.Futur_ist_Anzeige_Label)
        Form2.addRow(Conditionnel_ist_Label, self.Conditionnel_ist_Anzeige_Label)
        Form2.addRow(Subjontif_ist_Label, self.Subjontif_ist_Anzeige_Label)
        VBox_1 = QVBoxLayout()
        VBox_1.addWidget(Auswahl_Label)
        VBox_1.addLayout(Form1)
        VBox_2 = QVBoxLayout()
        VBox_2.addWidget(Ist_Label)
        VBox_2.addLayout(Form2)
        VBox_Haupt.addLayout(VBox_1)
        VBox_Haupt.addLayout(VBox_2)
        VBox_Haupt.addWidget(self.Anleit_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        VBox_Haupt.addWidget(self.Ende_Knopf, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(VBox_Haupt)
    
    #Methoden
    def anleiten(self):
        anleitung = """<p>In diesem Menü können .txt-Datei als Wörterbücher ausgewählt werden, indem man den Namen der Datei in das Feld eingibt.</p>
        <p>Achtung: Der vollständige Dateiname (also mit Datentyp .txt) muss angegeben werden, weil sie sonst nicht geladen werden kann.</p<
        <p>Die ausgewählte Datei muss per Knopfdruck bestätigt werden, damit sie geladen wird.</p>
        <p>Für Deutsch-Französisch und Französisch-Deutsch wird die gleiche Datei verwendet und wird unter 'einfache Abfrage' angegeben.</p>"""
        QMessageBox.information(self, "Anleitung", anleitung, QMessageBox.StandardButton.Ok)

    def vokabelnAbfrageLaden(self):
        file = "files/"+self.Abfrage_Edit.text()
        geladen = vokabelnAbfrageLaden(file)
        if geladen == True:
            text = "Die Datei " + file + " wurde geladen."
            self.Abfrage_ist_Anzeige_Label.setText(text)
        elif file == "--" or file == "":
            self.Abfrage_ist_Anzeige_Label.setText("Keine Datei")
        else:
            text = "Die Datei " + file + " konnte nicht geladen werden."
            self.Abfrage_ist_Anzeige_Label.setText(text)

    def verbenPresensLaden(self):
        file = "files/"+self.Presens_Edit.text()
        geladen = verbenPresensLaden(file)
        if geladen == True:
            text = "Die Datei " + file + " wurde geladen."
            self.Presens_ist_Anzeige_Label.setText(text)
        elif file == "--" or file == "":
            self.Presens_ist_Anzeige_Label.setText("Keine Datei")
        else:
            text = "Die Datei " + file + " konnte nicht geladen werden."
            self.Presens_ist_Anzeige_Label.setText(text)

    def verbenImparfaitLaden(self):
        file = "files/"+self.Imparfait_Edit.text()
        geladen = verbenImparfaitLaden(file)
        if geladen == True:
            text = "Die Datei " + file + " wurde geladen."
            self.Imparfait_ist_Anzeige_Label.setText(text)
        elif file == "--" or file == "":
            self.Imparfait_ist_Anzeige_Label.setText("Keine Datei")
        else:
            text = "Die Datei " + file + " konnte nicht geladen werden."
            self.Imparfait_ist_Anzeige_Label.setText(text)

    def verbenFuturLaden(self):
        file = "files/"+self.Futur_Edit.text()
        geladen = verbenFuturLaden(file)
        if geladen == True:
            text = "Die Datei " + file + " wurde geladen."
            self.Futur_ist_Anzeige_Label.setText(text)
        elif file == "--" or file == "":
            self.Futur_ist_Anzeige_Label.setText("Keine Datei")
        else:
            text = "Die Datei " + file + " konnte nicht geladen werden."
            self.Futur_ist_Anzeige_Label.setText(text)

    def verbenConditionnelLaden(self):
        file = "files/"+self.Conditionnel_Edit.text()
        geladen = verbenConditionnelLaden(file)
        if geladen == True:
            text = "Die Datei " + file + " wurde geladen."
            self.Conditionnel_ist_Anzeige_Label.setText(text)
        elif file == "--" or file == "":
            self.Conditionnel_ist_Anzeige_Label.setText("Keine Datei")
        else:
            text = "Die Datei " + file + " konnte nicht geladen werden."
            self.Conditionnel_ist_Anzeige_Label.setText(text)

    def verbenSubjontifLaden(self):
        file = "files/"+self.Subjontif_Edit.text()
        geladen = verbenSubjontifLaden(file)
        if geladen == True:
            text = "Die Datei " + file + " wurde geladen."
            self.Subjontif_ist_Anzeige_Label.setText(text)
        elif file == "--" or file == "":
            self.Subjontif_ist_Anzeige_Label.setText("Keine Datei")
        else:
            text = "Die Datei " + file + " konnte nicht geladen werden."
            self.Subjontif_ist_Anzeige_Label.setText(text)

    def verbenPasseComposeLaden(self):
        file = "files/"+self.Passe_Compose_Edit.text()
        geladen = verbenPasseComposeLaden(file)
        if geladen == True:
            text = "Die Datei " + file + " wurde geladen."
            self.Passe_Compose_ist_Anzeige_Label.setText(text)
        elif file == "--" or file == "":
            self.Passe_Compose_ist_Anzeige_Label.setText("Keine Datei")
        else:
            text = "Die Datei " + file + " konnte nicht geladen werden."
            self.Passe_Compose_ist_Anzeige_Label.setText(text)

    def sichern(self):
        with open("files/setup.txt", "w") as f:
            if self.Abfrage_Edit.text != "":
                text = "files/"+self.Abfrage_Edit.text()
            else:
                text = "--"
            if self.Presens_Edit.text() != "":
                text += " " + "files/"+self.Presens_Edit.text()
            else:
                text += " --"
            if self.Passe_Compose_Edit.text() != "":
                text += " " + "files/"+self.Passe_Compose_Edit.text()
            else:
                text += " --"
            if self.Imparfait_Edit.text() != "":
                text += " " + "files/"+self.Imparfait_Edit.text()
            else:
                text += " --"
            if self.Futur_Edit.text() != "":
                text += " " + "files/"+self.Futur_Edit.text()
            else:
                text += " --"
            if self.Conditionnel_Edit.text() != "":
                text += " " + "files/"+self.Conditionnel_Edit.text()
            else:
                text += " --"
            if self.Subjontif_Edit.text() != "":
                text += " " + "files/"+self.Subjontif_Edit.text()
            else:
                text += " --"
            f.write(text)

    def ende(self):
        print("Menü geschlossen.")
        self.sichern()
        self.hide()
        HM.show()

#spätere Ausführung
if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupLaden()
    SF = Startfenster()
    Hilfe = Hilfefenster()
    Credits = Mitwirkende()
    HM = Hauptmenue()
    DF = Deutsch_Franzoesisch_Quiz()
    FD = Franzoesisch_Deutsch_Quiz()
    Presens = Verben_Presens_Quiz()
    Passe_Compose = Passe_Compose_Quiz()
    Imparfait = Verben_Imparfait_Quiz()
    Futur = Verben_Futur_Quiz()
    Conditionnel = Verben_Conditionnel_Quiz()
    Subjontif = Verben_Subjontif_Quiz()
    VE = Vokabel_Editor()
    VM = Vokabel_Menue()

    geladen = vokabelnAbfrageLaden(Setup[0])
    if geladen == True:
        text = "Die Datei " + Setup[0] + " wurde geladen."
        VM.Abfrage_ist_Anzeige_Label.setText(text)
        VM.Abfrage_Edit.setText(Setup[0])
    elif Setup[0] == "--":
            VM.Abfrage_ist_Anzeige_Label.setText("Keine Datei")
    else:
        text = "Die Datei " + Setup[0] + " konnte nicht geladen werden."
        VM.Abfrage_ist_Anzeige_Label.setText(text)

    geladen = verbenPresensLaden(Setup[1])
    if geladen == True:
        text = "Die Datei " + Setup[1] + " wurde geladen."
        VM.Presens_ist_Anzeige_Label.setText(text)
        VM.Presens_Edit.setText(Setup[1])
    elif Setup[1] == "--":
        VM.Presens_ist_Anzeige_Label.setText("Keine Datei")
    else:
        text = "Die Datei " + Setup[1] + " konnte nicht geladen werden."
        VM.Presens_ist_Anzeige_Label.setText(text)

    geladen = verbenPasseComposeLaden(Setup[2])
    if geladen == True:
        text = "Die Datei " + Setup[2] + " wurde geladen."
        VM.Passe_Compose_ist_Anzeige_Label.setText(text)
        VM.Passe_Compose_Edit.setText(Setup[2])
    elif Setup[2] == "--":
        VM.Passe_Compose_ist_Anzeige_Label.setText("Keine Datei")
    else:
        text = "Die Datei " + Setup[2] + " konnte nicht geladen werden."
        VM.Passe_Compose_ist_Anzeige_Label.setText(text)

    geladen = verbenImparfaitLaden(Setup[3])
    if geladen == True:
        text = "Die Datei " + Setup[3] + " wurde geladen."
        VM.Imparfait_ist_Anzeige_Label.setText(text)
        VM.Imparfait_Edit.setText(Setup[3])
    elif Setup[3] == "--":
        VM.Imparfait_ist_Anzeige_Label.setText("Keine Datei")
    else:
        text = "Die Datei " + Setup[3] + " konnte nicht geladen werden."
        VM.Imparfait_ist_Anzeige_Label.setText(text)
    
    geladen = verbenFuturLaden(Setup[4])
    if geladen == True:
        text = "Die Datei " + Setup[4] + " wurde geladen."
        VM.Futur_ist_Anzeige_Label.setText(text)
        VM.Futur_Edit.setText(Setup[4])
    elif Setup[4] == "--":
        VM.Futur_ist_Anzeige_Label.setText("Keine Datei")
    else:
        text = "Die Datei " + Setup[4] + " konnte nicht geladen werden."
        VM.Futur_ist_Anzeige_Label.setText(text)
    
    geladen = verbenConditionnelLaden(Setup[5])
    if geladen == True:
        text = "Die Datei " + Setup[5] + " wurde geladen."
        VM.Conditionnel_ist_Anzeige_Label.setText(text)
        VM.Conditionnel_Edit.setText(Setup[5])
    elif Setup[5] == "--":
        VM.Conditionnel_ist_Anzeige_Label.setText("Keine Datei")
    else:
        text = "Die Datei " + Setup[5] + " konnte nicht geladen werden."
        VM.Conditionnel_ist_Anzeige_Label.setText(text)
    
    geladen = verbenSubjontifLaden(Setup[6])
    if geladen == True:
        text = "Die Datei " + Setup[6] + " wurde geladen."
        VM.Subjontif_ist_Anzeige_Label.setText(text)
        VM.Subjontif_Edit.setText(Setup[6])
    elif Setup[6] == "--":
        VM.Subjontif_ist_Anzeige_Label.setText("Keine Datei")
    else:
        text = "Die Datei " + Setup[6] + " konnte nicht geladen werden."
        VM.Subjontif_ist_Anzeige_Label.setText(text)

    sys.exit(app.exec())