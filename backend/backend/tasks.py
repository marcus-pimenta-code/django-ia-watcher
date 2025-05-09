from celery import shared_task
from .models import Document
from fontes.models import Source
import requests
from bs4 import BeautifulSoup
import fitz # PyMuPDF
import docx
import hashlib
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_document_task(document_id):
    """Task to fetch, parse, and extract text from a document."""
    try:
        doc = Document.objects.get(id=document_id)
        doc.processing_status = "PROCESSING"
        doc.save()

        content_bytes = b""
        text_content = ""

        # 1. Fetch content
        if doc.source and doc.source.source_type in ["WEBSITE", "RSS"] and doc.original_url:
            try:
                response = requests.get(doc.original_url, timeout=30)
                response.raise_for_status() # Raise an exception for bad status codes
                content_bytes = response.content
                # TODO: Improve content type detection (e.g., check headers)
                if "text/html" in response.headers.get("Content-Type", ""):
                    soup = BeautifulSoup(content_bytes, "html.parser")
                    # Basic text extraction - improve this (e.g., use readability-lxml)
                    body = soup.find("body")
                    if body:
                        text_content = body.get_text(separator="\n", strip=True)
                    else:
                        text_content = soup.get_text(separator="\n", strip=True)
                else:
                    # Attempt generic parsing if not HTML (e.g., could be PDF linked directly)
                    text_content = parse_content_bytes(content_bytes, doc.original_url)

            except requests.RequestException as e:
                logger.error(f"Error fetching URL {doc.original_url} for doc {doc.id}: {e}")
                doc.processing_status = "FAILED"
                doc.save()
                return
        elif doc.file_path:
            try:
                with open(doc.file_path, "rb") as f:
                    content_bytes = f.read()
                text_content = parse_content_bytes(content_bytes, doc.file_path)
            except FileNotFoundError:
                logger.error(f"File not found: {doc.file_path} for doc {doc.id}")
                doc.processing_status = "FAILED"
                doc.save()
                return
            except Exception as e:
                logger.error(f"Error reading file {doc.file_path} for doc {doc.id}: {e}")
                doc.processing_status = "FAILED"
                doc.save()
                return
        else:
            logger.warning(f"Document {doc.id} has no URL or file path to process.")
            doc.processing_status = "FAILED"
            doc.save()
            return

        # 2. Calculate Hash
        if content_bytes:
            doc.content_hash = hashlib.sha256(content_bytes).hexdigest()

        # 3. Save Extracted Text
        doc.extracted_text = text_content

        # 4. Trigger Indexing (call another task or service)
        from rag_integration.services import build_indices_for_document
        # Consider making build_indices_for_document a Celery task itself for better decoupling
        # build_indices_for_document.delay(doc.id)
        try:
            build_indices_for_document(doc.id) # Call synchronously for now, or make it a task
            doc.processing_status = "PROCESSED" # Mark as fully processed after indexing
        except Exception as index_exc:
            logger.error(f"Error during indexing for document {doc.id}: {index_exc}", exc_info=True)
            doc.processing_status = "FAILED" # Mark as failed if indexing fails
        
        doc.save()
        logger.info(f"Successfully processed and attempted indexing for document {doc.id}: {doc.title}")

    except Document.DoesNotExist:
        logger.error(f"Document with id {document_id} not found.")
    except Exception as e:
        logger.error(f"Unexpected error processing document {document_id}: {e}")
        try:
            # Try to mark as failed if the object still exists
            doc = Document.objects.get(id=document_id)
            doc.processing_status = "FAILED"
            doc.save()
        except Document.DoesNotExist:
            pass # Already logged above
        except Exception as inner_e:
            logger.error(f"Failed to mark document {document_id} as FAILED: {inner_e}")

def parse_content_bytes(content_bytes, filename_or_url):
    """Attempts to parse text content from bytes based on likely file type."""
    text_content = ""
    filename_lower = filename_or_url.lower()

    try:
        if filename_lower.endswith(".pdf"):
            with PyMuPDF.open(stream=content_bytes, filetype="pdf") as pdf_doc:
                text_content = "\n".join([page.get_text() for page in pdf_doc])
        elif filename_lower.endswith(".docx"):
            import io
            doc = docx.Document(io.BytesIO(content_bytes))
            text_content = "\n".join([para.text for para in doc.paragraphs])
        elif filename_lower.endswith( (".txt", ".md", ".py", ".js", ".html", ".css") ): # Add more text types
            # Try decoding assuming UTF-8, fallback to latin-1
            try:
                text_content = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text_content = content_bytes.decode("latin-1")
        else:
            # Fallback: try decoding as text anyway
            logger.warning(f"Unknown file type for {filename_or_url}, attempting text decode.")
            try:
                text_content = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    text_content = content_bytes.decode("latin-1")
                except UnicodeDecodeError:
                    logger.error(f"Could not decode content for {filename_or_url}")
                    text_content = "" # Could not decode
    except Exception as e:
        logger.error(f"Error parsing content from {filename_or_url}: {e}")
        text_content = "" # Parsing failed

    return text_content.strip()

# TODO: Add task for chunking
# @shared_task
# def chunk_document_task(document_id):
#     pass

