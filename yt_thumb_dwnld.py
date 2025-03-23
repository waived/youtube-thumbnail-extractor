import requests, os, sys, re
from bs4 import BeautifulSoup

# setup colors
b = '\033[1m'  #bright
r = '\033[31m' #red
w = '\033[37m' #white
g = '\033[32m' #green
y = '\033[33m' #yellow

def download(link, path):
    if link.startswith("//"):
        link = "https:" + link
    
    try:
        response = requests.get(link)
        
        if not response.status_code == 200:
            print(f'{r} Unable to fetch {y}{link}')
        else:
            filename = os.path.basename(link)
            
            with open(os.path.join(path, filename), 'wb') as file:
                file.write(response.content)
                file.close()
        
        print(f'{w} Downloaded ---> {y}{link}')
    except:
        print(f'{r} Could not download {y}{link}')

def main():
    os.system('clear')
    
    print(f'''{b}{y}
 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+
 |Y|o|u|T|u|b|e| |T|h|u|m|b|n|a|i|l| |E|x|t|r|a|c|t|o|r|
 +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+    
''')
    path = ""

    try:
        print(f'{w} ID Example: https://www.youtube.com/watch?v={r}<ID_HERE>\r\n')

        vid_id = input(f'{g} Youtube Video ID:{w} ')
    
        dwnd = input(f'{g} Download extracted thumbnails? (Y/n):{w} ')
        
        if dwnd.lower().startswith('y'):
            path = input(f'{g} Download to (/tmp/folder):{w} ')
            
            if not os.path.exists(path):
                sys.exit(f'\r\n{r} Error! Folder not found...\r\n')
            
        input(f'\r\n{w} Ready? Strike ENTER to extract links...\r\n')
    except KeyboardInterrupt:
        sys.exit()
    except:
        main()
    
    try:
        video_url = f"https://www.youtube.com/watch?v={vid_id}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(video_url, headers=headers)
        
        if not response.status_code == 200:
            sys.exit(f'\r\n{r} Error! Video unavailable...\r\n')
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            
            links = set()
            
            for tag in soup.find_all(["a", "img", "link", "meta"]):
                link = tag.get("href") or tag.get("src") # Get URL from href or src
                if link and "i.ytimg.com" in link:
                    links.add(link)
            
            if not links:
                sys.exit(f'\r\n{y} Sorry! No thumbnails found...\r\n')
            else:
                for link in links:
                    if not link.endswith('generate_204'):
                        if path:
                            download(link, path)
                        else:
                            print(f'{w} Extracted ---> {y}{link}')
        
    except Exception as ex:
        sys.exit(f'\r\n{r}{ex}\r\n')
        
    sys.exit(f'{w}\r\n Complete!\r\n')
    
if __name__ == "__main__":
    main()
