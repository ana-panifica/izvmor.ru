import os
import urllib.request
import re
import html
import shutil
def function1 ():
    os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\')
    os.mkdir('plain')
    os.mkdir('plain-clean')
    os.mkdir('mystem-plain')
    os.mkdir('mystem-xml')
    a = ''
    b = ''
    #i = 2496994 #30 сентября
    #i = 2496437 #9 сентября
    i = 2494219 #30 июня
    #i = 2494746
    #i = 2495106 #29 июля
    #i = 2495383 #8 августа
    year = '2016'
    os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain-clean\\')
    os.mkdir(year)
    
    os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain\\')
    os.mkdir(year)

            
    month_num = str(6)
    os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain\\%s'%year + '\\')
    os.mkdir(month_num)
    
    os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain-clean\\%s'%year + '\\')
    os.mkdir(month_num)
                
    month = 'июня'

    f = open ('C:\\Users\\Настя\\Desktop\\Газета\\metadata.csv', 'w', encoding = 'utf-8')
    f.write ('path'+ '\t' + 'author'+ '\t' + 'sex'+ '\t' + 'birthday'+ '\t' + 'header'+ '\t' + 'created'+ '\t' + 'sphere'+ '\t' + 'genre_fi'+ '\t' + 'type'+ '\t' + 'topic'+ '\t' + 'chronotop'+ '\t' + 'style'+ '\t' + 'audience_age'+ '\t' + 'audience_level'+ '\t' + 'audience_size'+ '\t' + 'source	publication'+ '\t' + 'publisher'+ '\t' + 'publ_year'+ '\t' + 'medium'+ '\t' + 'country'+ '\t' + 'region	language')
    f.close ()
    
    #while i <= 2494225:
    while i <= 2497390: #13 октября
    #while i <= 2496437: #9 сентября
    #while i <=  2495383: #8 августа
    #while i <=  2495603: #15 августа
        i += 1
        if i == 2494253 or i == 2494521 or i == 2494601 or i == 2494819 or i == 2495058 or i == 2495460 or i == 2495541 or i == 2495605 or i == 2495606 or i == 2496427 or i == 2497020 or i == 2497021 or i == 2497193:
            i += 1 #это страницы с перепутанной датой и они ломают программу, поэтому их пропускаем
        if i == 2494396:
            i += 4
        req = urllib.request.Request('http://izvmor.ru/news/view/%s'%i)
        with urllib.request.urlopen(req) as response:
           htmlnew = response.read().decode('utf-8')
           regexp = '<div class="news-params"><span>.+? (.*?) (.*?) .*?</span>' #ищем год и месяц
           res = re.search (regexp, htmlnew)

           if res:
                a = res.group(1)
                b = res.group(2)
           else:
               print ('не нашёл дату')
               continue
               
           if b != year:
               year = b
               os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain-clean\\')
               os.mkdir(b)
               os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain\\')
               os.mkdir(b)
            
           if a != month:
                print ('новый месяц')
                month = a
                month_num = int (month_num)
                month_num += 1
                month_num = str (month_num)
                os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain-clean\\%s'%year + '\\')
                os.mkdir(month_num)
                os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain\\%s'%year + '\\')
                os.mkdir(month_num)
                        
           
           regexp1 = '<div class="news-content">([\s\S]+?)</div>'
           text = re.search (regexp1, htmlnew)
           article = ''
           if text:
               print ('ok')
               article = text.group (1)

           
           t = article  # тут какой-то html
           regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)  # это рег. выражение находит все тэги
           regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL) # все скрипты
           regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)  # все комментарии
           regLink = re.compile('При полном или частичном использовании текстов индексируемая гиперссылка на сайт http://izvmor.ru/ обязательна.', flags=re.U | re.DOTALL)  # последняя строчка

# а дальше заменяем ненужные куски на пустую строку
           clean_t = regScript.sub("", t)
           clean_t = regComment.sub("", clean_t)
           clean_t = regTag.sub("", clean_t)
           clean_t = regLink.sub("", clean_t)

           clean_t = html.unescape(clean_t)
           
