# Crie um arquivo inserir_assinaturas.py com este código:


from database.queries import get_db_cursor

import base64

import os


def inserir_assinatura(tipo, nome, cargo, caminho_imagem):

    try:

        with open(caminho_imagem, 'rb') as f:

            imagem_bytes = f.read()

        with get_db_cursor(commit=True) as cursor:

            cursor.execute("""

                UPDATE assinaturas_certificados 

                SET nome = %s, cargo = %s, imagem_assinatura = %s, ativo = 1

                WHERE tipo = %s

            """, (nome, cargo, imagem_bytes, tipo))

            print(f"✅ Assinatura {tipo} inserida!")

    except Exception as e:

        print(f"Erro: {e}")


# Executar

inserir_assinatura('coordenacao', 'Marian', 'Coordenador de Treinamentos', 'assinatura_coordenacao.png')

inserir_assinatura('gerencia', 'Fabiana', 'Gerente de RH', 'assinatura_gerencia.png')

inserir_assinatura('diretor', 'Wamberto', 'Diretor Geral', 'assinatura_diretor.png')
