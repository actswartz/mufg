import os
from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Cisco XRd Specialist Course', 0, 0, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def clean_text(text):
    # Remove emojis and other non-latin1 characters for basic PDF compatibility
    return text.encode('ascii', 'ignore').decode('ascii')

def markdown_to_pdf(md_file, pdf_file):
    with open(md_file, 'r') as f:
        md_content = f.read()

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    lines = md_content.split('\n')
    
    for line in lines:
        cleaned_line = clean_text(line)
        if not cleaned_line.strip() and not line.strip():
            pdf.ln(5)
            continue

        if cleaned_line.startswith('# '):
            pdf.set_font('helvetica', 'B', 20)
            pdf.multi_cell(0, 15, cleaned_line[2:])
            pdf.ln(5)
        elif cleaned_line.startswith('## '):
            pdf.set_font('helvetica', 'B', 16)
            pdf.multi_cell(0, 12, cleaned_line[3:])
            pdf.ln(2)
        elif cleaned_line.startswith('### '):
            pdf.set_font('helvetica', 'B', 14)
            pdf.multi_cell(0, 10, cleaned_line[4:])
        elif cleaned_line.startswith('#### '):
            pdf.set_font('helvetica', 'B', 12)
            pdf.multi_cell(0, 10, cleaned_line[5:])
        elif cleaned_line.startswith('|') or cleaned_line.startswith('+-'):
            pdf.set_font('courier', '', 9)
            pdf.multi_cell(0, 5, cleaned_line)
        elif cleaned_line.startswith('```'):
            pdf.set_font('courier', '', 9)
            continue 
        elif cleaned_line.startswith('> '):
            pdf.set_font('helvetica', 'I', 11)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 7, cleaned_line[2:])
            pdf.set_text_color(0, 0, 0)
        elif cleaned_line.strip() == '---':
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
            pdf.ln(2)
        elif cleaned_line.startswith('- [ ] ') or cleaned_line.startswith('- [x] '):
            pdf.set_font('helvetica', '', 11)
            pdf.multi_cell(0, 7, f" [ ] {cleaned_line[6:]}")
        elif cleaned_line.startswith('- ') or cleaned_line.startswith('* '):
            pdf.set_font('helvetica', '', 11)
            pdf.multi_cell(0, 7, f" - {cleaned_line[2:]}")
        else:
            # Basic formatting stripping
            text = cleaned_line
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            text = re.sub(r'`(.*?)`', r'\1', text)
            
            pdf.set_font('helvetica', '', 11)
            pdf.multi_cell(0, 7, text)

    pdf.output(pdf_file)
    print(f"Generated: {pdf_file}")

if __name__ == "__main__":
    files = [
        "Lab1_Foundations.md",
        "Lab2_IGP.md",
        "Lab3_BGP.md",
        "Lab4_Segment_Routing.md",
        "Lab5_NETCONF.md",
        "Lab6_Telemetry.md"
    ]
    
    if not os.path.exists("XRD"):
        os.makedirs("XRD")
        
    for f in files:
        md_path = os.path.join("XRD", f)
        pdf_path = os.path.join("XRD", f.replace(".md", ".pdf"))
        if os.path.exists(md_path):
            markdown_to_pdf(md_path, pdf_path)
        else:
            print(f"Skipping {md_path}, file not found.")
