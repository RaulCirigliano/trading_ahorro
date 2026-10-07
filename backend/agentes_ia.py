import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# Cargar las variables de entorno (como tu GOOGLE_API_KEY)
load_dotenv()

# Inicializar el modelo Gemini
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ==========================================
# DEFINICIÓN DE LOS AGENTES CON IA (MODO AHORRO)
# ==========================================

# 1. Agente Macro-Económico (Analista Global)
agente_macroeconomico = Agent(
    role="Analista Macro-Económico Global",
    goal="Leer noticias sobre tasas de interés, inflación y tendencias mundiales para detectar ciclos largos.",
    backstory="Eres un veterano de Wall Street enfocado en economía global. No te importa si Bitcoin sube hoy o baja mañana, te importa si en los próximos 2 años habrá adopción masiva o crisis de liquidez.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# 2. Agente Fondo Oportunidad (Value Investor)
agente_oportunidad = Agent(
    role="Cazador de Ofertas (Value Investor)",
    goal="Vigilar caídas históricas (RSI < 25 en gráfica diaria o semanal) para usar la reserva de efectivo.",
    backstory="Eres seguidor de la filosofía de Warren Buffett. Guardas efectivo pacientemente durante meses y solo compras cuando hay pánico absoluto en las calles.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# 3. Agente Orquestador DCA (Gestor de Ahorros)
agente_inversor_largo_plazo = Agent(
    role="Gestor de Ahorros a Largo Plazo",
    goal="Tomar la decisión final de ejecutar el DCA normal o usar el Fondo de Oportunidad.",
    backstory="Eres el líder del fondo de pensiones. Tu trabajo es asegurar que el cliente acumule riqueza a 10 años. Ignoras el ruido, compras cada mes pase lo que pase, pero escuchas a tus asesores por si hay una ganga histórica.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm
)

# ==========================================
# PRUEBA RÁPIDA (EJECUCIÓN)
# ==========================================
if __name__ == "__main__":
    tarea_decision = Task(
        description='''
        El Agente Macro-Económico reporta: La Reserva Federal acaba de bajar las tasas de interés. Tendencia macro alcista.
        El Agente Fondo Oportunidad reporta: Mercado tranquilo, RSI diario en 55. No hay pánico, guardar la reserva de efectivo.
        Capital disponible para DCA rutinario: 100 USD. Capital de Reserva: 1000 USD.
        
        Evalúa estos reportes y toma una decisión sobre la inversión de este mes. Responde en formato JSON estricto con las claves: "decision" (DCA_NORMAL, USAR_RESERVA, MANTENER_TODO_EN_EFECTIVO) y "razonamiento".
        ''',
        expected_output='Un JSON con la decisión final y la justificación.',
        agent=agente_inversor_largo_plazo
    )

    crew = Crew(
        agents=[agente_macroeconomico, agente_oportunidad, agente_inversor_largo_plazo],
        tasks=[tarea_decision],
        process=Process.sequential
    )

    print("Iniciando comité mensual de ahorros e inversión...")
    resultado = crew.kickoff()
    print("========================================")
    print("DECISIÓN FINAL DEL GESTOR DE AHORROS:")
    print(resultado)
