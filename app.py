import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# ---------------- ML MODEL ---------------- #

data = {
    'Age': [25, 30, 45, 50, 35, 40],
    'BMI': [22.0, 28.5, 30.0, 26.7, 24.5, 32.0],
    'BloodPressure': [120, 140, 135, 128, 118, 145],
    'SugarLevel': [90, 150, 170, 130, 110, 200],
    'Gender': [1, 0, 0, 1, 1, 0],
    'Risk': [0, 1, 1, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df[['Age', 'BMI', 'BloodPressure', 'SugarLevel', 'Gender']]
y = df['Risk']

# ✅ FIX: added random_state
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# ---------------- GUI ---------------- #

app = tk.Tk()
app.title("🩺 Health Sensors")
app.geometry("470x600")
app.configure(bg="#eaf6fb")

# Header
header_frame = tk.Frame(app, bg="#3498db", height=70)
header_frame.pack(fill="x")

header_label = tk.Label(
    header_frame,
    text="🧬 Health Sensor Machine",
    font=("Helvetica", 20, "bold"),
    fg="white",
    bg="#3498db"
)
header_label.pack(pady=20)

# Gender
gender_var = tk.IntVar(value=1)

gender_frame = tk.LabelFrame(
    app, text="Select Gender", font=("Arial", 11, "bold"),
    bg="#d6f1ff", fg="#34495e", padx=10, pady=5
)
gender_frame.pack(pady=10)

tk.Radiobutton(gender_frame, text="👨 Male", variable=gender_var, value=1,
               bg="#d6f1ff").pack(side="left", padx=20)

tk.Radiobutton(gender_frame, text="👩 Female", variable=gender_var, value=0,
               bg="#d6f1ff").pack(side="left", padx=20)

# Input creator
def create_input(label_text):
    frame = tk.Frame(app, bg="#d6f1ff")
    frame.pack(pady=5)

    label = tk.Label(frame, text=label_text + ":", width=18,
                     anchor='w', bg="#d6f1ff", font=("Arial", 11))
    label.pack(side="left", padx=5)

    entry = tk.Entry(frame, font=("Arial", 11), width=22)
    entry.pack(side="left")

    return entry

# Inputs
age_entry = create_input("🧓 Age")
bmi_entry = create_input("📏 BMI")
bp_entry = create_input("💓 Blood Pressure")
sugar_entry = create_input("🍬 Sugar Level")

# Result
result_label = tk.Label(app, text="", font=("Arial", 14, "bold"), bg="#eaf6fb")
result_label.pack(pady=15)

info_label = tk.Label(app, text="", font=("Arial", 10), bg="#eaf6fb", fg="#555")
info_label.pack()

# ---------------- FUNCTIONS ---------------- #

def validate_inputs(age, bmi, bp, sugar):
    if age <= 0 or age > 120:
        return "Invalid Age"
    if bmi <= 0 or bmi > 60:
        return "Invalid BMI"
    if bp <= 0 or bp > 250:
        return "Invalid Blood Pressure"
    if sugar <= 0 or sugar > 500:
        return "Invalid Sugar Level"
    return None


def predict_risk():
    try:
        age = float(age_entry.get())
        bmi = float(bmi_entry.get())
        bp = float(bp_entry.get())
        sugar = float(sugar_entry.get())
        gender = gender_var.get()

        # ✅ NEW: validation
        error = validate_inputs(age, bmi, bp, sugar)
        if error:
            messagebox.showerror("Invalid Input", error)
            return

        input_data = pd.DataFrame([[age, bmi, bp, sugar, gender]],
                                  columns=X.columns)

        prediction = model.predict(input_data)[0]

        if prediction == 1:
            result_label.config(text="⚠️ Health Risk Detected", fg="#e74c3c")
        else:
            result_label.config(text="✅ You Are Healthy", fg="#2ecc71")

        info_label.config(
            text=f"Age: {age}, BMI: {bmi}, BP: {bp}, Sugar: {sugar}, Gender: {'Male' if gender == 1 else 'Female'}"
        )

    except ValueError:
        messagebox.showerror("Invalid Input", "❌ Enter numeric values only.")


def clear_fields():
    for entry in [age_entry, bmi_entry, bp_entry, sugar_entry]:
        entry.delete(0, tk.END)

    gender_var.set(1)
    result_label.config(text="")
    info_label.config(text="")

# Buttons
tk.Button(app, text="🔍 Predict Risk", command=predict_risk,
          bg="#3498db", fg="white", width=18, height=2).pack(pady=10)

tk.Button(app, text="🔁 Clear Fields", command=clear_fields,
          bg="#bdc3c7", width=15).pack()

# Footer
tk.Label(app, text="Made with ❤️ by Alishba",
         bg="#eaf6fb", fg="#7f8c8d").pack(side="bottom", pady=15)

app.mainloop()