from flask import Flask, render_template, request, send_file,redirect
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib.units import inch
import io  # For in-memory PDF

app = Flask(__name__)

def extract_content(url, headers):
    """Extracts content from a given URL."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        # Extract full text content
        text_content = "\n".join(p.get_text(strip=True) for p in soup.find_all("p"))
        title = soup.title.string if soup.title else "No Title"

        return {
            "url": url,
            "title": title,
            "text": text_content
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def process_links_pdf(base_url, headers=None):
    """Extracts links from a base URL, processes them, and returns PDF as bytes."""

    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    try:
        base_response = requests.get(base_url, headers=headers)
        base_response.raise_for_status()
        base_soup = BeautifulSoup(base_response.content, "lxml")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching base URL: {e}")
        return None

    links = [urljoin(base_url, a.get("href")) for a in base_soup.find_all("a", href=True)]
    links = list(set(links))  # Remove duplicates

    pdf_buffer = io.BytesIO()  # In-memory buffer for PDF
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    for i, link in enumerate(links):
        print(f"Processing link {i+1} of {len(links)}: {link}")

        content = extract_content(link, headers)
        if content:
            story.append(Paragraph(f"<b>URL:</b> {content['url']}<br/>", styles['Normal']))
            story.append(Paragraph(f"<b>Title:</b> {content['title']}<br/>", styles['Normal']))
            story.append(Paragraph(f"<b>Content:</b><br/><br/>{content['text']}<br/><br/>", styles['Normal']))
            story.append(Paragraph("<br/><br/>", styles['Normal']))
            print(f"Content from {link} added to PDF.")
        else:
            print(f"Could not extract content from {link}")

    doc.build(story)
    pdf_buffer.seek(0)  # Go to the beginning of the buffer
    return pdf_buffer


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/lo')
def lo():
    return redirect("http://127.0.0.1:8000/")


@app.route('/scrape', methods=['GET', 'POST'])
def scrape_page():
    pdf_output = None
    if request.method == 'POST':
        url_to_scrape = request.form['url']
        if url_to_scrape:
            pdf_output = process_links_pdf(url_to_scrape)
            if pdf_output:
                return send_file(
                    pdf_output,
                    mimetype='application/pdf',
                    download_name='scraped_content.pdf',
                    as_attachment=True
                )
            else:
                error_message = "Error during scraping. Please check the URL and try again."
                return render_template('scrape.html', error=error_message)
        else:
            error_message = "Please enter a URL to scrape."
            return render_template('scrape.html', error=error_message)

    if request.args.get('redirect_chatbot'): # Check for a redirect parameter
        return redirect("http://127.0.0.1:8000/") # Redirect here

    return render_template('scrape.html', error=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001) # running on port 5001 to avoid conflict with 8000