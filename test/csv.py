import re
def main():
    s="1, 2, \"\"\"3\"\"\"\n 4,5, 6\n"
    print(csv(s))

def csv_simple(src):
    row_list=[]
    for line in src.split('\n'):
        row_list.append(re.split(r',\s*', line.lstrip()))
    return row_list

def csv(src):
    src_len=len(src)
    src_pos=0
    re1 = re.compile(r"[ \t]+")
    re2 = re.compile(r"\r?\n")
    re3 = re.compile(r'"([^"]|"")*"')
    re4 = re.compile(r"[^,\n]*")
    row_list=[]
    cur_row=[]
    cur_rec=""
    while src_pos<src_len:
        # r"[ \t]+"
        m = re1.match(src, src_pos)
        if m:
            src_pos=m.end()
        if src_pos<src_len and src[src_pos]==',':
            src_pos+=1
            cur_rec = cur_rec.rstrip()
            if len(cur_rec)>0 and cur_rec[0]=='"' and cur_rec[-1]=='"':
                cur_rec=re.sub('""', '"', cur_rec[1:-1])
            cur_row.append(cur_rec)
            cur_rec=""
            continue
        # r"\r?\n"
        m = re2.match(src, src_pos)
        if m:
            src_pos=m.end()
            cur_rec = cur_rec.rstrip()
            if len(cur_rec)>0 and cur_rec[0]=='"' and cur_rec[-1]=='"':
                cur_rec=re.sub('""', '"', cur_rec[1:-1])
            cur_row.append(cur_rec)
            cur_rec=""
            row_list.append(cur_row)
            cur_row=[]
            continue
        # r'"([^"]|"")*"'
        m = re3.match(src, src_pos)
        if m:
            src_pos=m.end()
            cur_rec+=m.group(0)
            continue
        # r"[^,\n]*"
        m = re4.match(src, src_pos)
        if m:
            src_pos=m.end()
            cur_rec+=m.group(0)
            continue
    if cur_rec or cur_row:
        cur_rec = cur_rec.rstrip()
        if len(cur_rec)>0 and cur_rec[0]=='"' and cur_rec[-1]=='"':
            cur_rec=re.sub('""', '"', cur_rec[1:-1])
        cur_row.append(cur_rec)
        cur_rec=""
        row_list.append(cur_row)
    return row_list

if __name__ == "__main__":
    main()
