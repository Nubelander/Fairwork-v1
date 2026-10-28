"""
Rebuild the FAIRWORK SLR page data from the master codebook spreadsheet.

  pip install pandas openpyxl
  python3 build_slr.py Master_Codebook.xlsx slr.html [YYYY-MM-DD]

Keeps papers marked Include (any capitalisation), de-duplicates double-coded papers
by WOS ID (preferring completed, non-IRR rows), fixes known codebook typos, drops
coder names, and writes the cleaned data into slr.html's embedded <script id="slr-data">.
"""
import pandas as pd, json, re, collections
import sys
XLSX = sys.argv[1] if len(sys.argv)>1 else 'codebook.xlsx'
PAGE = sys.argv[2] if len(sys.argv)>2 else 'slr.html'
SNAP = sys.argv[3] if len(sys.argv)>3 else None
df = pd.read_excel(XLSX, dtype=str)
df.columns = [c.strip() for c in df.columns]

def split(v):
    """Split a multi-select cell on commas, ignoring commas inside quotes or parentheses."""
    if pd.isna(v) or not str(v).strip(): return []
    out, cur, depth, q = [], '', 0, False
    for ch in str(v):
        if ch == '"': q = not q; continue
        if not q and ch == '(': depth += 1
        if not q and ch == ')': depth = max(0, depth-1)
        if ch == ',' and not q and depth == 0:
            out.append(cur); cur = ''
        else: cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]

FIX = {'Pesimistic':'Pessimistic','Bossting':'Boosting','Pyschological':'Psychological','Accomodation':'Accommodation',
       'Interview of Focus Group':'Interview or Focus Group'}
def fix(s):
    for a,b in FIX.items(): s = s.replace(a,b)
    return s

COLS = {  # key: (source column, multi?)
 'concept':('Technological Concept Studied (P)',True),'aiTypes':('Types of AI Discussed (M)',True),
 'focus':('Focus of Analysis (P)',True),'geo':('Geographic Coverage (P)',True),'sector':('Industry Sector(s) (P)',True),
 'time':('Time Perspective',True),'approach':('Empirical Approach (P)',True),'methods':('Methods Used (M)',True),
 'attitude':('Attitudes Toward AI & Tech (P)',True),'subcomp':('Substitution vs. Complementarity (P)',True),
 'frames':('Frames Invoked in Study (M)',True),'ethics':('Ethical & Societal Considerations (M)',True),
 'scope':('Scope of Impacts Emphasized (P)',True),'tasks':('Task Allocation & Skills (M)',True),
 'jobQty':('Job Quantity Effects (M)',True),'jqMaterial':('Material Job Quality (M)',True),
 'jqIntangible':('Intangible Job Quality (M)',True),'environment':('Working Environment & Conditions (M)',True),
 'team':('Team Structure (M)',True),'interaction':('Interaction & Relationships (M)',True),
 'workforce':('Workforce-Level Dynamics (M)',True),'subgroup':('Subgroup Analysis (P)',True),
 'design':('Technology Design Choices (M)',True),'protections':('Worker Protections & Work Environment (M)',True),
 'education':('Education & Retraining (M)',True),'safetyNets':('Social Safety Nets (M)',True),
 'laborPolicy':('Labor Market and Economic Policy (M)',True),
}
df['_inc'] = df['Inclusion Review'].fillna('').str.strip().str.lower()
screened = df['WOS ID'].nunique()
reviewed = df[df['_inc']!=''].drop_duplicates('WOS ID')
inc = df[df['_inc']=='include'].copy()
inc['_done'] = inc['Coding Completion Status'].fillna('').eq('Completed')
inc['_irr'] = inc['is_IRR'].fillna('').eq('Yes')
inc = inc.sort_values(['WOS ID','_done','_irr'], ascending=[True,False,True]).drop_duplicates('WOS ID')
coded = inc[inc['Attitudes Toward AI & Tech (P)'].notna()]

