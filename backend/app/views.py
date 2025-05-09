
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from app.models import Document, DocumentChunk, Fonte, FonteLog, Tema, Anotacao, Favorito
from gqlalchemy import Memgraph

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        try:
            mg = Memgraph(host="memgraph", port=7687)
            total_entidades = list(mg.execute_and_fetch("MATCH (e:Entidade) RETURN count(e) AS total"))[0]['total']
            total_relacoes = list(mg.execute_and_fetch("MATCH ()-[r:APARECE_COM]->() RETURN count(r) AS total"))[0]['total']
        except:
            total_entidades = 0
            total_relacoes = 0

        return JsonResponse({
            "documentos": Document.objects.count(),
            "fontes": Fonte.objects.count(),
            "chunks": DocumentChunk.objects.count(),
            "entidades": total_entidades,
            "relacoes": total_relacoes,
            "logs": FonteLog.objects.count(),
        })

@staff_member_required
def painel_stats(request):
    try:
        mg = Memgraph(host="memgraph", port=7687)
        total_entidades = list(mg.execute_and_fetch("MATCH (e:Entidade) RETURN count(e) AS total"))[0]['total']
        total_relacoes = list(mg.execute_and_fetch("MATCH ()-[r:APARECE_COM]->() RETURN count(r) AS total"))[0]['total']
    except:
        total_entidades = 0
        total_relacoes = 0

    stats = {
        "Documentos": Document.objects.count(),
        "Fontes": Fonte.objects.count(),
        "Chunks": DocumentChunk.objects.count(),
        "Entidades": total_entidades,
        "Relações": total_relacoes,
        "Logs de coleta": FonteLog.objects.count()
    }

    html = render_to_string("app/painel_stats.html", {"stats": stats})
    return HttpResponse(html)

@staff_member_required
def painel_admin(request):
    return render(request, "app/painel_admin.html")

@method_decorator(staff_member_required, name='dispatch')
class MarcarFavoritoView(View):
    def post(self, request, doc_id):
        user = request.user
        doc = Document.objects.get(id=doc_id)
        fav, created = Favorito.objects.get_or_create(usuario=user, documento=doc)
        return JsonResponse({'favoritado': True, 'created': created})

    def delete(self, request, doc_id):
        user = request.user
        Favorito.objects.filter(usuario=user, documento_id=doc_id).delete()
        return JsonResponse({'favoritado': False})

@method_decorator(staff_member_required, name='dispatch')
class AnotacaoView(View):
    def post(self, request, doc_id):
        user = request.user
        texto = request.POST.get('texto', '')
        doc = Document.objects.get(id=doc_id)
        anotacao = Anotacao.objects.create(usuario=user, documento=doc, texto=texto)
        return JsonResponse({'anotado': True, 'id': anotacao.id})

    def get(self, request, doc_id):
        user = request.user
        notas = Anotacao.objects.filter(usuario=user, documento_id=doc_id).order_by('-criado_em')
        return JsonResponse([{"id": n.id, "texto": n.texto, "criado_em": n.criado_em} for n in notas], safe=False)


from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from app.vectorstore import carregar_faiss
from app.models import Document, Tema, Fonte
from langchain.embeddings import HuggingFaceEmbeddings

@csrf_exempt
def busca_hibrida(request):
    termo = request.GET.get("termo", "").strip()
    tema_id = request.GET.get("tema")
    fonte_id = request.GET.get("fonte")
    top_k = int(request.GET.get("top_k", 5))

    documentos_filtrados = Document.objects.all()
    if tema_id:
        documentos_filtrados = documentos_filtrados.filter(temas__id=tema_id)
    if fonte_id:
        documentos_filtrados = documentos_filtrados.filter(fonte_id=fonte_id)

    if termo:
        try:
            db = carregar_faiss()
            resultados = db.similarity_search_with_score(termo, k=top_k)
            docs_ids = [int(r[0].metadata.get("documento_id", 0)) for r in resultados if "documento_id" in r[0].metadata]
            docs_filtrados = documentos_filtrados.filter(id__in=docs_ids)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    else:
        docs_filtrados = documentos_filtrados.order_by('-data_publicacao')[:top_k]

    return JsonResponse([
        {
            "id": d.id,
            "titulo": d.titulo,
            "url": d.url,
            "data": d.data_publicacao,
            "fonte": d.fonte.nome,
            "temas": [t.nome for t in d.temas.all()],
            "resumo": d.texto_extraido[:300]
        }
        for d in docs_filtrados
    ], safe=False)


def listar_temas(request):
    temas = Tema.objects.all().values("id", "nome")
    return JsonResponse(list(temas), safe=False)

def listar_fontes(request):
    fontes = Fonte.objects.all().values("id", "nome")
    return JsonResponse(list(fontes), safe=False)


from django.contrib.auth.decorators import login_required

@login_required
def meus_favoritos(request):
    user = request.user
    favoritos = Favorito.objects.filter(usuario=user).select_related("documento__fonte").prefetch_related("documento__temas")
    return JsonResponse([
        {
            "id": f.documento.id,
            "titulo": f.documento.titulo,
            "fonte": f.documento.fonte.nome,
            "temas": [t.nome for t in f.documento.temas.all()],
            "url": f.documento.url,
            "data": f.documento.data_publicacao,
            "resumo": f.documento.texto_extraido[:300]
        }
        for f in favoritos
    ], safe=False)

