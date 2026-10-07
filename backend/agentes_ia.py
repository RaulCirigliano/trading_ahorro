import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# Cargar las variables de entorno (como tu GOOGLE_API_KEY)
load_dotenv()

# Inicializar el modelo Gemini
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", # Puedes usar gemini-1.5-pro para tareas más complejas
    verbose=True,
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ==========================================
# DEFINICIÓN DE LOS AGENTES CON IA
# ==========================================

# 1. Agente de Sentimiento (El Lector)
agente_sentimiento = Agent(
    role="Analista de Sentimiento de Mercado",
    goal="Leer noticias financieras y determinar el nivel de optimismo o pesimismo del 1 al 10.",
    backstory="Eres un psicólogo de mercados experto. Lees titulares de noticias y tweets y logras captar la euforia o el pánico de los inversores al instante.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# 2. Agente Orquestador (El Jefe Trader)
agente_orquestador = Agent(
    role="Jefe Trader y Gestor de Portafolio",
    goal="Tomar la decisión final de COMPRAR, VENDER o MANTENER basándote en el análisis de todos tus subordinados.",
    backstory="Eres el líder del fondo de inversión. Tu trabajo es escuchar los datos matemáticos puros del Agente Cuantitativo, los límites del Agente de Riesgo, y el resumen del Agente de Sentimiento para tomar una decisión informada y conservadora.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# ==========================================
# PRUEBA RÁPIDA (EJECUCIÓN)
# ==========================================
if __name__ == "__main__":
    # Creamos una tarea de prueba para el Agente Orquestador simulando que los otros agentes ya le dieron información
    tarea_decision = Task(
        description='''
        El Agente Cuantitativo reporta: RSI en 25 (Sobreventa). SMA20 acaba de cruzar SMA50 hacia arriba. Señal: COMPRAR.
        El Agente de Riesgo reporta: Capital disponible 1000 USD. Riesgo máximo aprobado: 10 USD.
        El Agente de Sentimiento reporta: Noticias pesimistas sobre regulación en EE.UU. Puntuación: 3/10.
        
        Evalúa estos tres reportes y toma una decisión. Responde en formato JSON estricto con las claves: "decision" (COMPRAR, VENDER, MANTENER) y "razonamiento".
        ''',
        expected_output='Un JSON con la decisión final y la justificación.',
        agent=agente_orquestador
    )

    crew = Crew(
        agents=[agente_orquestador],
        tasks=[tarea_decision],
        process=Process.sequential
    )

    print("Iniciando reunión del comité de trading...")
    resultado = crew.kickoff()
    print("========================================")
    print("DECISIÓN FINAL DEL JEFE TRADER:")
    print(resultado)
