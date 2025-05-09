from django.urls import path
from . import views

app_name = "rag_integration"

from . import views

from . import views

from . import views

from . import views

from . import views

from . import views

urlpatterns = [
    path('api/exportar/', views.exportar_documentos),

    path('api/recomendacoes/', views.recomendacoes_usuario),

    path('api/tema/evolucao/<int:tema_id>/', views.evolucao_tema),

    path('api/dashboard/detalhes/', views.dashboard_detalhes),

    path('api/meus-favoritos/', views.meus_favoritos),
    path('api/minhas-anotacoes/', views.minhas_anotacoes),

    path('api/temas/', views.listar_temas),
    path('api/fontes/', views.listar_fontes),
    path('api/busca/', views.busca_hibrida),

    path("query/", views.QueryView.as_view(), name="query"),
]
