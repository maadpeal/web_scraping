from scripts.QuickSiteScript import QuickSiteScript
from scripts.PhoneSiteScript import PhoneSiteScript
import concurrent.futures
import os


def execute_script(script):
    return script.process()


if __name__ == "__main__":
    folder_csv = "csv"
    folder_log = "logs"
    os.makedirs(folder_csv, exist_ok=True)
    os.makedirs(folder_log, exist_ok=True)
    quick_script = QuickSiteScript()
    phone_script = PhoneSiteScript()

    # Crear un ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Iniciar los scripts en paralelo y esperar a que ambos terminen
        results = list(executor.map(execute_script, [quick_script, phone_script]))

    # Imprimir los resultados
    for result in results:
        print(result)
