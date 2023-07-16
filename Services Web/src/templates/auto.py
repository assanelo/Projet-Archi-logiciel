import os
from bs4 import BeautifulSoup

def replace_local_urls_with_url_for(html_content, base_path):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Replace <link> tag for favicon with url_for version
    for link_tag in soup.find_all('link', rel='icon', href=True):
        if not link_tag['href'].startswith(('http://', 'https://')):
            relative_path = os.path.relpath(link_tag['href'], base_path).replace("\\", "/")  # Clean the path
            link_tag['href'] = "{{ url_for('static', filename='" + relative_path + "') }}"

    # Replace <img> tags for images with url_for versions
    for img_tag in soup.find_all('img', src=True):
        if not img_tag['src'].startswith(('http://', 'https://')):
            relative_path = os.path.relpath(img_tag['src'], base_path).replace("\\", "/")  # Clean the path
            img_tag['src'] = "{{ url_for('static', filename='" + relative_path + "') }}"

    # Replace <script> tags for scripts with url_for versions
    for script_tag in soup.find_all('script', src=True):
        if not script_tag['src'].startswith(('http://', 'https://')):
            relative_path = os.path.relpath(script_tag['src'], base_path).replace("\\", "/")  # Clean the path
            script_tag['src'] = "{{ url_for('static', filename='" + relative_path + "') }}"

    # Replace <source> tags for sources with url_for versions
    for source_tag in soup.find_all('source', src=True):
        if not source_tag['src'].startswith(('http://', 'https://')):
            relative_path = os.path.relpath(source_tag['src'], base_path).replace("\\", "/")  # Clean the path
            source_tag['src'] = "{{ url_for('static', filename='" + relative_path + "') }}"

    return str(soup)

def main():
    file_path = input("Entrez le chemin du fichier HTML à modifier : ")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            base_path = os.path.dirname(os.path.abspath(file_path))
            modified_html = replace_local_urls_with_url_for(html_content, base_path)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_html)

        print("Les URLs locales dans les balises <link>, <img>, <script> et <source> ont été remplacées par des URLs avec url_for tout en conservant les chemins vers les ressources.")
    
    except FileNotFoundError:
        print("Le fichier spécifié n'a pas été trouvé.")
    except Exception as e:
        print("Une erreur est survenue :", e)

if __name__ == "__main__":
    main()
