import json
import os
import django
from pathlib import Path

# 🔹 Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portofolio.models import (
    Licenciatura,
    UnidadeCurricular,
    Universidade,
    Docente
)

BASE_DIR = Path(__file__).resolve().parents[2]
FILES_PATH = BASE_DIR / 'files'


def carregar_ucs():
    ficheiro = FILES_PATH / 'ULHT260-PT.json'

    print("A usar ficheiro:", ficheiro)
    print("Existe?", ficheiro.exists())

    if not ficheiro.exists():
        print("❌ Ficheiro não encontrado")
        return

    with open(ficheiro, encoding='utf-8') as f:
        dados = json.load(f)

    # 🔹 Universidade
    universidade, _ = Universidade.objects.get_or_create(
        nome="Universidade Lusófona"
    )

    # 🔹 Licenciatura
    nome_curso = dados.get("courseName", "Curso Desconhecido")

    licenciatura, _ = Licenciatura.objects.get_or_create(
        nome=nome_curso,
        defaults={
            "descricao": "Importado automaticamente",
            "duracao": 3,
            "universidade": universidade
        }
    )

    # =========================================================
    # 🔹 1. CRIAR DOCENTES (nível superior do JSON)
    # =========================================================
    docentes = []

    for teacher in dados.get("teachers", []):
        nome = teacher.get("fullName")
        email = teacher.get("email")
        codigo = teacher.get("employeeCode")
        grau = teacher.get("degree")

        if not nome:
            continue

        docente, _ = Docente.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nome": nome,
                "email": email,
                "grau": grau,
            }
        )

        docentes.append(docente)

    print(f"✅ Docentes criados: {len(docentes)}")

    # =========================================================
    # 🔹 2. CRIAR UCs
    # =========================================================
    for uc in dados.get("courseFlatPlan", []):

        codigo = uc.get("curricularUnitCode")
        nome = uc.get("curricularUnitName")
        ects = uc.get("ects", 0)
        ano = uc.get("curricularYear", 1)
        semestre = uc.get("semester")
        objetivos = uc.get("objectives", "")

        unidade, _ = UnidadeCurricular.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nome": nome,
                "ects": ects,
                "ano": ano,
                "semestre": semestre,
                "objectives": objetivos,
            }
        )

        # 🔹 associar licenciatura
        unidade.licenciatura = licenciatura
        unidade.save()

        # =========================================================
        # 🔹 3. ASSOCIAR DOCENTES À UC (mesmos para todas)
        # =========================================================
        for docente in docentes:
            unidade.docentes.add(docente)

    print("✅ UCs e docentes importados com sucesso!")


if __name__ == '__main__':
    carregar_ucs()
