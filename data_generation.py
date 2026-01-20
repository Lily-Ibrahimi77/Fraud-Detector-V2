import pandas as pd
import numpy as np
from faker import Faker
import json

# --- CONFIG (Detta är din 'Source of Truth') ---
# Vi definierar hur fusk "ser ut" statistiskt, inte som fasta regler.
SIM_CONFIG = {
    "n_rows": 5000,
    "fraud_rate": 0.04,
    "features": {
        "days_to_claim": {
            "clean": {"mean": 180, "std": 90, "min": 0},
            "fraud": {"mean": 5, "std": 20, "min": 0} # Stor överlappning med clean!
        },
        "amount": {
            "clean": {"mean": 15000, "std": 10000},
            "fraud": {"mean": 45000, "std": 80000} # Vissa fuskare är giriga, andra inte.
        }
    }
}

fake = Faker('sv_SE')

def generate_smart_data(config):
    n = config["n_rows"]
    
    # 1. Skapa labels först - ingen mer 'if rand < 0.02' inuti loopen
    is_fraud = np.random.binomial(1, config["fraud_rate"], n)
    
    data = []
    for i in range(n):
        fraud = is_fraud[i]
        
        # 2. Generera värden från distributioner istället för fasta tal
        # Vi använder log-normal eller normalfördelning för att skapa realism
        f_cfg = config["features"]
        
        if fraud:
            days = max(0, int(np.random.normal(f_cfg["days_to_claim"]["fraud"]["mean"], 
                                             f_cfg["days_to_claim"]["fraud"]["std"])))
            amount = max(500, int(np.random.normal(f_cfg["amount"]["fraud"]["mean"], 
                                                 f_cfg["amount"]["fraud"]["std"])))
        else:
            days = max(0, int(np.random.normal(f_cfg["days_to_claim"]["clean"]["mean"], 
                                             f_cfg["days_to_claim"]["clean"]["std"])))
            amount = max(500, int(np.random.normal(f_cfg["amount"]["clean"]["mean"], 
                                                 f_cfg["amount"]["clean"]["std"])))

        # 3. Injicera "Dirty Data" direkt i källan
        # Vi slumpar fram felskrivningar i incident_type
        incidents = ['Vattenskada', 'Inbrott', 'Bilolycka', 'Glasskada']
        incident = np.random.choice(incidents)
        if np.random.rand() < 0.05: incident = incident.lower() # Smutsig text
        if np.random.rand() < 0.02: incident = "Oklart/Annat"     # Okända kategorier

        data.append({
            'claim_id': f"CLM-{1000+i}",
            'days_to_claim': days,
            'amount': amount,
            'incident_type': incident,
            'is_fraud': fraud
        })

    return pd.DataFrame(data)

# Kör och spara
df = generate_smart_data(SIM_CONFIG)
df.to_csv('if_insurance_claims_dirty.csv', index=False)
print("✅ Dynamisk data genererad. Ingen mer 100% precision nu!")