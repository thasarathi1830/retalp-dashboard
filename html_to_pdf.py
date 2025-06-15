import pdfkit

# Full path to wkhtmltopdf.exe
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

# Configure pdfkit to use the full path
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# Input and output file paths (you can change these)
input_html = r"C:\Users\thasa\input.html"     # Path to your HTML file
output_pdf = r"C:\Users\thasa\output.pdf"     # Path where you want the PDF

# Convert HTML to PDF
pdfkit.from_file(input_html, output_pdf, configuration=config)

print(f"PDF generated at: {output_pdf}")
