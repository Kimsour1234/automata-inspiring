import json

def handle(req):
    data = json.loads(req)

    prestations = data.get("Prestations", [])
    prix_ht = data.get("Prix HT", [])
    prix_ttc = data.get("Prix TTC", [])
    tva_percent = data.get("TVA %", [])
    montant_tva = data.get("Montant TVA", [])

    lignes = []

    # Génère chaque ligne : "Nom – 1 × 200 € = 200 €"
    for i in range(len(prestations)):
        nom = prestations[i]
        pu = prix_ht[i]        # prix unitaire HT
        qte = 1                # On force 1 par prestation (comme tu veux)
        total = prix_ht[i]     # total = PU × 1

        lignes.append(f"{nom} – {qte} × {pu} € = {total} €")

    # Format final multi-lignes
    prestations_text = "\n".join(lignes)

    # Totaux
    total_ht = sum(prix_ht)
    total_ttc = sum(prix_ttc)
    total_tva = sum(montant_tva)
    tva_unique = tva_percent[0] if tva_percent else 0

    return json.dumps({
        "LISTE_PRESTATIONS": prestations_text,
        "TOTAL_HT": total_ht,
        "TVA_POURCENT": tva_unique,
        "MONTANT_TVA": total_tva,
        "TOTAL_TTC": total_ttc
    })
