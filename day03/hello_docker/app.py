import sys 
import os

print("Hello from Docker")
print(f"Python Sürümü: {sys.version}")
print(f"APP_MODE: {os.environ.get('APP_MODE', 'Tanımlanmadı')}")