import numpy as np
import yaml


def lese_yaml(dateiname):
    with open('Daten/' + dateiname + '.yaml') as datei:
        daten = yaml.safe_load(datei)
    return daten


def main():
    allgemein = lese_yaml('Allgemein')
    abgeordnete = lese_yaml('Abgeordnete')
    wahlergebnisse = lese_yaml('Wahlergebnisse')
    senat = lese_yaml('Senat')
    wahlergebnis = wahlergebnisse[-1]
    delegierte = {}
    for staat in allgemein['Staaten'].keys():
        anzahl_abgeordnete = len([abgeordneter for abgeordneter in abgeordnete if abgeordneter['Staat'] == staat])
        bonus = int(np.ceil(0.06 * wahlergebnis[staat]['WM'])) if wahlergebnis[staat]['R'] > wahlergebnis[staat][
            'D'] else 0
        republikanische_abgeordnete = len([abgeordneter for abgeordneter in abgeordnete if
                                           abgeordneter['Staat'] == staat and abgeordneter['Partei'] == 'R'])
        republikanische_senatoren = len(
            [senator for senator in senat if senator['Staat'] == staat and senator['Partei'] == 'R'])
        anzahl = 10 + 3 * anzahl_abgeordnete + bonus + (
                    republikanische_abgeordnete > 0.5 * anzahl_abgeordnete) + republikanische_senatoren + 1 # +1 Superdelegierten
        delegierte.update({staat: anzahl})
    print(delegierte)


if __name__ == '__main__':
    main()
