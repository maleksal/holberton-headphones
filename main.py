from bs4 import BeautifulSoup
import sys
import codecs
import re
import hashlib



class Obfuscate:
    """ Obfuscate html/css """

    def __init__(self, html_file, css_file, overwrite=False):
        self.html_file = html_file
        self.css_file = css_file
        self.overwrite = overwrite
        self.obf_dic = self.obfuscate_class_names()

        print(self.obf_dic)

    @staticmethod
    def hash_string(string):
        result = hashlib.md5(string.encode())
        result = result.hexdigest()
        result = list(result)
        result[0] = 'f'
        return "".join(result)

    def extract_html_class_names(self):
        ignore = [
        'social',
        'trademark',
        'container',
        "footer",
        "footer-logo",
        'social-item',
        'social-link',
        'email',
        'name',
        'message',
        "form-field name",
        'form-field message',
        "form-field email",
        'form-field-container',
        'form-submit',
        'form-contact',
        'social-item facebook-icon',
        'facebook-icon',
        'form-field',
        'instagram-icon',
        'social nav'
        'social',
        'social-item instagram-icon',
        'twitter-icon',
        'social-item twitter-icon',
        'holberton_school-icon-ic_sound', 'icon',
        'holberton_school-icon-ic_video',
        'holberton_school-icon-ic_music',
        'holberton_school-icon-ic_hearing',
        'holberton_school-icon-ic_facebook',
        'holberton_school-icon-ic_twitter',
        'holberton_school-icon-ic_instagram',
        'do', 'do-1', 'do-2', 'do-3', 'do-4']

        class_list = set()

        with open(self.html_file, 'r') as fp:
            soup = BeautifulSoup(fp , 'html.parser')
            tags = {tag.name for tag in soup.find_all()}
        for tag in tags:
            for i in soup.find_all( tag ):
                if i.has_attr( "class" ):
                    if len( i['class'] ) != 0:
                        for e in i['class']:
                            if e not in ignore:
                                class_list.add(" ".join([e]))
        return class_list

    def obfuscate_class_names(self):
        d = {}

        for name in self.extract_html_class_names():
            d[name] = self.hash_string(name)
        return {key: d[key] for key in sorted(d, key=len, reverse=True)}

    def obfucate_html_file(self):
        with open(self.html_file, 'r') as fpin:
            inp = fpin.read()
            for orgin, obf in self.obf_dic.items():
                orgin, obf = f'class=\"{orgin}\"', f'class=\"{obf}\"'
                inp = inp.replace(orgin, obf)
        return inp

    def obfuscate_css_file(self):
        with open(self.css_file, 'r') as fpin:
            inp = fpin.read()
            for orgin, obf in self.obf_dic.items():
                orgin, obf = f".{orgin}", f".{obf}"
                inp = inp.replace(orgin, obf)
        return inp
    
    def main(self):
        mode = ["w", "w+"]
        md = mode[0]

        css = self.css_file
        html = self.html_file

        if not self.overwrite:
            css = "copy_of_" + self.css_file
            html = "copy_of_" + self.html_file
            md = mode[1]

        new_html = self.obfucate_html_file()
        new_css = self.obfuscate_css_file()

        with open(html, md) as fp:
            fp.write(new_html)

        with open(css, md) as fp:
            fp.write(new_css)


if __name__== "__main__":
    if len(sys.argv) > 2:
        print(sys.argv)
        obfuscator = Obfuscate(
            html_file=sys.argv[1],
            css_file=sys.argv[2],
            overwrite=True
        )
        obfuscator.main()
    else:
        exit(1)