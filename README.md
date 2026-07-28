# Liquid Check for Home Assistant

Benutzerdefinierte Home-Assistant-Integration für Liquid-Check-Füllstandssensoren.

Die Integration liest die Messwerte eines Liquid-Check-Geräts über das lokale Netzwerk aus und stellt sie in Home Assistant als Sensoren bereit.

## Funktionen

- Füllstand in Prozent
- Inhalt in Litern
- gemessene Füllhöhe
- Verbindungsstatus
- Zeitpunkt der letzten erfolgreichen Aktualisierung
- Anzeige des letzten Fehlers
- manuelles Auslösen einer Messung
- konfigurierbares Abrufintervall
- optionales Beibehalten des letzten Messwerts bei Verbindungsfehlern
- Konfiguration vollständig über die Home-Assistant-Oberfläche

## Voraussetzungen

- Home Assistant
- Liquid-Check-Gerät im lokalen Netzwerk
- feste IP-Adresse oder erreichbarer Hostname des Geräts
- HACS für die empfohlene Installation

## Installation über HACS

1. HACS öffnen.
2. Zu **Integrationen** wechseln.
3. Über das Drei-Punkte-Menü **Benutzerdefinierte Repositories** öffnen.
4. Folgendes Repository eintragen: `wortsprung/liquid-check-home-assistant`
5. Als Typ **Integration** auswählen.
6. Nach **Liquid Check** suchen und installieren.
7. Home Assistant vollständig neu starten.

## Einrichtung

Nach dem Neustart:

1. **Einstellungen** öffnen.
2. **Geräte & Dienste** auswählen.
3. **Integration hinzufügen** wählen.
4. Nach **Liquid Check** suchen.

Anschließend unter anderem folgende Angaben eintragen:

- Name der Integration
- IP-Adresse oder Hostname
- Port
- HTTP oder HTTPS
- Name des Behälters
- Maximalvolumen in Litern
- automatisches Abrufintervall
- Wartezeit nach einer Messung
- Zeitüberschreitung

## Manuelle Installation

Den Ordner `custom_components/liquid_check` nach `/config/custom_components/liquid_check` kopieren und Home Assistant anschließend vollständig neu starten.

## Aktualisierung

Aktualisierungen können über HACS installiert werden. Nach einer Aktualisierung sollte Home Assistant vollständig neu gestartet werden.

## Fehlerbehebung

Wenn die Integration nicht angezeigt wird:

- prüfen, ob der Ordner `/config/custom_components/liquid_check` vorhanden ist
- Home Assistant vollständig neu starten
- unter **Einstellungen → System → Protokolle** nach `liquid_check` suchen

Wenn keine Verbindung möglich ist:

- IP-Adresse und Port prüfen
- sicherstellen, dass Home Assistant das Gerät im Netzwerk erreichen kann
- HTTP- beziehungsweise HTTPS-Einstellung kontrollieren
- Zeitüberschreitung gegebenenfalls erhöhen

## Datenschutz

Die Kommunikation erfolgt direkt zwischen Home Assistant und dem Liquid-Check-Gerät im lokalen Netzwerk. Die Integration benötigt keinen externen Cloud-Dienst.

## Version

Aktuelle Version: **1.0.4**

## Haftungsausschluss

Dies ist eine private, unabhängige Home-Assistant-Integration und kein offizielles Produkt des Geräteherstellers oder des Home-Assistant-Projekts.
