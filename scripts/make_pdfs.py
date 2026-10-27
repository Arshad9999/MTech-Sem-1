import json, re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether

ROOT=Path(__file__).resolve().parents[1]
COURSES=json.loads((ROOT/'assets/course-data.json').read_text())['courses']

def clean(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def rgb(hexv):
    h=hexv.lstrip('#');return colors.Color(int(h[:2],16)/255,int(h[2:4],16)/255,int(h[4:],16)/255)
def footer(canvas,doc):
    canvas.saveState(); canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#64748b'))
    canvas.drawString(18*mm,10*mm,doc.title);canvas.drawRightString(192*mm,10*mm,f"Page {doc.page}");canvas.restoreState()
def build(c):
    accent=rgb(c['accent']);out=ROOT/c['slug']/f"{c['code']}-{c['slug']}.pdf"
    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm,title=f"{c['code']} - {c['title']}",author='Arshad9999')
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='Cover',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=26,leading=29,textColor=colors.HexColor('#10213a'),spaceAfter=12))
    styles.add(ParagraphStyle(name='CourseCode',parent=styles['Normal'],fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=accent,spaceAfter=8))
    styles.add(ParagraphStyle(name='H1x',parent=styles['Heading1'],fontName='Helvetica-Bold',fontSize=19,leading=22,textColor=colors.HexColor('#10213a'),spaceBefore=8,spaceAfter=9))
    styles.add(ParagraphStyle(name='H2x',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=14,leading=17,textColor=accent,spaceBefore=7,spaceAfter=6))
    styles.add(ParagraphStyle(name='Bodyx',parent=styles['BodyText'],fontSize=10,leading=15,spaceAfter=7))
    styles.add(ParagraphStyle(name='Eq',parent=styles['Code'],fontName='Courier',fontSize=8.5,leading=12,textColor=colors.white,backColor=colors.HexColor('#101829'),borderPadding=8,spaceBefore=5,spaceAfter=9))
    styles.add(ParagraphStyle(name='Small',parent=styles['BodyText'],fontSize=8.5,leading=12,textColor=colors.HexColor('#475569')))
    credit_text=f"{c['credits']} CREDITS" if isinstance(c['credits'],int) else "CREDIT NOT STATED IN SOURCE"
    story=[Spacer(1,28*mm),Paragraph(clean(c['code'])+f" &bull; {credit_text}",styles['CourseCode']),Paragraph(clean(c['title']),styles['Cover']),Paragraph(clean(c['tagline']),ParagraphStyle(name='Lead',parent=styles['Bodyx'],fontSize=13,leading=19,textColor=colors.HexColor('#475569'))),Spacer(1,18*mm)]
    overview=[[Paragraph('<b>STUDY BLOCKS</b>',styles['Small']),Paragraph('<b>FORMAT</b>',styles['Small']),Paragraph('<b>SCOPE</b>',styles['Small'])],[Paragraph(str(len(c['modules'])),styles['H1x']),Paragraph('Definitions<br/>Equations<br/>Worked examples',styles['Bodyx']),Paragraph('Supplied syllabus only',styles['Bodyx'])]]
    t=Table(overview,colWidths=[43*mm,55*mm,55*mm]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef2ff')),('BOX',(0,0),(-1,-1),.6,colors.HexColor('#cbd5e1')),('INNERGRID',(0,0),(-1,-1),.4,colors.HexColor('#e2e8f0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));story += [t,Spacer(1,22*mm),Paragraph('<b>How to use this handbook</b>',styles['H2x']),Paragraph('For every study block: define the terms, reproduce the relation and its assumptions, solve the example without looking, and explain when the method is unsuitable.',styles['Bodyx']),Paragraph('<b>Scope note:</b> This handbook expands only topics named in the supplied syllabus. Confirm examination guidance, prescribed texts, and institutional policy with the responsible instructor.',styles['Small']),PageBreak(),Paragraph('Course map',styles['H1x'])]
    for i,m in enumerate(c['modules'],1): story.append(Paragraph(f"<b>{i}. {clean(m['title'])}</b><br/><font color='#475569'>{clean(', '.join(m['topics']))}</font>",styles['Bodyx']))
    story.append(PageBreak())
    for i,m in enumerate(c['modules'],1):
        topic_rows=[[Paragraph(clean(x),styles['Small']) for x in m['topics'][j:j+2]] for j in range(0,len(m['topics']),2)]
        if topic_rows and len(topic_rows[-1])==1: topic_rows[-1].append('')
        tt=Table(topic_rows,colWidths=[77*mm,77*mm]);tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#f8fafc')),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#dbe3ef')),('INNERGRID',(0,0),(-1,-1),.3,colors.HexColor('#e2e8f0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story += [Paragraph(f"Study block {i:02d}",styles['CourseCode']),Paragraph(clean(m['title']),styles['H1x']),tt,Spacer(1,4*mm),Paragraph('<b>Definition and idea</b>',styles['H2x']),Paragraph(clean(m['definition']),styles['Bodyx']),Paragraph(clean(m['equation']),styles['Eq']),Paragraph('<b>Worked example</b>',styles['H2x']),Paragraph(clean(m['example']),styles['Bodyx']),Table([[Paragraph('<b>MUST UNDERSTAND</b><br/>'+clean(m['checkpoint']),styles['Bodyx'])]],colWidths=[154*mm],style=TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fef9c3')),('BOX',(0,0),(-1,-1),.7,colors.HexColor('#eab308')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)])),PageBreak() if i<len(c['modules']) else Spacer(1,5*mm)]
    story += [Paragraph('Revision checklist',styles['H1x']),Paragraph('Use this final pass before an assessment or interview:',styles['Bodyx'])]
    for item in ['I can define every listed syllabus term in plain language.','I can reproduce the central equations and state their assumptions.','I can complete each worked example and create one variation.','I can compare closely related methods and justify a choice.','I can name limitations, failure modes, and ethical or operational concerns where relevant.']:
        story.append(Paragraph('&square; '+item,styles['Bodyx']))
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    return out
for c in COURSES: print(build(c))