#теперь ищем мета информацию
           regexp = '<div class="news-params"><span>(.+?) .*? .*? .*?</span>' #ищем день
           res = re.search (regexp, htmlnew)
           den = ''

    
           if res:
                den = res.group(1)
           else:
               print ('не нашёл день')

           if int(den) <= 9:
               den = den.strip()
               den = '0' + den
           if int(month_num) <= 9:
               #den = den.strip()
               month_num_o = '0' + month_num           
           else:
               month_num_o = month_num
           day = '@da ' + den + '.' + str (month_num_o) + '.' + b
           dayforcsv = den + '.' + str (month_num_o) + '.' + b
           #print (day)

           regexp = '<head>[\s\S]+?<title>(.*?)</title> ' #ищем название
           res = re.search (regexp, htmlnew)
           title = ''
           if res:
                title = res.group(1)
           full_title = '@ti ' + title


           regexp = '<br /><strong>(.+?)</strong><br />\n<br /><b>При' #ищем год и месяц
           res = re.search (regexp, htmlnew)

           if res:
               au = res.group(1)
               au = au.title()
               print (au)
           else:
               au = 'Noname'
               print (au)

           full_author = '@au ' + au

           regexp = '<a href="/">Главная страница</a>[\s\S]+?<span>/</span>[\s\S]+?<a href=".*?">(.*?)</a>[\s\S]+?<span>/</span>' #ищем рубрику
           res = re.search (regexp, htmlnew)
           topic = ''
           if res:
                topic = res.group(1)
           full_topic = '@topic ' + topic

           full_url = '@url ' + 'http://izvmor.ru/news/view/%s'%i
           url = 'http://izvmor.ru/news/view/%s'%i


           os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain\\%s'%year + '\\%s'%month_num + '\\')
           full_text = full_author + '\n' + full_title + '\n' + day + '\n' + full_topic + '\n' + full_url + clean_t
           path = 'C:\\Users\\Настя\\Desktop\\Газета\\plain\\' + '%s'%year + '\\%s'%month_num + '\\article%s.txt'%i
           f = open (path, 'w', encoding = 'utf-8')
           f.write (full_text)
           f.close ()

           os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\plain-clean\\%s'%year + '\\%s'%month_num + '\\')
           full_text_clean = clean_t
           path = 'C:\\Users\\Настя\\Desktop\\Газета\\plain-clean\\' + '%s'%year + '\\%s'%month_num + '\\article%s.txt'%i
           f = open (path, 'w', encoding = 'utf-8')
           f.write (full_text_clean)
           f.close ()


           f = open ('C:\\Users\\Настя\\Desktop\\Газета\\metadata.csv', 'a', encoding = 'utf-8')
           f.write ('\n' + path + '\t' + au + '\t' + '' + '\t' + '' + '\t' + title + '\t' + dayforcsv + '\t' + 'публицистика' + '\t' + '' + '\t' + '' + '\t' + topic + '\t' + '' + '\t' + 'нейтральный' + '\t' + 'н-возраст' + '\t' + 'н-уровень' + '\t' + 'районная' + '\t' + url + '\t' + 'Известия Мордовии' + '\t' + '' + '\t' + year + '\t' + 'газета' + '\t' + 'Россия' + '\t'	+ 'Мордовия' + '\t' + 'ru')
           f.close ()


def function2 ():


    os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\mystem-plain\\')
    os.mkdir('2016')
    year = '2016'
    
    month_num = 6 #первый месяц
    
    while month_num <= 10: #последний месяц
        month_num = str (month_num)
        os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\mystem-plain\\%s'%year + '\\')
        os.mkdir(month_num)
                
        os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\')
        inp = "plain-clean\\2016\\%s"%month_num
        lst = os.listdir(inp)
        for fl in lst:
        
            os.system("C:\\Users\\Настя\\Desktop\\mystem.exe " + inp + os.sep + fl + " mystem-plain\\2016\\%s"%month_num + os.sep + fl + ' -cnid')

        month_num = int(month_num)
        month_num += 1
##        f = open('C:\\Users\\Настя\\Desktop\\Газета\\mystem-plain\\2016\\6' + os.sep + fl, encoding = 'utf-8').readlines()
##        for i in [0,0,1,2,3]:
##            f.pop(i)
##        with open('C:\\Users\\Настя\\Desktop\\Газета\\mystem-plain\\2016\\6' + os.sep + fl,'w',encoding = 'utf-8' ) as F:
##            F.writelines(f)

def function3 ():

    os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\mystem-xml\\')
    os.mkdir('2016')
    year = '2016'

    month_num = 6 #первый месяц
    
    while month_num <= 10: #последний месяц

        month_num = str (month_num)

        os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\mystem-xml\\%s'%year + '\\')
        os.mkdir(month_num)
                
        os.chdir('C:\\Users\\Настя\\Desktop\\Газета\\')
        inp = "plain-clean\\2016\\%s"%month_num
        lst = os.listdir(inp)
        for fl in lst:
            os.system("C:\\Users\\Настя\\Desktop\\mystem.exe " + inp + os.sep + fl + " mystem-xml\\2016\\%s"%month_num + os.sep + fl + ".xml -cnid --format xml --eng-gr")

        month_num = int(month_num)
        month_num += 1
        
    #он делает названия файлам .txt, но на самом деле они xml (.txt.xml)
    #path = os.path.join(os.path.abspath(os.path.dirname()), 'TestDir')
    shutil.rmtree('C:\\Users\\Настя\\Desktop\\Газета\\plain-clean\\')

def main ():
    f1 = function1 ()
    f2 = function2 ()
    f3 = function3 ()
    
if __name__ == '__main__':
    main ()
