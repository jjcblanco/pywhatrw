from requests import Request
from requests import Session
from lxml import html,etree
from datetime import date
import time
import dicttoxml
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sqlite3

class Crawler():
    
    nondirectoryhreflist=[]
    errhref=[]
    username="fruits"
    password="fruits457"
    verifyHTTPS=False
    def init(self):
        self.s= Session()
        print("Iniciada sesion HTTP.")
        s=self.s
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',}) ## Asi parecemos un user normal de toa' la vida
        #s.headers.update({'content-type': 'text/html; charset=UTF-8',})
        s.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',})
        s.headers.update({'Accept-Encoding': 'gzip, deflate',})  
        s.headers.update({'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',})
        #s.headers.update({'woocommerce_items_in_cart':'1', 'wp_woocommerce_session_7854c5a22f2b99871c650bf96b3e2709':'e4c7c5b45787f0f6ddbf05212ddbe7c4||1639163787||1639160187||Ce95c7f689290a19df2f23decb3adcccb','woocommerce_cart_hash':'ba7d99da929fe012b60c865a64d6d469',})
    def login(self):
        self.init()
        s = self.s 
        print("entro al login")
        #s.get("http://cominterba.com/indexxxx.html")
        #s.get("http://bahia.peachconsulting.com.ar/")
        #payload={"LoginForm[userName]":self.username,
        #"LoginForm[password]":self.password,
        #"ajax":"login-form"}
        #s.post("http://bahia.peachconsulting.com.ar/login", data=payload)
        #payload={"LoginForm[userName]":self.username,
        #"LoginForm[password]":self.password,
        #"yt0":"Ingresar"}
        #s.post("http://bahia.peachconsulting.com.ar/login", data=payload)
        #s.get("http://bahia.peachconsulting.com.ar/document/index")

    def downloadAndSave(self, href, directorio, nombre):
        try:
            response = self.s.get("https://bahia.peachconsulting.com.ar"+href, verify=self.verifyHTTPS, timeout=30)
            open(directorio+"/"+nombre, 'wb').write(response.content)
        except:
            with open("failed.txt", "a") as file:
                file.write(href + "\n")

    def main(self):
        s=self.s
        if os.path.exists("failed.txt"):
            with open("failed.txt") as file:
                for cnt, line in enumerate(file):
                    self.nondirectoryhreflist.append(line.replace("\n",""))
        elif os.path.exists("links.txt"):
            with open("links.txt") as file:
                for cnt, line in enumerate(file):
                    self.nondirectoryhreflist.append(line.replace("\n",""))
        else:
            print("paso por aca")
            self.crawlAsFuck(s.get("http://www.javierblanco.com.ar/"))
            with open("links.txt","a") as file:
                for href in self.nondirectoryhreflist:
                    file.write(href+"\n")

        for href in self.nondirectoryhreflist:
            time.sleep(1)
            href = href.replace("%2F","/")
            href = href.replace("%252F","/")
            href = href.replace("%2B","+")

            directorio =  "/".join(href.split("?name=/")[1].split("&ext")[0].split("/")[:-1])
            nombre= href.split("&realName=")[1]

            try:
                os.makedirs(directorio)
            except:
                pass
            try:
                self.downloadAndSave(href, directorio, nombre)
            except ConnectionError:
                time.sleep(10)
                self.login()
                self.downloadAndSave(href, directorio, nombre)
            print(href)

        
    def crawlAsFuck(self, source):
        print(source.encoding)
        #print(source.text)
        tree = html.fromstring(source.text)
        
        hrefs = tree.xpath("//body//a/@href")
        for href in hrefs:
            print(href)
        for href in hrefs:
            if href[25:34]=="categoria":
                self.nondirectoryhreflist.append(href)
                               

    def dbQuery(self, query):
        conn = sqlite3.connect('links.db')
        c = conn.cursor()
        if "SELECT" not in query.upper()[:20]:
            c.execute(query)
            conn.commit()
            return True
        else:
            return c.fetchall()
        
        conn.close()


crawler = Crawler()
crawler.init()
crawler.main()
