
from app.models import Tema, Document, Anotacao
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime

User = get_user_model()

def gerar_relatorio_tema(tema_id: int, user_id: int = None) -> str:
    try:
        tema = Tema.objects.get(id=tema_id)
    except Tema.DoesNotExist:
        return "# Tema não encontrado"

    documentos = Document.objects.filter(temas=tema).order_by('-data_publicacao')
    markdown = f"# Relatório Temático: {tema.nome}\n\n"
    markdown += f"**Descrição:** {tema.descricao or 'N/A'}\n"
    markdown += f"**Total de documentos:** {documentos.count()}\n\n"

    for doc in documentos:
        markdown += f"## {doc.titulo}\n"
        markdown += f"Publicado em: {localtime(doc.data_publicacao).strftime('%d/%m/%Y') if doc.data_publicacao else 'Data desconhecida'}\n\n"
        markdown += f"{doc.texto_extraido[:300]}...\n\n"

        if user_id:
            anotacoes = Anotacao.objects.filter(usuario_id=user_id, documento=doc)
            for nota in anotacoes:
                markdown += f"> Nota ({localtime(nota.criado_em).strftime('%d/%m/%Y %H:%M')}): {nota.texto}\n\n"

        markdown += "---\n\n"

    return markdown


def gerar_relatorio_tematico_personalizado(user_id: int, tema_id: int) -> str:
    try:
        tema = Tema.objects.get(id=tema_id)
        user = User.objects.get(id=user_id)
    except (Tema.DoesNotExist, User.DoesNotExist):
        return "# Tema ou usuário não encontrado"

    favoritos_ids = Favorito.objects.filter(usuario=user, documento__temas=tema).values_list("documento_id", flat=True)
    anotacoes_ids = Anotacao.objects.filter(usuario=user, documento__temas=tema).values_list("documento_id", flat=True)
    doc_ids = set(favoritos_ids) | set(anotacoes_ids)

    documentos = Document.objects.filter(id__in=doc_ids).order_by('-data_publicacao')

    markdown = f"# Relatório Personalizado – {tema.nome}\n\n"
    markdown += f"Usuário: {user.get_full_name() or user.username}\n\n"
    markdown += f"**Total de documentos selecionados:** {documentos.count()}\n\n"

    for doc in documentos:
        markdown += f"## {doc.titulo}\n"
        markdown += f"Publicado em: {localtime(doc.data_publicacao).strftime('%d/%m/%Y') if doc.data_publicacao else 'Data desconhecida'}\n\n"
        markdown += f"{doc.texto_extraido[:300]}...\n\n"

        notas = Anotacao.objects.filter(usuario=user, documento=doc)
        for nota in notas:
            markdown += f"> Nota ({localtime(nota.criado_em).strftime('%d/%m/%Y %H:%M')}): {nota.texto}\n\n"

        markdown += "---\n\n"

    return markdown
