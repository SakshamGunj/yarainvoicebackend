import asyncio
from pyppeteer import launch

async def generate_pdf(html_content):
    """Generate PDF from HTML content using Pyppeteer (Python port of Puppeteer)"""
    
    # Launch browser
    browser = await launch(
        headless=True,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
        ]
    )
    
    # Create a new page
    page = await browser.newPage()
    
    # Set HTML content
    await page.setContent(html_content, {'waitUntil': 'networkidle0'})
    
    # Generate PDF
    pdf = await page.pdf({
        'format': 'A4',
        'printBackground': True,
        'margin': {'top': '0', 'right': '5mm', 'bottom': '5mm', 'left': '5mm'}
    })
    
    # Close browser
    await browser.close()
    
    return pdf
