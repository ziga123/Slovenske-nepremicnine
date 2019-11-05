import re
import orodja

stevilo_strani = 56

vzorec = (
    r'<h2 itemprop="name".*'
    r'(?P<Id>\d{7})' # zajem IDja
    r'.*"title">'
    r'(?P<Lokacija>.*)' # zajem lokacije
    r'</s.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*'
    r'(?P<Leto>\d{4})' # zajem letnice gradnje
    r'.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*">'
    r'\d{2,3},?\d{0,2} m2, '
    r'(?P<Sobe>\d,?\d?)' # zajem števila sob
    r'.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*">'
    r'(?P<Kvadratura>\d+,\d+)' # zajem kvadrature
    r'.*\n.*\n.*\n.*\n.*">'
    r'(?P<Agencija>.*)' # zajem agencije
    r'<.*\n.*\n.*content="'
    r'(?P<Cena>\d+.\d+)' # zajem cene
)

def pretvori_podatke(blok):
    stanovanje = blok.groupdict()
    stanovanje['Id'] = int(stanovanje['Id'])
    stanovanje['Leto'] = int(stanovanje['Leto'])
    stanovanje['Sobe'] = float(stanovanje['Sobe'].replace(',', '.'))
    stanovanje['Kvadratura'] = float(stanovanje['Kvadratura'].replace(',', '.'))
    stanovanje['Cena'] = float(stanovanje['Cena'])
    return stanovanje

stanovanja = []
for stran in range(1, stevilo_strani + 1):
    url = (
        'https://www.nepremicnine.net'
        '/oglasi-prodaja/ljubljana-mesto'
        f'/stanovanje/{stran}/'
    )
    ime_datoteke = f'zajeti_podatki/nepremicnine-stran-{stran}.html'
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for zadetek in re.finditer(vzorec, vsebina):
        stanovanja.append(pretvori_podatke(zadetek))

stanovanja.sort(key=lambda stanovanje: stanovanje['Id'])
orodja.zapisi_json(stanovanja, 'obdelani_podatki/stanovanja.json')
orodja.zapisi_csv(stanovanja, ['Id', 'Lokacija', 'Leto', 'Sobe', 'Kvadratura', 'Agencija', 'Cena'], 'obdelani_podatki/stanovanjaLJ.csv')
