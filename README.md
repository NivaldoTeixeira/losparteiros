# Monitoramento de partos

### Para execucao:

* O arquivo de dados "SINASC13_GEO.dbf" deve estar localizado na pasta "data".
* Com base no arquivo disponibilizado pelo governo, o script "preprocessing.py" gera, na pasta "data", o arquivo de entrada do sistema (python preprocessing.py)
* Dois arquivos sao gerados: invalidFacilities, com estabelecimentos com poucos partos para a analise, e validFacilities, com estabelecimentos validos. Esses arquivos devem ser alimentados a pagina web para a geracao dos insights.

### Notebooks
A pasta "Notebooks" contem a implementacao do modelo utilizado no pre-processamento, bem como uma analise exploratoria inicial dos dados.

### Front-end
Consiste dos arquivos index.html, na raiz, e das pastas "js" e "CSS".

### Fontes academicas
Souza, J. P., et al. "A global reference for caesarean section rates (C‐Model): a multicountry cross‐sectional study." BJOG: An International Journal of Obstetrics & Gynaecology 123.3 (2016): 427-436.

Vengoechea, Pedro José Cabeza, et al. "Clasificación de cesáreas por Grupos de Robson en dos periodos comparativos en el Hospital de Manacor." Progresos de Obstetricia y Ginecología 53.10 (2010): 385-390.
