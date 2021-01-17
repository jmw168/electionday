import numpy as np
import yaml


def lese_yaml(dateiname):
    with open('Daten/' + dateiname + '.yaml') as datei:
        daten = yaml.safe_load(datei)
    return daten


def plot(delegierte):
    # import cartopy
    import cartopy.crs as ccrs
    import cartopy.io.shapereader as shpreader
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = {
        'WA': fig.add_axes([0.00, 0, 0.33, 1], projection=ccrs.PlateCarree(), frameon=False),
        'UT': fig.add_axes([0.33, 0, 0.33, 1], projection=ccrs.PlateCarree(), frameon=False),
        'FL': fig.add_axes([0.67, 0, 0.33, 1], projection=ccrs.PlateCarree(), frameon=False)
    }
    # ax.patch.set_visible(False)

    plt.title('Verteilung der Delegierten der republikanischen Vorwahl auf die Staaten')
    ax['WA'].set_extent([-125, -116, 45, 49], ccrs.Geodetic())
    ax['UT'].set_extent([-115, -109, 36, 42], ccrs.Geodetic())
    ax['FL'].set_extent([-88, -79.9, 24, 31], ccrs.Geodetic())
    ax['WA'].set_title('Washington')
    ax['UT'].set_title('Utah')
    ax['FL'].set_title('Florida')

    shape_name = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shape_name)
    reader = shpreader.Reader(states_shp)
    staaten = reader.records()

    for staat in staaten:
        if staat.attributes['iso_a2'] == 'US' and staat.attributes['postal'] in delegierte.keys():
            ax[staat.attributes['postal']].add_geometries([staat.geometry],
                                                          ccrs.PlateCarree(),
                                                          facecolor='white',
                                                          edgecolor='black')

    ax['WA'].text(0, 0, 'abc')

    # ax.add_geometries(
    #     shpreader.Reader(states_shp).geometries(),
    #     ccrs.PlateCarree(),
    #     facecolor='white', edgecolor='black')
    #
    plt.show()


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
                republikanische_abgeordnete > 0.5 * anzahl_abgeordnete) + republikanische_senatoren
        delegierte.update({staat: anzahl})
    print(delegierte)
    plot(delegierte)


if __name__ == '__main__':
    main()
