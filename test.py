my_proposal = {
    "title": "Tesla Model 3 Configurator",
    "date": "29 novembre 2016",
    "place": "Philadelphie",
    "version": "v1",
    "sect": {
        "email": "bf@bf-printer.com",
        "logo": "tests/samples/tesla_logo.png",
        "name": "BF Printer \\& Co",
    },
    "legal": {
        "address": {
            "city": "Philadelphie",
            "line1": "E Thompson Saint",
            "zip": "19125",
        },
        "siret": "999999999 00099",
    },
    "author": {
        "civility": "M.",
        "mobile": "07.73.35.51.00",
        "name": "Benjamin Franklin",
        "role": "membre",
    },
    "client": {
        "contact": {
            "civility": "M.",
            "name": "Elon Musk",
            "role": "CEO",
            "sason": "son",
        },
        "legal": {
            "address": {
                "city": "Chambourcy",
                "line1": "103 Route de Mantes",
                "zip": "78240",
            },
            "siret": "524335262 00084",
        },
        "name": "Tesla",
    },
    "object": "The current proposal includes ...\n",
    "prestations": [
        {
            "description": "Files for describing the steps of product configuration, their prices, etc.",
            "price": 5000,
            "title": "Definition of configurations",
        }
    ],
}

my_invoices = {
    "sect": {"email": "bf@bf-printer.com", "name": "BF Printer \\& Co"},
    "legal": {
        "address": {
            "city": "Philadelphie",
            "line1": "E Thompson Saint",
            "zip": "19125",
        },
        "siret": "999999999 00099",
    },
    "author": {
        "civility": "M.",
        "mobile": "07.73.35.51.00",
        "name": "Benjamin Franklin",
        "role": "membre",
    },
    "client": {
        "contact": {
            "civility": "M.",
            "name": "Elon Musk",
            "role": "CEO",
            "sason": "son",
        },
        "legal": {
            "address": {
                "city": "Chambourcy",
                "line1": "103 Route de Mantes",
                "zip": "78240",
            },
            "siret": "524335262 00084",
        },
        "name": "Tesla",
    },
    "invoices": [
        {
            "date": "5 janvier 2017",
            "lines": [{"price": 12000, "title": "Acompte devis 16-TESLA-01"}],
            "number": "17001",
            "vat_rate": 20,
        }
    ],
}
