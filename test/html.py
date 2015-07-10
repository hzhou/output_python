import re
def main():
    s = "<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Test</h1><p>Hello World!</p></body></html>"
    page = parse_html(s)
    debug_dom(page["dom"])

def parse_html(src):
    tag_stack=[]
    cur_list=[]
    tag_stack.append({'_name':'root', '_list':cur_list})
    src_len=len(src)
    src_pos=0
    while src_pos < src_len:
        # r"<!--.*?-->"
        m = re1.match(src, src_pos)
        if m:
            src_pos=m.end()
            continue
        # r"<!DOCTYPE.*?>", re.I
        m = re2.match(src, src_pos)
        if m:
            src_pos=m.end()
            continue
        # r"[^<]+"
        m = re3.match(src, src_pos)
        if m:
            src_pos=m.end()
            cur_list.append(m.group(0))
            continue
        # r"<(\w+)(.*?)>"
        m = re4.match(src, src_pos)
        if m:
            src_pos=m.end()
            s_name=m.group(1)
            s_attr=m.group(2)
            tag = {'_name':s_name}
            parse_attribute(tag, s_attr)
            cur_list.append(tag)
            if '/' in tag or re.match(r"area|base|br|col|embed|hr|img|input|keygen|link|meta|param|source|track|wbr", s_name, re.I):
                pass
            elif re.match(r"script|style|textarea|title", s_name, re.I):
                i_start=src_pos
                while src_pos < src_len:
                    # r"([^<]|<[^/])+"
                    m = re5.match(src, src_pos)
                    if m:
                        src_pos=m.end()
                        continue
                    # r"</(\w+).*?>"
                    m = re6.match(src, src_pos)
                    if m:
                        src_pos=m.end()
                        if m.group(1)==s_name:
                            break
                        else:
                            continue
                    src_pos+=1
                i_end=src_pos
                tag['_text'] = src[i_start:i_end]
            else:
                tag_stack.append(tag)
                cur_list=[]
                tag['_list'] = cur_list
            continue
        # r"</(\w+).*?>"
        m = re6.match(src, src_pos)
        if m:
            src_pos=m.end()
            s_name=m.group(1)
            if s_name == tag_stack[-1]['_name']:
                tag_stack.pop()
                cur_list=tag_stack[-1]['_list']
            else:
                j=len(tag_stack)-2
                while j>0:
                    if s_name == tag_stack[j]['_name']:
                        while len(tag_stack)>=j:
                            tag_stack.pop()
                        cur_list=tag_stack[-1]['_list']
                        break
                    j-=1
            continue
        src_pos+=1
        continue
    return {"dom":tag_stack[0]}

def parse_attribute(tag, src):
    src_len=len(src)
    src_pos=0
    while src_pos < src_len:
        # r"\s+"
        m = re7.match(src, src_pos)
        if m:
            src_pos=m.end()
            continue
        if src_pos<src_len and src[src_pos]=='/':
            src_pos+=1
            tag['/']=1
            continue
        # r"([^\s'\"\\=<>`]+)"
        m = re8.match(src, src_pos)
        if m:
            src_pos=m.end()
            s_attr_name=m.group(1)
            # r"\s*=\s*"
            m = re9.match(src, src_pos)
            if m:
                src_pos=m.end()
                while src_pos < src_len:
                    # r"\"((?:[^\\\"]+|\\.)*)\""
                    m = re10.match(src, src_pos)
                    if m:
                        src_pos=m.end()
                        tag[s_attr_name] = m.group(1)
                        break
                    # r"'((?:[^\\\']+|\\.)*)'"
                    m = re11.match(src, src_pos)
                    if m:
                        src_pos=m.end()
                        tag[s_attr_name] = m.group(1)
                        break
                    # r"[^\s'\"=<>`]+"
                    m = re12.match(src, src_pos)
                    if m:
                        src_pos=m.end()
                        tag[s_attr_name] = m.group(0)
                        break
                    i+=1
            else:
                tag[s_attr_name]=1
            continue
        src_pos+=1
        continue

def debug_dom(node):
    def print_node(node, level):
        if isinstance(node, str):
            print("    " * level, node)
        else:
            print("    " * level, node['_name'])
            if "_list" in node:
                for t in node['_list']:
                    print_node(t, level+1)
    print_node(node, 0)

re1 = re.compile(r"<!--.*?-->")
re2 = re.compile(r"<!DOCTYPE.*?>", re.I)
re3 = re.compile(r"[^<]+")
re4 = re.compile(r"<(\w+)(.*?)>")
re5 = re.compile(r"([^<]|<[^/])+")
re6 = re.compile(r"</(\w+).*?>")
re7 = re.compile(r"\s+")
re8 = re.compile(r"([^\s'\"\\=<>`]+)")
re9 = re.compile(r"\s*=\s*")
re10 = re.compile(r"\"((?:[^\\\"]+|\\.)*)\"")
re11 = re.compile(r"'((?:[^\\\']+|\\.)*)'")
re12 = re.compile(r"[^\s'\"=<>`]+")
if __name__ == "__main__":
    main()
