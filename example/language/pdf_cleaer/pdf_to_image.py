from pdf2image import convert_from_path

pages = convert_from_path('input.pdf', dpi=150)
for i, page in enumerate(pages):
    page.save(f'output/{i}.png', 'PNG')
