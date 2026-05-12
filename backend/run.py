import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.main import app

if __name__ == '__main__':
    print("Iniciando servidor Chatbot Académico UNAL...")
    print("API disponible en: http://localhost:8000")
    print("Presiona Ctrl+C para detener")
    app.run(debug=True, port=8000, host='0.0.0.0')