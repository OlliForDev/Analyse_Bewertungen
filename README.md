# Analyse Bewertungen der Stadtwerke Karlsruhe aus einem Vergleichsportal

## Wie kam es zu der Projektidee? 
Auf der Suche nach einem neuem Stromanbieter bin ich in einem Vergleichsportal auf die Bewertungssektion gestoßen. 
Beim genaueren Hinschauen ist mir aufgefallen, dass ein großer Teil der Bewertungen ohne Punktevergabe eingereicht wurden.
Aufgrund der sehr guten Bewertung und der doch auffällig wenig detailierten Bewertungen, hat es mich interessiert, wie Scorings berechnet werden.

## Entwicklungsablauf
###Datenextraktion
Um dies herauszufinden, habe ich einen Webscraper für das Portal entwickelt, der automatisiert alle Bewertungen eines Anbieters extrahiert.
Zum Einsatz kam hierfür Python mit den Modulen Selenium und BeautifulSoup.

### Datenspeicherung
Die extrahierten Daten von dem Vergleichsportal wurden anschließend in einer lokal gehosteten MySQL-DB gespeichert.
Der Nachvollziehbarkeit und der Bereitstellung wegen wurden die Daten anschließend als CSV-Datei exportiert.

### Datenanalyse
Um den eingangswähnten Auffälligkeiten einer Antwort zuordnen zu können, ging es im Jupyter-Notebook mit Python und dem Modul Pandas weiter.

Alle Ergebnisse der Analyse können in der Datei sw_karlsruhe_ratings_verivox.ipynb im Verzeichnis data_analysis eingesehen werden. 
