# 🌍 QGIS Gemini Copilot - Assistente de IA Nativo com PyQGIS

<div align="center">

![QGIS](https://img.shields.io/badge/QGIS-3.x-589632?style=for-the-badge&logo=qgis&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API%20REST-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Dependências](https://img.shields.io/badge/Dependências-Zero%20(Nativo)-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

<p align="center">
  <b>Transforme comandos em linguagem natural em rotinas PyQGIS executadas em tempo real dentro do QGIS.</b>
</p>

</div>

---

## 📖 Visão Geral

O **QGIS Gemini Copilot** é uma ferramenta de inteligência artificial nativa desenvolvida para automatizar processos dentro do **QGIS 3.x**. 

Através de um painel acoplável (*DockWidget*) integrado diretamente à interface gráfica do QGIS, o usuário digita comandos em linguagem natural (ex: *"Crie um buffer de 500m na camada de rios e pinte de azul claro"*). O assistente inspeciona as camadas ativas do projeto, envia o contexto para a **API do Google Gemini (LLM)**, gera o código PyQGIS seguro e o executa instantaneamente na sessão aberta.

### 🚀 Por que esta abordagem é inovadora?
- ⚡ **Zero dependências externas:** Usa apenas as bibliotecas padrão do Python (`urllib.request`, `json`, `re`) e o ecossistema nativo do QGIS (`qgis.core`, `qgis.PyQt`). Não é necessário instalar `pip install` nem gerenciar ambientes virtuais no Python do QGIS.
- 🗺️ **Consciência de Contexto Espacial:** Antes de consultar a IA, o script mapeia automaticamente o nome, tipo geométrico (pontos, linhas, polígonos, rasters) e SRC (Sistema de Referência de Coordenadas) das camadas carregadas no projeto.
- 🛡️ **Engenharia de Prompt Especializada:** Instruções de sistema blindadas orientam o modelo a usar APIs corretas do PyQGIS 3, evitando funções depreciadas e garantindo o encadeamento adequado do módulo `processing`.
---

## 📋 Pré-requisitos

1. **QGIS 3.x** instalado (recomendado QGIS 3.22 LTR ou superior).
2. **Chave de API do Google Gemini** (gratuita através do [Google AI Studio](https://aistudio.google.com/)).
3. Conexão ativa com a internet para requisições HTTPS à API do Google.

---

## ⚙️ Instalação e Configuração Passo a Passo

### 1️⃣ Obter a Chave da API Gemini
1. Acesse o [Google AI Studio](https://aistudio.google.com/).
2. Faça login com sua conta Google.
3. Clique em **"Get API key"** e depois em **"Create API key"**.
4. Copie a chave gerada.

### 2️⃣ Configurar a Chave no Código
Abra o arquivo [`Qgis_Gemini.py`](file:///c:/Users/Windows%2011/Desktop/QGIS_AUTOM/Qgis_Gemini.py) e localize as linhas de configuração inicial:

```python
# Configure sua chave de API do Google AI Studio
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "SUA_CHAVE_API_AQUI")
MODEL_NAME = "gemini-2.5-flash"  # ou gemini-1.5-flash / gemini-2.0-flash
```

> 🔒 **Dica de Segurança:** Evite enviar sua chave diretamente para repositórios públicos no GitHub. Você pode defini-la como variável de ambiente no seu sistema operacional (`GEMINI_API_KEY`) ou mantê-la segura em um arquivo `.env` não versionado.

---

## 🖥️ Como Executar no QGIS

1. Abra o **QGIS** com o seu projeto de trabalho ou adicione as camadas que deseja manipular.
2. Abra o **Console Python** do QGIS:
   - Menu superior: **Complementos** ➔ **Console Python** (ou atalho <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>P</kbd> no Windows).
3. No Console Python, clique no ícone do **Editor** (ícone de folha com lápis 📝) para abrir o painel de edição de scripts.
4. Clique no ícone de pasta 📂 para abrir o arquivo [`Qgis_Gemini.py`](file:///c:/Users/Windows%2011/Desktop/QGIS_AUTOM/Qgis_Gemini.py) ou cole todo o código no editor.
5. Clique no botão verde de **Executar Script** ▶️ (*Run Script*).
6. O painel **"Gemini QGIS Copilot"** aparecerá acoplado na lateral direita do QGIS!

![Interface QGIS](https://raw.githubusercontent.com/qgis/QGIS/master/images/icons/qgis_icon.svg) *(O painel pode ser redimensionado, desacoplado ou encaixado em qualquer lateral do QGIS)*.

---

## 💡 Exemplos de Prompts para Testar

### 🎨 1. Estilização e Simbologia
- *"Mude a cor da camada de polígonos ativa para azul petróleo com 40% de transparência e borda preta de 0.5mm."*
- *"Aplique uma simbologia categorizada na camada de propriedades usando a coluna 'STATUS'."*
- *"Altere a cor de todos os pontos da camada de poços para vermelho com tamanho 4."*

### ⚙️ 2. Geoprocessamento e Análise Espacial
- *"Crie uma área de influência (buffer) de 300 metros ao redor da camada de rodovias e adicione o resultado como uma camada temporária."*
- *"Faça a dissolução (dissolve) dos polígonos da camada de municípios baseando-se no campo 'ESTADO'."*
- *"Extraia apenas os vértices da camada de linhas ativa e adicione ao mapa."*

### 📊 3. Tabela de Atributos e Cálculos
- *"Crie uma nova coluna inteira chamada 'Area_ha' na camada de talhões e calcule a área em hectares de cada feição."*
- *"Selecione todas as feições onde o campo 'POPULACAO' for maior que 50000."*
- *"Conte quantas feições existem na camada ativa e imprima no log o resumo."*

### 💾 4. Exportação e Conversão de Dados
- *"Salve a camada ativa no formato GeoPackage no caminho 'C:/temp/resultado.gpkg' com o nome de camada 'analise_final'."*
- *"Reprojete a camada ativa para SIRGAS 2000 / UTM zone 23S (EPSG:31983) e adicione ao projeto."*

---

## 🧩 Estrutura do Código Explicada

| Componente | Função |
| :--- | :--- |
| **`GeminiQGISDock`** | Classe herdada de `QDockWidget` que cria a interface gráfica (caixa de texto, botão de execução e área de log com suporte a HTML). |
| **`get_project_context()`** | Varre a instância ativa do `QgsProject`, extraindo dinamicamente o nome de cada camada, sua geometria e seu CRS para enriquecer o prompt enviado ao modelo. |
| **`call_gemini_api()`** | Constrói a requisição HTTP nativa com `urllib.request`, aplicando uma *System Instruction* detalhada que força respostas em Python puro compatíveis com a API do PyQGIS 3. |
| **`process_command()`** | Trata o envio do prompt, extrai o bloco de código Python via Regex (`re.search`), exibe no painel de log e executa dinamicamente usando `exec()` no escopo do `iface` e `QgsProject`. |

---

## 🛠️ Resolução de Problemas (Troubleshooting)

### ❌ Erro `HTTP Error 404: Not Found` ou `400: Bad Request`
- **Causa:** Nome do modelo incorreto ou endpoint desatualizado.
- **Solução:** Verifique se a variável `MODEL_NAME` está definida como `"gemini-2.5-flash"`, `"gemini-2.0-flash"` ou `"gemini-1.5-flash"`.

### ❌ Erro `HTTP Error 403: Forbidden` / Chave Inválida
- **Causa:** A chave de API expirou, está digitada incorretamente ou não possui permissões no Google AI Studio.
- **Solução:** Gere uma nova chave no [Google AI Studio](https://aistudio.google.com/) e atualize a variável `GEMINI_API_KEY`.

### ❌ Buffer com tamanho incorreto ou distorcido
- **Causa:** A camada vetorial está em coordenadas geográficas (graus decimais, ex: `EPSG:4326`), e o comando pediu buffer em metros.
- **Solução:** Reprojete a camada para um sistema projetado (ex: UTM / `EPSG:31983` ou `EPSG:32723`) antes de rodar análises métricas, ou especifique no prompt para converter a projeção.

### ❌ Janela duplicada ao rodar o script várias vezes
- **Solução:** O script já conta com tratamento automático para fechar e remover instâncias anteriores antes de abrir uma nova:
  ```python
  try:
      gemini_dock.close()
      iface.removeDockWidget(gemini_dock)
  except:
      pass
  ```

---

## 🔒 Segurança e Melhores Práticas

- ⚠️ **Execução de Código Dinâmico:** A função `exec()` executa o código Python gerado diretamente na sessão do QGIS. Sempre revise o código exibido na janela de **Log / Código Executado** para garantir que as operações correspondem ao pretendido antes de aplicá-las em arquivos originais ou bases de dados de produção.
- 💾 **Trabalhe com Cópias:** Para processos destrutivos ou edições em camadas vetoriais existentes, prefira criar camadas temporárias em memória (`memory:`) ou salvar cópias de segurança.

---

## 📄 Licença

Este projeto é disponibilizado sob a licença [MIT](LICENSE). Sinta-se livre para utilizar, modificar e contribuir!
