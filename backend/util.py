import re

TRESHOLDS = [5, 10, 30, 50]


def check_huttunen(huttuset):
    res = []

    for h in huttuset:
        try:
            lower_bound = int(h["amount"])
        except ValueError:
            lower_bound = int(re.search(r"(\d+)", h["amount"])[1])

        if lower_bound <= TRESHOLDS[0]:
            huttusukko = 0
        elif lower_bound <= TRESHOLDS[1]:
            huttusukko = 1
        elif lower_bound <= TRESHOLDS[2]:
            huttusukko = 2
        elif lower_bound <= TRESHOLDS[3]:
            huttusukko = 3
        else:
            huttusukko = 4

        res.append({
            "id": h["id"],
            "icon": huttusukko,
            "amount": h["amount"]
        })

    return res
