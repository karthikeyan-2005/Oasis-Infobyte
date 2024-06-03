import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# API details
API_KEY = "82c0bc52be4150e375de8804189ef80d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather_data(city):
    try:
        complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + city
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            return data
        else:
            messagebox.showerror("Error", "City Not Found")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return None

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.configure(bg="#e0e0e0")
        
        # Create and place widgets
        self.city_label = tk.Label(root, text="Enter City Name:", bg="#e0e0e0", font=("Helvetica", 14))
        self.city_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.city_entry = tk.Entry(root, font=("Helvetica", 14))
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.get_weather_button = tk.Button(root, text="Get Weather", command=self.show_weather, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.get_weather_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.weather_display = tk.Label(root, text="", justify="left", anchor="w", bg="#e0e0e0", font=("Helvetica", 14))
        self.weather_display.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        self.weather_icon = tk.Label(root, bg="#e0e0e0")
        self.weather_icon.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        
        self.unit_var = tk.StringVar(value="Celsius")
        self.unit_conversion_button = tk.Button(root, text="Convert Units", command=self.convert_units, font=("Helvetica", 14), bg="#008CBA", fg="white")
        self.unit_conversion_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        self.units_label = tk.Label(root, text="Temperature Units:", bg="#e0e0e0", font=("Helvetica", 14))
        self.units_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        
        self.celsius_radio = tk.Radiobutton(root, text="Celsius", variable=self.unit_var, value="Celsius", bg="#e0e0e0", font=("Helvetica", 14))
        self.celsius_radio.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        self.fahrenheit_radio = tk.Radiobutton(root, text="Fahrenheit", variable=self.unit_var, value="Fahrenheit", bg="#e0e0e0", font=("Helvetica", 14))
        self.fahrenheit_radio.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset, font=("Helvetica", 14), bg="#f44336", fg="white")
        self.reset_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
    
    def show_weather(self):
        city = self.city_entry.get()
        if city:
            data = get_weather_data(city)
            if data:
                self.display_weather(data)
        else:
            messagebox.showwarning("Input Error", "Please enter a city name")
    
    def display_weather(self, data):
        city = data["name"]
        country = data["sys"]["country"]
        temp_kelvin = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        icon_id = data["weather"][0]["icon"]
        
        # Convert temperature based on selected units
        if self.unit_var.get() == "Celsius":
            temp = temp_kelvin - 273.15
            temp_unit = "°C"
        else:
            temp = (temp_kelvin - 273.15) * 9/5 + 32
            temp_unit = "°F"
        
        weather_info = (f"City: {city}, {country}\n"
                        f"Temperature: {temp:.2f} {temp_unit}\n"
                        f"Weather: {weather}\n"
                        f"Wind Speed: {wind_speed} m/s\n"
                        f"Humidity: {humidity}%\n")
        
        self.weather_display.config(text=weather_info)
        
        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}.png"
        icon_data = requests.get(icon_url, stream=True).content
        icon_image = Image.open(io.BytesIO(icon_data))
        icon_image = icon_image.resize((100, 100), resample=Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.weather_icon.config(image=icon_photo)
        self.weather_icon.image = icon_photo
    
    def convert_units(self):
        self.show_weather()
    
    def reset(self):
        self.city_entry.delete(0, tk.END)
        self.weather_display.config(text="")
        self.weather_icon.config(image="")
        self.unit_var.set("Celsius")  # Reset unit to Celsius

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
