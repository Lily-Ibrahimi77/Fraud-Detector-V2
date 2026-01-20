import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# 1. Ladda den "smutsiga" datan
# Vi använder den fil som vår nya generator skapade
try:
    df = pd.read_csv('if_insurance_claims_dirty.csv')
except FileNotFoundError:
    df = pd.read_csv('if_insurance_claims.csv') # Fallback

# --- 2. Feature Selection (Äpplena är redan skalade!) ---
# Vi behöver inte längre räkna ut dagar, de finns redan i 'days_to_claim'.
# Vi väljer bara de kolumner som faktiskt behövs för träningen.
features = ['amount', 'days_to_claim']
X = df[features]
y = df['is_fraud']

# Hantera kategorisk data (incident_type)
# Vi lägger till dummy_na=True för att fånga upp "Oklart/Annat" eller saknade värden
X = pd.concat([X, pd.get_dummies(df['incident_type'], dummy_na=True)], axis=1)

# KARPATHY FIX: Tvinga alla kolumnnamn till strängar (fixar ditt förra error)
X.columns = X.columns.astype(str) 

# --- 3. Imputation (Hanterar NaN-värden) ---
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# Fortsätt med train_test_split och modellträning som vanligt...


# 3. Robust Splitting
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

# 4. Träna modellen med Cross-Validation
# Vi litar inte på ett enda testresultat. Vi kör 5 olika tester (K-Fold).
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
cv_scores = cross_val_score(model, X_train, y_train, cv=5)

print(f"--- MODELLENS STABILITET (CV) ---")
print(f"Genomsnittlig precision: {cv_scores.mean():.2f} (+/- {cv_scores.std():.2f})")

model.fit(X_train, y_train)

# 5. Från binärt val till Risk Score
# En senior lösning säger inte bara ja/nej. Den ger en grad av misstanke.
y_probs = model.predict_proba(X_test)[:, 1] # Sannolikhet för klass 1 (Fusk)

# 6. Visualisera Beslutsunderlag
importances = pd.Series(model.feature_importances_, index=X.columns)
importances.nlargest(5).plot(kind='barh', color='#00548F')
plt.title('Vad driver riskbedömningen?')
plt.show()

print("\n--- TEST PÅ OSYNLIG DATA ---")
y_pred = (y_probs > 0.7).astype(int) # Vi sätter en hög tröskel för att minska falska anklagelser
print(classification_report(y_test, y_pred))

# Beräkna sannolikhet för hela datasetet för rapporten
df['fraud_probability'] = model.predict_proba(imputer.transform(X))[:, 1]
df.to_csv('if_claims_with_scores.csv', index=False)