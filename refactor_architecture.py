import os
import shutil

def create_dirs(dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Create an __init__.py to make it a package
        init_file = os.path.join(d, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("# Init module\n")
        print(f"Created package: {d}")

def move_files(files, dest):
    for f in files:
        if os.path.exists(f):
            # Check if file exists to avoid crashes
            shutil.move(f, os.path.join(dest, f))
            print(f"Moved: {f} -> {dest}/")
        else:
            print(f"Skipped (not found): {f}")

def main():
    print("Starting Architecture Restructure...")
    
    # 1. Create Directories
    directories = [
        "frontend",
        "frontend/views",
        "frontend/assets",
        "backend",
        "backend/services",
        "backend/models",
        "backend/data"
    ]
    create_dirs(directories)
    
    # 2. Move Elements
    move_files(["styles.py", "components.py"], "frontend")
    
    move_files([
        "ayurveda_hero.png", "ayurveda_icon.png", 
        "dashboard_logo.png", "logo.png", "patient_history_icon.png"
    ], "frontend/assets")
    
    move_files([
        "appointments.py", "ayurveda.py", "blood_report.py", 
        "bmi_calculator.py", "diet_plan.py", "eye_test.py", 
        "fitness_planner.py", "hospital_finder.py", "medical_store.py", 
        "medicine_reminder.py", "mental_health.py", "report_scanner.py", 
        "skin_disease.py", "user_profile.py", "water_tracker.py"
    ], "frontend/views")
    
    move_files(["auth.py", "verify_connection.py", "ai_functions.py"], "backend/services")
    
    move_files(["model.pkl", "model.joblib", "train_model.py"], "backend/models")
    
    move_files(["appointments.csv", "dataset.csv", "users.csv"], "backend/data")
    
    print("\n✅ Restructure complete! Files moved successfully.")

if __name__ == "__main__":
    main()
