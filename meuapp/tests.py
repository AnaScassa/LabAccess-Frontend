from django.test import TestCase




def acessos_usr():
    from meuapp.models import Acesso  # importa o modelo certo

    vistos = set()
    duplicados = []

    for acesso in Acesso.objects.order_by('usuario', 'data_acesso'):
        chave = (
            acesso.usuario_id,
            acesso.data_acesso,
            acesso.desc_area,
            acesso.ent_sai,
        )
        print(chave)
        if chave in vistos:
            duplicados.append(acesso.id)
        else:
            vistos.add(chave)

    Acesso.objects.filter(id__in=duplicados).delete()

    print(f"{len(duplicados)} registros duplicados removidos com sucesso. {len(vistos)}")
