import json
import os
import django

# configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portofolio.models import Tfc

# caminho para o JSON
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'data', 'tfcs_2024_2025.json')


def run():
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        Tfc.objects.create(
            titulo=item.get('titulo'),
            autores=item.get('autores'),
            orientadores=item.get('orientadores'),
            licenciaturas=item.get('licenciaturas'),
            ano=item.get('ano'),
            sumario=item.get('sumario'),
            link_pdf=item.get('link_pdf'),
            imagem=item.get('imagem'),
            palavras_chave=item.get('palavras_chave'),
            areas=item.get('areas'),
            tecnologias_usadas=item.get('tecnologias_usadas'),
            rating=item.get('rating', 3)  
        )


if __name__ == '__main__':
    run()
