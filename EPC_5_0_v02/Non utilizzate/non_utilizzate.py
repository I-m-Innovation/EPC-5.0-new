
class GeneratePDFView(View):
    def get(self, request, student_id, *args, **kwargs):
        try:
            # Fetch the Offerta based on the provided student_id
            offerta = Offerta.objects.get(pk=student_id)

            # Create a context dictionary with data specific to this student
            context = {
                'student_data': offerta,
            }

            # Specify the path to the wkhtmltopdf executable
            config = pdfkit.configuration(wkhtmltopdf=url)

            # Render the HTML template to a string
            template = get_template('EPC_5_0_v02/offerta_v01.html')
            html = template(context)

            # Define the options for PDF generation
            options = {
                'page-size': 'A4',
                'margin-top': '10mm',
                'margin-right': '10mm',
                'margin-bottom': '10mm',
                'margin-left': '10mm',
                'orientation': 'Landscape',
                'enable-local-file-access': "",
                'enable-smart-shrinking': '',
            }

            # Construct the filename based on student data
            filename = f"{offerta.nome_cliente}-data.pdf"

            # Generate the PDF using pdfkit and save it to a temporary file
            pdf_file_path = 'prova.pdf' # tempfile.mktemp(suffix='.pdf')
            css_file = 'EPC_5_0_v02/static/EPC_5_0_v02/styles_v0.css'
            pdfkit.from_string(html, 'prova.pdf', configuration=config, options=options, css=css_file)

            # Prepare the response to serve the PDF for download
            with open(pdf_file_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'

            # Remove the temporary PDF file
            os.remove(pdf_file_path)

            return response
        except Offerta.DoesNotExist:
            # Handle the case where the student does not exist
            print("Offerta non trovata")
            return redirect(reverse('offerta'))

