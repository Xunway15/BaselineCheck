m=1
n=0
q=0
with open('111.html', 'r',encoding='utf-8') as fr:
    with open('hostinfo1.html', 'w',encoding='utf-8') as fw:
        fw.seek(0)
        fw.truncate()
        con = fr.readlines()
        
        for i in range(len(con)):
            print(i)
            # if con[i].find('<tr>')>=0:
            #     con[i] = '    <tr>\n    <td>{}</td>'.format(m)
            #     m+=1
            if con[i].find('check_info')>=0:
                con[i] = '    <td>{{{{ check_info.{} }}}}</td>\n'.format(n)
                n+=1
            if con[i].find('check_result')>=0:
                con[i] = '    <td>{{{{ check_result.{} }}}}</td>\n'.format(q)
                q+=1
        for i in con:
            #print(i)
            fw.write(i)
        #print(fr.read().findall('<tr>'))
        
