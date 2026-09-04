
import json
import os
import re
import urllib.request
from qgis.core import QgsProject
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from qgis.utils import iface

# Configure sua chave de API do Google AI Studio via variável de ambiente ou substitua abaixo
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "SUA_CHAVE_AQUI")
MODEL_NAME = "gemini-2.5-flash"



class GeminiQGISDock(QDockWidget):

  def __init__(self, parent=None):
    super().__init__("Gemini QGIS Copilot", parent)
    self.setAllowedAreas(
        Qt.DockWidgetArea.LeftDockWidgetArea
        | Qt.DockWidgetArea.RightDockWidgetArea
    )

    widget = QWidget()
    layout = QVBoxLayout(widget)

    layout.addWidget(QLabel("<b>Comando em Linguagem Natural:</b>"))
    self.input_prompt = QPlainTextEdit()
    self.input_prompt.setPlaceholderText(
        "Ex: Mude a cor da camada de talhões para verde claro e aplique"
        " transparência de 50%"
    )
    self.input_prompt.setFixedHeight(80)
    layout.addWidget(self.input_prompt)

    btn_layout = QHBoxLayout()
    self.btn_run = QPushButton("⚡ Executar Ação")
    self.btn_run.clicked.connect(self.process_command)
    btn_layout.addWidget(self.btn_run)
    layout.addLayout(btn_layout)

    layout.addWidget(QLabel("<b>Log / Código Executado:</b>"))
    self.log_area = QTextEdit()
    self.log_area.setReadOnly(True)
    layout.addWidget(self.log_area)

    self.setWidget(widget)

  def get_project_context(self):
    """Extrai informações das camadas abertas no QGIS."""
    layers = QgsProject.instance().mapLayers().values()
    info = []
    for l in layers:
      tipo = "Raster"
      if hasattr(l, "geometryType"):
        geom_names = {
            0: "Pontos",
            1: "Linhas",
            2: "Polígonos",
            3: "Desconhecido/Nulo",
        }
        tipo = f"Vetor ({geom_names.get(l.geometryType(), 'Outro')})"
      info.append(f"- Camada: '{l.name()}', Tipo: {tipo}, CRS: {l.crs().authid()}")
    return "\n".join(info) if info else "Nenhuma camada carregada no projeto."

  def call_gemini_api(self, prompt, context):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"

    system_instruction = f"""Você é um especialista em automação e desenvolvimento de algoritmos no QGIS (PyQGIS 3).

Contexto atual das camadas no projeto:
{context}

DIRETRIZES DE DECISÃO:
1. SE O USUÁRIO PEDIR UM "MODELO" (Graphical Modeler / Model Designer / arquivo .model3):
   - Não execute as ferramentas diretamente de forma imperativa.
   - Crie uma subclasse de `QgsProcessingModelAlgorithm` ou construa a estrutura gráfica do modelo usando `QgsProcessingModelAlgorithm` programaticamente, salvando o arquivo `.model3` na pasta de modelos do QGIS (`QgsApplication.qgisSettingsDirPath() + 'processing/models/'`).
   - Ou crie um script de algoritmo personalizado (`QgsProcessingAlgorithm`) que encadeia as operações e registre-o no `QgsApplication.processingRegistry()`.

2. SE O USUÁRIO PEDIR UMA "AUTOMAÇÃO / EXECUÇÃO DIRETA":
   - Use o módulo `processing.run()` ou `processing.runAndLoadResults()`.
   - Certifique-se de que cada etapa encadeada use a saída anterior (`output['OUTPUT']`) como entrada da próxima.

REGRAS DE CÓDIGO:
- Retorne APENAS código Python puro executável, sem texto explicativo fora de blocos de código.
- Trate sempre importações necessárias de `qgis.core` e `processing`.
- Se modificar ou criar camadas no projeto, atualize com `iface.mapCanvas().refresh()`.

REGRAS CRÍTICAS DE PYQGIS:
1. NUNCA use `QgsApplication.processingRegistry().addAlgorithm()`, pois este método NÃO existe.
2. Para adicionar algoritmos à Caixa de Ferramentas:
   - Salve o script .py na pasta `os.path.join(QgsApplication.qgisSettingsDirPath(), 'processing', 'scripts')` e chame `QgsApplication.processingRegistry().providerById('script').refreshAlgorithms()`.
   - OU crie uma subclasse de `QgsProcessingProvider`, adicione o algoritmo nela com `self.addAlgorithm()`, e adicione o provedor com `QgsApplication.processingRegistry().addProvider(provider)`.
"""

    payload = {
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1},
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=30) as response:
      res_json = json.loads(response.read().decode("utf-8"))
      return res_json["candidates"][0]["content"]["parts"][0]["text"]

  def process_command(self):
    prompt_text = self.input_prompt.toPlainText().strip()
    if not prompt_text:
      return

    self.btn_run.setEnabled(False)
    self.log_area.append(f"\n<b>Prompt:</b> {prompt_text}")

    try:
      context = self.get_project_context()
      raw_response = self.call_gemini_api(prompt_text, context)

      # Extrai o código Python da resposta
      code_match = re.search(
          r"```(?:python)?\s*(.*?)\s*```", raw_response, re.DOTALL
      )
      code = code_match.group(1) if code_match else raw_response.strip()

      self.log_area.append(
          f"<pre style='color: #2b5c8f; background: #f0f0f0; padding: 6px;'>{code}</pre>"
      )

      # Executa no escopo do QGIS
      local_scope = {
          "iface": iface,
          "QgsProject": QgsProject,
      }
      exec(code, globals(), local_scope)

      self.log_area.append(
          "<b style='color: green;'>✓ Executado com sucesso!</b>"
      )
      self.input_prompt.clear()

    except Exception as e:
      self.log_area.append(f"<b style='color: red;'>Erro:</b> {str(e)}")

    finally:
      self.btn_run.setEnabled(True)


# Limpa instância anterior se houver
try:
  gemini_dock.close()
  iface.removeDockWidget(gemini_dock)
except:
  pass

gemini_dock = GeminiQGISDock(iface.mainWindow())
iface.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, gemini_dock)