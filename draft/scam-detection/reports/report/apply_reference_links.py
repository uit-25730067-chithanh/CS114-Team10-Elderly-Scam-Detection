"""
Apply clickable hyperlinks to references in report.docx
Maintains all formatting, indents, styles, and TOC.
"""
import shutil
import re
import os
import docx
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

REPORT_PATH = "draft/scam-detection/reports/report/report.docx"
BACKUP_PATH = "draft/scam-detection/reports/report/report_backup_before_links.docx"

def main():
    if not os.path.exists(REPORT_PATH):
        print(f"Error: {REPORT_PATH} not found!")
        return

    # Backup first
    shutil.copy2(REPORT_PATH, BACKUP_PATH)
    print(f"Backed up to {BACKUP_PATH}")

    doc = docx.Document(REPORT_PATH)
    print(f"Total paragraphs in document: {len(doc.paragraphs)}")

    url_regex = re.compile(r'(https?://[^\s]+)')
    doi_regex = re.compile(r'doi:\s*([^\s]+)')

    modified_count = 0

    for i in range(233, 253):
        if i >= len(doc.paragraphs):
            break
        p = doc.paragraphs[i]
        text = p.text
        url_m = url_regex.search(text)
        doi_m = doi_regex.search(text)

        if url_m or doi_m:
            if url_m:
                raw_url = url_m.group(1).rstrip('.')
                target = raw_url
                start, end = url_m.span(1)
                if url_m.group(1).endswith('.'):
                    end -= 1
            else:
                raw_doi = doi_m.group(1).rstrip('.')
                target = f"https://doi.org/{raw_doi}"
                start = doi_m.start(1)
                end = start + len(raw_doi)

            before = text[:start]
            link_str = text[start:end]
            after = text[end:]

            assert before + link_str + after == text, f"Mismatch in P#{i}"

            # Create external relationship for hyperlink
            r_id = p.part.relate_to(target, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

            # Preserve pPr (hanging indent, line spacing, etc.)
            pPr = p._p.pPr

            # Remove existing run children
            for child in list(p._p):
                if child != pPr:
                    p._p.remove(child)

            # 1. Before run
            if before:
                before_escaped = before.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                r_before = parse_xml(
                    f'<w:r {nsdecls("w")}>'
                    f'<w:rPr>'
                    f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
                    f'<w:color w:val="1E293B"/>'
                    f'</w:rPr>'
                    f'<w:t xml:space="preserve">{before_escaped}</w:t>'
                    f'</w:r>'
                )
                p._p.append(r_before)

            # 2. Hyperlink element
            link_escaped = link_str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            h_xml = (
                f'<w:hyperlink {nsdecls("w", "r")} r:id="{r_id}" w:history="1">'
                f'<w:r>'
                f'<w:rPr>'
                f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
                f'<w:color w:val="0563C1"/>'
                f'<w:u w:val="single"/>'
                f'</w:rPr>'
                f'<w:t xml:space="preserve">{link_escaped}</w:t>'
                f'</w:r>'
                f'</w:hyperlink>'
            )
            h_elem = parse_xml(h_xml)
            p._p.append(h_elem)

            # 3. After run
            if after:
                after_escaped = after.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                r_after = parse_xml(
                    f'<w:r {nsdecls("w")}>'
                    f'<w:rPr>'
                    f'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
                    f'<w:color w:val="1E293B"/>'
                    f'</w:rPr>'
                    f'<w:t xml:space="preserve">{after_escaped}</w:t>'
                    f'</w:r>'
                )
                p._p.append(r_after)

            modified_count += 1
            print(f"Applied link [{modified_count}]: P#{i} -> {target}")

    doc.save(REPORT_PATH)
    print(f"Saved {REPORT_PATH} successfully! Total links applied: {modified_count}")

    # Validate
    doc_check = docx.Document(REPORT_PATH)
    print(f"Validation: loaded document with {len(doc_check.paragraphs)} paragraphs.")
    print("Sample checks:")
    print(f"P#233: {doc_check.paragraphs[233].text}")
    print(f"P#238: {doc_check.paragraphs[238].text}")
    print(f"P#252: {doc_check.paragraphs[252].text}")

if __name__ == "__main__":
    main()
