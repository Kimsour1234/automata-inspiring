from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Lire body brut
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length)
        body_str = raw_body.decode("utf-8")

        # --- PARSE SAFE JSON ---
        try:
            data = json.loads(body_str)
        except Exception:
            # Si JSON pourri → pas de crash → valeurs vides
            data = {}

        # --- EXTRACT SAFE (ne crash JAMAIS) ---
        prestations   = self.safe_list(data, "Prestations")
        prix_ht       = self.safe_list(data, "Prix_HT")
        prix_ttc      = self.safe_list(data, "Prix_TTC")
        tva_percent   = self.safe_list(data, "TVA_%")
        montant_tva   = self.safe_list(data, "Montant_TVA")

        # ---- Lignes prestations ----
        lignes = []
        n = len(prestations)

        for i in range(n):
            nom = str(prestations[i])
            ht  = self.safe_get(prix_ht, i)
            ttc = self.safe_get(prix_ttc, i)
            lignes.append(f"- {nom} : {ht} € HT → {ttc} € TTC")

        liste_prestations = "\n".join(lignes)

        # ---- Totaux safe ----
        total_ht  = sum([v for v in prix_ht if isinstance(v, (int, float))])
        total_ttc = sum([v for v in prix_ttc if isinstance(v, (int, float))])
        total_tva = sum([v for v in montant_tva if isinstance(v, (int, float))])
        tva_unique = tva_percent[0] if len(tva_percent) > 0 else 0

        result = {
            "LISTE_PRESTATIONS": liste_prestations,
            "TOTAL_HT": total_ht,
            "TVA_POURCENT": tva_unique,
            "MONTANT_TVA": total_tva,
            "TOTAL_TTC": total_ttc
        }

        # ---- SEND ----
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode("utf-8"))

    # --- UTILITAIRES SAFE ---
    def safe_list(self, data, key):
        """Retourne toujours une LISTE (ne crash jamais)"""
        val = data.get(key, [])
        if isinstance(val, list):
            return val
        return [val] if val else []

    def safe_get(self, arr, i):
        """Retourne arr[i] ou 0 si inexistant"""
        try:
            return arr[i]
        except:
            return 0
