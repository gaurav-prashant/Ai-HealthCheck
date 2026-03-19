# ============================================================
# train_model.py — Improved Model with More Diseases & Symptoms
# ============================================================

import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# ── SYMPTOMS (41 symptoms) ──
SYMPTOMS = [
    "Fever", "Cough", "Headache", "Fatigue", "Vomiting", "Cold",
    "Body Pain", "Sore Throat", "Breathlessness", "Chest Pain",
    "Dizziness", "Diarrhea", "Nausea", "Loss of Smell", "Loss of Taste",
    "Runny Nose", "Sneezing", "Joint Pain", "Muscle Pain", "Back Pain",
    "Skin Rash", "Itching", "Swelling", "Weight Loss", "Night Sweats",
    "Chills", "Sweating", "Weakness", "Loss of Appetite", "Stomach Pain",
    "Bloating", "Constipation", "Burning Urination", "Frequent Urination",
    "Eye Redness", "Ear Pain", "Neck Stiffness", "Confusion",
    "High Blood Pressure", "Palpitations", "Anxiety"
]

# ── DISEASES & THEIR SYMPTOM PATTERNS ──
DISEASE_PATTERNS = {
    "Flu / Influenza": {
        "required": ["Fever", "Cough", "Body Pain", "Fatigue", "Headache"],
        "optional": ["Chills", "Sweating", "Sore Throat", "Runny Nose", "Muscle Pain"],
        "samples": 120
    },
    "Common Cold": {
        "required": ["Cold", "Runny Nose", "Sneezing"],
        "optional": ["Sore Throat", "Cough", "Headache", "Fatigue", "Fever"],
        "samples": 100
    },
    "COVID-19": {
        "required": ["Fever", "Cough", "Fatigue"],
        "optional": ["Loss of Smell", "Loss of Taste", "Breathlessness", "Headache", "Body Pain", "Diarrhea"],
        "samples": 120
    },
    "Migraine": {
        "required": ["Headache", "Nausea"],
        "optional": ["Vomiting", "Dizziness", "Eye Redness", "Sensitivity to Light", "Fatigue"],
        "samples": 100
    },
    "Food Poisoning": {
        "required": ["Vomiting", "Diarrhea", "Stomach Pain", "Nausea"],
        "optional": ["Fever", "Weakness", "Chills", "Loss of Appetite", "Bloating"],
        "samples": 100
    },
    "Heart Problem": {
        "required": ["Chest Pain", "Palpitations"],
        "optional": ["Breathlessness", "Sweating", "Dizziness", "Anxiety", "Fatigue", "High Blood Pressure"],
        "samples": 100
    },
    "Typhoid": {
        "required": ["Fever", "Weakness", "Stomach Pain"],
        "optional": ["Headache", "Loss of Appetite", "Constipation", "Diarrhea", "Night Sweats", "Chills"],
        "samples": 100
    },
    "Dengue": {
        "required": ["Fever", "Joint Pain", "Headache", "Eye Redness"],
        "optional": ["Skin Rash", "Muscle Pain", "Nausea", "Vomiting", "Fatigue", "Chills"],
        "samples": 100
    },
    "Malaria": {
        "required": ["Fever", "Chills", "Sweating"],
        "optional": ["Headache", "Muscle Pain", "Nausea", "Vomiting", "Fatigue", "Dizziness"],
        "samples": 100
    },
    "Pneumonia": {
        "required": ["Fever", "Cough", "Breathlessness", "Chest Pain"],
        "optional": ["Fatigue", "Sweating", "Chills", "Muscle Pain", "Confusion"],
        "samples": 100
    },
    "Diabetes": {
        "required": ["Frequent Urination", "Fatigue", "Weight Loss"],
        "optional": ["Blurred Vision", "Burning Urination", "Weakness", "Loss of Appetite", "Nausea"],
        "samples": 100
    },
    "Urinary Tract Infection": {
        "required": ["Burning Urination", "Frequent Urination"],
        "optional": ["Fever", "Back Pain", "Stomach Pain", "Nausea", "Weakness", "Fatigue"],
        "samples": 100
    },
    "Arthritis": {
        "required": ["Joint Pain", "Swelling"],
        "optional": ["Fatigue", "Fever", "Muscle Pain", "Weakness", "Back Pain", "Body Pain"],
        "samples": 100
    },
    "Asthma": {
        "required": ["Breathlessness", "Cough", "Chest Pain"],
        "optional": ["Fatigue", "Anxiety", "Sweating", "Weakness"],
        "samples": 100
    },
    "Meningitis": {
        "required": ["Headache", "Fever", "Neck Stiffness"],
        "optional": ["Vomiting", "Confusion", "Eye Redness", "Chills", "Skin Rash"],
        "samples": 80
    },
    "Appendicitis": {
        "required": ["Stomach Pain", "Fever", "Nausea"],
        "optional": ["Vomiting", "Loss of Appetite", "Constipation", "Bloating", "Weakness"],
        "samples": 80
    },
    "Jaundice / Hepatitis": {
        "required": ["Fatigue", "Loss of Appetite", "Nausea"],
        "optional": ["Fever", "Stomach Pain", "Weakness", "Weight Loss", "Vomiting"],
        "samples": 80
    },
    "Chickenpox": {
        "required": ["Fever", "Skin Rash", "Itching"],
        "optional": ["Headache", "Fatigue", "Loss of Appetite", "Body Pain", "Chills"],
        "samples": 80
    },
    "Measles": {
        "required": ["Fever", "Skin Rash", "Cough"],
        "optional": ["Runny Nose", "Eye Redness", "Loss of Appetite", "Fatigue", "Headache"],
        "samples": 80
    },
    "Tuberculosis": {
        "required": ["Cough", "Night Sweats", "Weight Loss", "Fatigue"],
        "optional": ["Fever", "Chest Pain", "Loss of Appetite", "Weakness", "Breathlessness"],
        "samples": 80
    },
}

