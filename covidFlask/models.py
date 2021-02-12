'''
Rekeningen {
    "_id":"NL38INGB0006110821",
    "naam":"Vaste lasten rekening",
    "bank":"ING",
    "saldodatum":"2020-01-01T00:00:00.000Z",
    "startsaldo":0
}

Posten {
    "_id":"Action",
     "soort":"Uitgaven",
     "categorie":"Huishoudelijk",
     "hits":0,
     "lasthit":"1900-01-01T00:00:00.000Z",
     "opmerking": "Spullen van de Action"
}

Posten {
    "_id":"Spar",
     "soort":"Uitgaven",
     "categorie":"Levensmiddelen",
     "onderdelen": ["jumbo", "plus", "albert heijn", "spar"]
     "hits":0,
     "lasthit":"1900-01-01T00:00:00.000Z"
}

sm2 = ["Jumbo", "Plus", "Albert Heijn", "AH", "Spar"]
v =  "jum"
[x for x in sm2 if v in x.lower()]
=> ['jumbo']

Categorieen {
    "_id": "Levensmiddelen",
    "soort": "Uitgaven",
}

Transactie
{
    _id: ObjectId(),
    datum: 20200617,
    naam: "Staatsloterij B.V.",
    rekening: "NL38INGB0006110821",
    tegenrekening: "NL25INGB0653573251",
    code: "IC",
    bedrag: 15.00,
    mutsoort: "Incasso",
    mededeling: {
        'naam': 'Staatsloterij B.V.', 
        'omschrijving': '1 juli trekking .Incasso trekking 01-07-2020 .56361341/9/1', 
        'iban': 'NL25INGB0653573251', 
        'kenmerk': '56361341-9-1 Machtiging ID: ABO56361341 Incassant ID: NL40CON271397880000 Eerste incasso', 
        'valutadatum': '17-06-2020'},
    opmerking: "Dit is een opmerking..."
    tags: [
        "Vaste last", "Rekening"],
    posts: [
        {
            _id: "Staatsloterij",
            soort: "Uitgaven",
            categorie: "Abonnementen",
            toegekend: 15.00
        }]
}

ToekomstTransacties
{
    _id: ObjectId(),
    datum: 20200926,
    rekening: "NL38INGB0006110821",
    naam: "Staatsloterij B.V.",
    bedrag: 15.00,
    opmerking: "Dit is een opmerking...",
    lopendsaldo: -1009.56,
    tags: [
        "Vaste last", "Rekening"],
    post: [
        {
            _id: "Staatsloterij",
            soort: "Uitgaven",
            categorie: "Abonnementen",
            toegekend: 15.00
        }]
}

Ingelezen {
    # Eén object per rekening!!
    _id: OjectId(),
    soort: "transactie",
    data: {
        datum_in : 20200727,
        rekening: "NL38INGB0006110821",
        datum_van: 20200601,
        datum_tm : 20200630,
        trans_aantal: 124,
        trans_herkend: 112,
        bedrag_tot: -1500.2 }
    }

Ingelezen {
    _id: OjectId(),
    soort: "post",
    data: {
        datum_in : 20200727,
        soort: 2,
        categorie: 30,
        post: 150 }
    }
'''