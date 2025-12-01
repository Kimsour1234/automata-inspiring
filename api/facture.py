import json

def handler(request):
    # Vercel envoie tout en GET par défaut → on force POST seulement
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }

    # Lecture du body JSON
    try:
        data = json.loads(request.body)
    except:
        return {
            "statusCode": 400,
            "body": "Invalid JSON"
        }

    # --- Extraction arrays ---
    prestations = data.get("Prestations", [])
    prix_ht = data.get("Prix HT", [])
    prix_ttc = data.get("Prix TTC", [])
    tva_percent = data.get("TVA %", [])
    montant_tva = data.get("Montant TVA", [])

    # --- Format des lignes pour Google Docs ---
    lignes = []
    for i in range(len(prestations)):
        nom = prestations[i]
        pu = prix_ht[i]
        qte = 1
        total = pu * qte
        lignes.append(f"{nom} – {qte} × {pu} € = {total} €")

    prestations_text = "\n".join(lignes)

    # Totaux
    total_ht = sum(prix_ht)
    total_ttc = sum(prix_ttc)
    total_tva = sum(montant_tva)
    tva_unique = tva_percent[0] if tva_percent else 0

    result = {
        "LISTE_PRESTATIONS": prestations_text,
        "TOTAL_HT": total_ht,
        "TVA_POURCENT": tva_unique,
        "MONTANT_TVA": total_tva,
        "TOTAL_TTC": total_ttc
    }

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