# ── GENERATE DATASET ──
def generate_dataset():
    symptom_list = SYMPTOMS
    rows = []

    for disease, pattern in DISEASE_PATTERNS.items():
        required = pattern["required"]
        optional = pattern["optional"]
        n        = pattern["samples"]

        for _ in range(n):
            row = {s: 0 for s in symptom_list}

            # Add required symptoms (with small chance of missing one)
            for sym in required:
                if sym in symptom_list:
                    row[sym] = 1 if np.random.random() > 0.05 else 0

            # Add optional symptoms randomly
            num_optional = np.random.randint(1, min(len(optional)+1, 6))
            chosen = np.random.choice(optional, size=min(num_optional, len(optional)), replace=False)
            for sym in chosen:
                if sym in symptom_list:
                    row[sym] = 1

            # Add 1-2 random noise symptoms (real world noise)
            noise_syms = [s for s in symptom_list if row[s] == 0]
            if noise_syms and np.random.random() > 0.7:
                noise = np.random.choice(noise_syms, size=min(2, len(noise_syms)), replace=False)
                for s in noise:
                    row[s] = 1

            row["Disease"] = disease
            rows.append(row)

    df = pd.DataFrame(rows)
    print(f"✅ Dataset created: {len(df)} samples, {len(DISEASE_PATTERNS)} diseases")
    return df

# ── TRAIN MODEL ──
def train():
    print("🧠 Generating dataset...")
    df = generate_dataset()

    X = df[SYMPTOMS].values
    y = df["Disease"].values

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("🤖 Training models...")

    # Fast & Accurate: Random Forest only
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )

    # Train
    rf.fit(X_train, y_train)
    ensemble = rf  # Use RF as final model

    # Evaluate
    y_pred    = rf.predict(X_test)
    accuracy  = accuracy_score(y_test, y_pred)

    # Cross validation
    cv_scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')

    print(f"\n✅ Results:")
    print(f"   Test Accuracy:  {accuracy*100:.2f}%")
    print(f"   CV Accuracy:    {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")
    print(f"   Diseases:       {len(DISEASE_PATTERNS)}")
    print(f"   Symptoms:       {len(SYMPTOMS)}")
    print(f"   Training Samples: {len(X_train)}")

    # Save model
    model_data = {
        "model":    rf,
        "accuracy": accuracy,
        "symptoms": SYMPTOMS,
        "diseases": list(DISEASE_PATTERNS.keys()),
        "cv_score": cv_scores.mean()
    }

    with open("model.pkl", "wb") as f:
        pickle.dump(model_data, f)

    print(f"\n✅ Model saved as model.pkl")
    print(f"🎯 Final Accuracy: {accuracy*100:.2f}%")

    # Show per-disease accuracy
    print("\n📊 Sample predictions:")
    for i in range(min(5, len(y_test))):
        status = "✅" if y_pred[i] == y_test[i] else "❌"
        print(f"   {status} Predicted: {y_pred[i][:20]:<25} Actual: {y_test[i][:20]}")

if __name__ == "__main__":
    train()