def short_auth(a):
    if pd.isna(a): return ''
    ps = [p.strip() for p in a.split(';') if p.strip()]
    first = ps[0].split(',')[0].strip().title() if ps else ''
    return first + (' et al.' if len(ps)>2 else (' & '+ps[1].split(',')[0].strip().title() if len(ps)==2 else ''))
def clip(s,n=420):
    if pd.isna(s): return ''
    s = re.sub(r'\s+',' ',str(s)).strip().strip('"').strip()
    return s if len(s)<=n else s[:n].rsplit(' ',1)[0]+'…'

recs=[]
for _,r in coded.iterrows():
    d = {'id':r['WOS ID'],'title':re.sub(r'\s+',' ',str(r['Title'])).strip(),'authors':short_auth(r['Authors']),
         'journal':str(r['Journal/Source']).title() if pd.notna(r['Journal/Source']) else '',
         'year':int(float(r['Year'])) if pd.notna(r['Year']) else None,
         'doi':str(r['DOI or Persistent Identifier']).strip() if pd.notna(r['DOI or Persistent Identifier']) else '',
         'type':r['Type of Paper'] if pd.notna(r['Type of Paper']) else '',
         'countries':clip(r['Specific Countries or Regions'],120),'objective':clip(r['Overall Objectives'])}
    for k,(c,m) in COLS.items():
        vals=[fix(x) for x in split(r[c])]
        d[k]=vals
    recs.append(d)

# IRR: agreement on primary (P) single-choice vars among double-coded papers
irr = df[df['is_IRR'].fillna('').eq('Yes') & df['Attitudes Toward AI & Tech (P)'].notna()]
pairs = [g for _,g in irr.groupby('WOS ID') if len(g)>=2]
def kappa(col):
    a=[];b=[]
    for g in pairs:
        x=g.iloc[0][col]; y=g.iloc[1][col]
        if pd.isna(x) or pd.isna(y): continue
        a.append(fix(x).strip()); b.append(fix(y).strip())
    n=len(a); po=sum(i==j for i,j in zip(a,b))/n
    ca,cb=collections.Counter(a),collections.Counter(b)
    pe=sum(ca[k]*cb[k] for k in set(a)|set(b))/n/n
    return n, po, (po-pe)/(1-pe) if pe<1 else 1
irrstats={c:kappa(c) for c in ['Attitudes Toward AI & Tech (P)','Substitution vs. Complementarity (P)','Empirical Approach (P)','Scope of Impacts Emphasized (P)']}

meta={'screened':int(screened),'reviewed':int(len(reviewed)),'included':int(len(inc)),'coded':len(recs),
      'irrPapers':len(pairs),'variables':len(COLS)+8,
      'irr':{k:{'n':v[0],'agree':round(v[1],3),'kappa':round(v[2],3)} for k,v in irrstats.items()},
      'built':SNAP or __import__('datetime').date.today().isoformat()}

# ── Compact encoding for the page: categorical values → indices into a per-field dictionary ──
dicts = {k: sorted({x for r in recs for x in r[k]}) for k in COLS}
rows = []
for r in recs:
    rows.append([r['id'], r['title'], r['authors'], r['journal'], r['year'], r['doi'], r['type'], r['countries'], clip(r['objective'],320)]
                + [[dicts[k].index(x) for x in r[k]] for k in COLS])
packed = {'meta':meta, 'keys':list(COLS), 'dicts':dicts, 'rows':rows}
s = json.dumps(packed, ensure_ascii=False, separators=(',',':')).replace('</','<\\/')
html = open(PAGE, encoding='utf-8').read()
html = re.sub(r'(<script type="application/json" id="slr-data">).*?(</script>)', lambda m: m.group(1)+s+m.group(2), html, count=1, flags=re.S)
open(PAGE, 'w', encoding='utf-8').write(html)
print(f"Updated {PAGE}: {meta['coded']} coded papers, {meta['screened']} records, snapshot {meta['built']}")
