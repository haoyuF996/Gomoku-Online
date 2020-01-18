text = input('sth')
text_l = list(text)
o,y,out = '',False,[]
for i in text:
    if i=='>':
        y = True
    elif i =='<':
        out.append(o)
        y,o = False,''
    if y and i != '>':
        o+=i
print(out)
#<b><ahuhuiziu>方颢羽<spanneu/ijie>kkk<><>