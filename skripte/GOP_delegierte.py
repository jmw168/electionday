import numpy as np
import yaml


def lese_yaml(dateiname):
    with open('Daten/' + dateiname + '.yaml') as datei:
        daten = yaml.safe_load(datei)
    return daten


def main():
    allgemein = lese_yaml('allgemein')
    abgeordnete = lese_yaml('abgeordnete')
    wahlergebnisse = lese_yaml('wahlergebnisse')
    wahlergebnis = wahlergebnisse[-1]
    delegierte = {}
    for staat in allgemein['Staaten'].keys():
        anzahl_abgeordnete = len([abgeordneter for abgeordneter in abgeordnete if
                                  abgeordneter['Staat'] == staat and abgeordneter['Partei'] == 'R'])
        bonus = int(np.floor(0.6 * wahlergebnis[staat]['WM'])) if wahlergebnis[staat]['R'] > wahlergebnis[staat][
            'D'] else 0
        anzahl = 10 + 3 * anzahl_abgeordnete + bonus
        delegierte.update({staat: anzahl})
    print(delegierte)


if __name__ == '__main__':
    main()
