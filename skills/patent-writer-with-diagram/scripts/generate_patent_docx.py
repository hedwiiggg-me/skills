#!/usr/bin/env python3

import argparse
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from xml.sax.saxutils import escape


CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


DOCUMENT_RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>
"""


APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex Patent Writer</Application>
</Properties>
"""


STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei" w:eastAsia="Microsoft YaHei"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>
"""


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def xml_text(value: str) -> str:
    return escape(value or "")


def run_xml(text: str, *, bold: bool = False, size: int = 24, color: Optional[str] = None) -> str:
    props = [
        '<w:rFonts w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei" w:eastAsia="Microsoft YaHei"/>',
        f'<w:sz w:val="{size}"/>',
        f'<w:szCs w:val="{size}"/>',
    ]
    if bold:
        props.append("<w:b/>")
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    text_xml = xml_text(text).replace("\n", "</w:t><w:br/><w:t>")
    return f"<w:r><w:rPr>{''.join(props)}</w:rPr><w:t xml:space=\"preserve\">{text_xml}</w:t></w:r>"


def paragraph_xml(
    runs: List[str],
    *,
    align: Optional[str] = None,
    spacing_before: Optional[int] = None,
    spacing_after: Optional[int] = None,
    first_line: Optional[int] = None,
) -> str:
    ppr = []
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if spacing_before is not None or spacing_after is not None:
        before = spacing_before if spacing_before is not None else 0
        after = spacing_after if spacing_after is not None else 0
        ppr.append(f'<w:spacing w:before="{before}" w:after="{after}"/>')
    if first_line is not None:
        ppr.append(f'<w:ind w:firstLine="{first_line}"/>')
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    return f"<w:p>{ppr_xml}{''.join(runs)}</w:p>"


def numbered_paragraph_xml(index: int, text: str) -> str:
    return paragraph_xml([run_xml(f"{index}. {text}")], first_line=420, spacing_after=120)


def cell_xml(text: str, width: int, *, bold: bool = False, span: Optional[int] = None) -> str:
    span_xml = f'<w:gridSpan w:val="{span}"/>' if span else ""
    return (
        "<w:tc>"
        "<w:tcPr>"
        f'<w:tcW w:w="{width}" w:type="dxa"/>'
        f"{span_xml}"
        '<w:tcBorders>'
        '<w:top w:val="single" w:sz="4" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:color="000000"/>'
        "</w:tcBorders>"
        "</w:tcPr>"
        f"{paragraph_xml([run_xml(text, bold=bold)], spacing_after=0)}"
        "</w:tc>"
    )


def contact_cell_xml(phone: str, email: str, width: int) -> str:
    line1 = paragraph_xml(
        [run_xml("联系电话", bold=True), run_xml(f"  {phone}")],
        spacing_after=0,
    )
    line2 = paragraph_xml(
        [run_xml("e-mail：", bold=True), run_xml(f"  {email}")],
        spacing_after=0,
    )
    return (
        "<w:tc>"
        "<w:tcPr>"
        f'<w:tcW w:w="{width}" w:type="dxa"/>'
        '<w:gridSpan w:val="2"/>'
        '<w:tcBorders>'
        '<w:top w:val="single" w:sz="4" w:color="000000"/>'
        '<w:left w:val="single" w:sz="4" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="000000"/>'
        '<w:right w:val="single" w:sz="4" w:color="000000"/>'
        "</w:tcBorders>"
        "</w:tcPr>"
        f"{line1}{line2}"
        "</w:tc>"
    )


def table_xml(data: dict) -> str:
    inventors = data.get("inventors", [])
    if isinstance(inventors, list):
        inventors_text = " ".join(str(item) for item in inventors if item)
    else:
        inventors_text = str(inventors)
    contact = data.get("contact", {}) or {}
    rows = [
        "<w:tr>"
        f"{cell_xml('专利名称', 1360, bold=True)}"
        f"{cell_xml(str(data.get('patent_name', '')), 8751, span=3)}"
        "</w:tr>",
        "<w:tr>"
        f"{cell_xml('专利类型', 1360, bold=True)}"
        f"{cell_xml(str(data.get('patent_type', '')), 3348)}"
        f"{cell_xml('发明人', 1752, bold=True)}"
        f"{cell_xml(inventors_text, 3651)}"
        "</w:tr>",
        "<w:tr>"
        f"{cell_xml('联系人', 1360, bold=True)}"
        f"{cell_xml(str(contact.get('name', '')), 3348)}"
        f"{contact_cell_xml(str(contact.get('phone', '')), str(contact.get('email', '')), 5403)}"
        "</w:tr>",
    ]
    return (
        "<w:tbl>"
        "<w:tblPr>"
        '<w:tblW w:w="10111" w:type="dxa"/>'
        '<w:jc w:val="center"/>'
        "</w:tblPr>"
        "<w:tblGrid>"
        '<w:gridCol w:w="1360"/>'
        '<w:gridCol w:w="3348"/>'
        '<w:gridCol w:w="1752"/>'
        '<w:gridCol w:w="3651"/>'
        "</w:tblGrid>"
        f"{''.join(rows)}"
        "</w:tbl>"
    )


def ensure_list(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def build_document_xml(data: dict) -> str:
    body = []
    body.append(paragraph_xml([run_xml("专利申请技术交底书", bold=True, size=32)], align="center", spacing_after=240))
    body.append(table_xml(data))
    body.append(paragraph_xml([run_xml("针对上次评审意见的补充材料:")], spacing_before=240, spacing_after=240))

    body.append(paragraph_xml([run_xml("1 Background: ...", color="808080", size=20)], spacing_after=60))
    body.append(paragraph_xml([run_xml("1 背景: ...", color="808080", size=20)], spacing_after=120))
    body.append(paragraph_xml([run_xml("问题的描述:", bold=True)], spacing_after=120))
    body.append(paragraph_xml([run_xml(str(data.get("background", "")))], first_line=420, spacing_after=120))
    body.append(paragraph_xml([run_xml("现存问题的缺点：", bold=True)], spacing_after=120))
    drawbacks = ensure_list(data.get("drawbacks"))
    if drawbacks:
        for idx, item in enumerate(drawbacks, start=1):
            body.append(numbered_paragraph_xml(idx, item))
    else:
        body.append(paragraph_xml([run_xml("")], spacing_after=120))

    body.append(paragraph_xml([run_xml("2,Summary of Invention: ...", color="808080", size=20)], spacing_before=180, spacing_after=60))
    body.append(paragraph_xml([run_xml("2，发明要点：...", color="808080", size=20)], spacing_after=120))
    body.append(paragraph_xml([run_xml("针对上述问题和现有解决方案的缺陷，本方案提出：", bold=True)], spacing_after=120))
    body.append(paragraph_xml([run_xml(str(data.get("summary", "")))], first_line=420, spacing_after=120))
    body.append(paragraph_xml([run_xml("采用本方案的优势：", bold=True)], spacing_after=120))
    advantages = ensure_list(data.get("advantages"))
    if advantages:
        for idx, item in enumerate(advantages, start=1):
            body.append(numbered_paragraph_xml(idx, item))
    else:
        body.append(paragraph_xml([run_xml("")], spacing_after=120))

    body.append(paragraph_xml([run_xml("3,Description: ...", color="808080", size=20)], spacing_before=180, spacing_after=60))
    body.append(paragraph_xml([run_xml("3，描述：...", color="808080", size=20)], spacing_after=120))
    for paragraph in ensure_list(data.get("description")):
        body.append(paragraph_xml([run_xml(paragraph)], first_line=420, spacing_after=120))
    if not ensure_list(data.get("description")):
        body.append(paragraph_xml([run_xml("")], spacing_after=120))

    body.append("<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>")
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W_NS}"><w:body>{"".join(body)}</w:body></w:document>'
    )


def core_xml(title: str) -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{xml_text(title)}</dc:title>
  <dc:creator>Codex Patent Writer</dc:creator>
  <cp:lastModifiedBy>Codex Patent Writer</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


def validate(data: dict) -> None:
    required = [
        ("patent_name", data.get("patent_name")),
        ("patent_type", data.get("patent_type")),
        ("background", data.get("background")),
        ("summary", data.get("summary")),
    ]
    missing = [name for name, value in required if not value]
    if missing:
        raise SystemExit(f"Missing required fields: {', '.join(missing)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a patent briefing DOCX without external dependencies.")
    parser.add_argument("--input", required=True, help="Path to the input JSON file.")
    parser.add_argument("--output", required=True, help="Path to the output .docx file.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    validate(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
        docx.writestr("_rels/.rels", RELS_XML)
        docx.writestr("word/document.xml", build_document_xml(data))
        docx.writestr("word/styles.xml", STYLES_XML)
        docx.writestr("word/_rels/document.xml.rels", DOCUMENT_RELS_XML)
        docx.writestr("docProps/app.xml", APP_XML)
        docx.writestr("docProps/core.xml", core_xml(str(data.get("patent_name", "专利申请技术交底书"))))


if __name__ == "__main__":
    main()
