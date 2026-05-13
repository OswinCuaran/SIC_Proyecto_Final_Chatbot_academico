import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(__file__))

def cargar_datos():
    """Carga los documentos en ChromaDB antes de iniciar el servidor"""
    print("=" * 50)
    print("  CHATBOT ACADÉMICO UNAL - Iniciando sistema")
    print("=" * 50)
    print("\nCargando base de conocimiento...")
    
    intentos = 3
    for intento in range(1, intentos + 1):
        try:
            print(f"  Intento {intento}/{intentos}...")
            resultado = subprocess.run(
                [sys.executable, os.path.join(os.path.dirname(__file__), 'cargar_chroma.py')],
                capture_output=False,
                text=True,
                cwd=os.path.dirname(__file__)
            )
            
            if resultado.returncode == 0:
                print("\nBase de conocimiento cargada exitosamente")
                return True
            else:
                print(f"\nError en intento {intento}")
                if intento < intentos:
                    print("   Reintentando...")
                    
        except Exception as e:
            print(f"\nError: {e}")
            if intento < intentos:
                print("   Reintentando...")
    
    print("\n❌ No se pudo cargar la base de conocimiento después de 3 intentos")
    print("   El servidor iniciará pero puede no responder correctamente")
    return False

if __name__ == '__main__':
    # Cargar datos primero
    cargado = cargar_datos()
    
    # Iniciar servidor
    print("\nIniciando servidor...")
    print("   URL: http://localhost:8000")
    print("   Presiona Ctrl+C para detener")
    print("=" * 50 + "\n")
    
    from app.main import app
    app.run(debug=False, port=8000, host='0.0.0.0')