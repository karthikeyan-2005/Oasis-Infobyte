import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.label_font = ("Arial", 10)
        self.result_font = ("Arial", 12, "bold")

        self.weight_label = tk.Label(root, text="Enter Weight (kg):", font=self.label_font, bg="#f0f0f0")
        self.weight_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=0, column=1, padx=10, pady=10)

        self.height_label = tk.Label(root, text="Enter Height (m):", font=self.label_font, bg="#f0f0f0")
        self.height_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10)

        self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi, bg="#4CAF50", fg="white", font=self.label_font)
        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = tk.Label(root, text="", font=self.result_font, bg="#f0f0f0")
        self.result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.figure = plt.Figure(figsize=(4, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, root)
        self.chart_canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.bmi_data = []
        self.load_bmi_data()

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = weight / (height ** 2)
            category = self.get_category(bmi)
            self.result_label.config(text=f"Your BMI: {bmi:.2f} ({category})", fg=self.get_color(category))
            self.bmi_data.append((weight, height, bmi, category))
            self.save_bmi_data(weight, height, bmi, category)
            self.plot_bmi_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for weight and height.")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Height cannot be zero.")

    def get_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal Weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def get_color(self, category):
        if category == "Underweight":
            return "#FF6347"
        elif category == "Normal Weight":
            return "#008000"
        elif category == "Overweight":
            return "#FFA500"
        else:
            return "#FF0000"

    def plot_bmi_data(self):
        self.ax.clear()
        bmi_values = [data[2] for data in self.bmi_data]
        self.ax.hist(bmi_values, bins=10, color='#007ACC', edgecolor='black')
        self.ax.set_xlabel('BMI')
        self.ax.set_ylabel('Frequency')
        self.ax.set_title('BMI Distribution')
        self.chart_canvas.draw()

    def save_bmi_data(self, weight, height, bmi, category):
        with open("bmi_data.txt", "a") as file:
            file.write(f"{weight},{height},{bmi},{category}\n")

    def load_bmi_data(self):
        try:
            with open("bmi_data.txt", "r") as file:
                for line in file:
                    weight, height, bmi, category = line.strip().split(",")
                    self.bmi_data.append((float(weight), float(height), float(bmi), category))
                self.plot_bmi_data()
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()