@login_required
def minhas_anotacoes(request):
    user = request.user
    anotacoes = Anotacao.objects.filter(usuario=user).select_related("documento")
    return JsonResponse([
        {
            "documento_id": a.documento.id,
            "titulo": a.documento.titulo,
            "texto": a.texto,
            "criado_em": a.criado_em
        }
        for a in anotacoes
    ], safe=False)


from django.db.models import Count
from django.utils.timezone import now, timedelta

def dashboard_detalhes(request):
    dados = {}

    # Top temas por número de documentos
    dados["temas"] = list(
        Tema.objects.annotate(qtd=Count("document")).order_by("-qtd").values("nome", "qtd")[:7]
    )

    # Top fontes por número de documentos
    dados["fontes"] = list(
        Fonte.objects.annotate(qtd=Count("document")).order_by("-qtd").values("nome", "qtd")[:7]
    )

    # Documentos por data nos últimos 30 dias
    data_limite = now() - timedelta(days=30)
    docs_por_data = (
        Document.objects.filter(data_publicacao__gte=data_limite)
        .values("data_publicacao")
        .annotate(qtd=Count("id"))
        .order_by("data_publicacao")
    )
    dados["por_data"] = [
        {"data": d["data_publicacao"].strftime("%Y-%m-%d"), "qtd": d["qtd"]}
        for d in docs_por_data
    ]

    return JsonResponse(dados, safe=False)


def evolucao_tema(request, tema_id):
    try:
        tema = Tema.objects.get(id=tema_id)
    except Tema.DoesNotExist:
        return JsonResponse({"erro": "Tema não encontrado"}, status=404)

    dias = int(request.GET.get("dias", 60))
    limite = now() - timedelta(days=dias)

    docs = (
        Document.objects.filter(temas=tema, data_publicacao__gte=limite)
        .values("data_publicacao")
        .annotate(qtd=Count("id"))
        .order_by("data_publicacao")
    )

    return JsonResponse([
        {"data": d["data_publicacao"].strftime("%Y-%m-%d"), "qtd": d["qtd"]}
        for d in docs
    ], safe=False)


@login_required
def recomendacoes_usuario(request):
    user = request.user

    temas_ids = list(
        Tema.objects.filter(document__favorito__usuario=user)
        .union(
            Tema.objects.filter(document__anotacao__usuario=user)
        )
        .distinct()
        .values_list("id", flat=True)
    )

    documentos_sugeridos = Document.objects.filter(temas__id__in=temas_ids).exclude(
        favorito__usuario=user
    ).exclude(
        anotacao__usuario=user
    ).distinct().order_by('-data_publicacao')[:10]

    return JsonResponse([
        {
            "id": d.id,
            "titulo": d.titulo,
            "url": d.url,
            "data": d.data_publicacao,
            "fonte": d.fonte.nome,
            "temas": [t.nome for t in d.temas.all()],
            "resumo": d.texto_extraido[:300]
        }
        for d in documentos_sugeridos
    ], safe=False)


from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_date

@require_GET
@login_required
def exportar_documentos(request):
    tema_id = request.GET.get("tema")
    fonte_id = request.GET.get("fonte")
    formato = request.GET.get("formato", "csv")
    data_ini = parse_date(request.GET.get("data_ini") or "")
    data_fim = parse_date(request.GET.get("data_fim") or "")

    queryset = Document.objects.all()
    if tema_id:
        queryset = queryset.filter(temas__id=tema_id)
    if fonte_id:
        queryset = queryset.filter(fonte__id=fonte_id)
    if data_ini:
        queryset = queryset.filter(data_publicacao__gte=data_ini)
    if data_fim:
        queryset = queryset.filter(data_publicacao__lte=data_fim)

    if formato == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Título", "Fonte", "Data", "Temas", "Resumo"])
        for d in queryset:
            writer.writerow([d.titulo, d.fonte.nome, d.data_publicacao, ", ".join(t.nome for t in d.temas.all()), d.texto_extraido[:200]])
        response = HttpResponse(output.getvalue(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="exportacao.csv"'
        return response

    elif formato == "md":
        md = "# Exportação de Documentos\n\n"
        for d in queryset:
            md += f"## {d.titulo}\n"
            md += f"Fonte: {d.fonte.nome}\n"
            md += f"Data: {d.data_publicacao.strftime('%d/%m/%Y')}\n"
            md += f"Temas: {', '.join(t.nome for t in d.temas.all())}\n\n"
            md += d.texto_extraido[:300] + "\n\n---\n\n"
        response = HttpResponse(md, content_type="text/markdown")
        response['Content-Disposition'] = 'attachment; filename="exportacao.md"'
        return response

    elif formato == "pdf":
        html = "<h1>Exportação de Documentos</h1>"
        for d in queryset:
            html += f"<h2>{d.titulo}</h2>"
            html += f"<p><strong>Fonte:</strong> {d.fonte.nome} | <strong>Data:</strong> {d.data_publicacao.strftime('%d/%m/%Y')}</p>"
            html += f"<p><strong>Temas:</strong> {', '.join(t.nome for t in d.temas.all())}</p>"
            html += f"<p>{d.texto_extraido[:300]}</p><hr>"
        pdf_file = BytesIO()
        HTML(string=html).write_pdf(pdf_file)
        pdf_file.seek(0)
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="exportacao.pdf"'
        return response

    return JsonResponse({"erro": "Formato inválido"}, status=400)
