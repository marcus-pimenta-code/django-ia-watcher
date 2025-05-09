
from celery import shared_task
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from app.relatorio import gerar_relatorio_tematico_personalizado
from markdown2 import markdown
from weasyprint import HTML
import tempfile

User = get_user_model()

@shared_task
def enviar_relatorio_por_email(user_id, tema_id):
    user = User.objects.get(id=user_id)
    md = gerar_relatorio_tematico_personalizado(user_id, tema_id)
    html = markdown(md)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        HTML(string=html).write_pdf(tmp.name)
        tmp.flush()
        email = EmailMessage(
            subject=f"Relatório do Tema",
            body=f"Olá {user.first_name or user.username},\n\nSegue em anexo o relatório solicitado.",
            from_email="observatorio@exemplo.com",
            to=[user.email]
        )
        email.attach("relatorio.pdf", tmp.read(), "application/pdf")
        email.send()
