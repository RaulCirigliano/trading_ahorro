# Proyecto Trading Ahorros - Contexto y Funcionalidades

## Visión General
Este proyecto es un "robo-advisor" y simulador de Paper Trading diseñado específicamente para estrategias de **Ahorro a Largo Plazo (DCA)** y **Value Investing**. A diferencia de los bots de scalping, esta plataforma se centra en crear riqueza promediando costos a lo largo de meses/años, o detectando pánicos históricos de mercado para invertir en activos tradicionales.

## Arquitectura y Stack Tecnológico
- **Frontend (`index.html`, `app.js`)**: Aplicación cliente estática que utiliza Lightweight Charts para gráficas y Tailwind CSS para el diseño (tema Slate/Amber). Funciona de forma desconectada del renderizado del servidor. Implementa persistencia local (`localStorage`) para el saldo de la billetera.
- **Backend (`backend/main.py`)**: API REST construida con **FastAPI** corriendo en el puerto `8766`. Usa `yfinance` para proporcionar datos reales de bolsas mundiales.
- **Persistencia de Historial**: El backend guarda y lee las operaciones de compra/venta en `backend/trades_history.json`.

## Funcionalidades y Herramientas Implementadas

### 1. Sistema de Paper Trading Robusto
- **Billetera Persistente**: Inicializa con $100.00 USD. Los fondos y activos se guardan en el navegador (`localStorage`). Incluye botón de reseteo (`🔄`).
- **Posiciones y PNL en Vivo**: Tabla de posiciones activas que calcula ganancias y pérdidas en tiempo real frente al precio promedio de compra.
- **Cierre de Emergencia (Panic Button)**: Permite liquidar el 100% de la posición activa de inmediato para retornar a dólares mediante un botón rojo de "✖️ Cerrar".
- **Historial de Transacciones**: Tabla con el registro perpetuo de las transacciones (fecha, tipo, modo, precio).

### 2. Modos de Ejecución (Seguridad)
- **👨‍✈️ Copiloto (Interactivo)**: El agente pausa el sistema al detectar una oportunidad y lanza una ventana emergente detallando la lógica, el precio y el modo, solicitando confirmación manual (Aceptar/Rechazar).
- **🤖 Autónomo**: El agente compra automáticamente sin intervención del usuario e informa mediante notificaciones en pantalla.

### 3. Perfiles del Agente (Estrategias)
- **🏛️ Inversor Institucional (DCA / Largo Plazo)**: 
  - Opera sobre velas de **1 Día**.
  - **DCA Automático**: Invierte $10 fijos periódicamente.
  - **Fondo de Oportunidad**: Invierte $50 de golpe si detecta pánico extremo (RSI < 30).
- **⚡ Simulador Educativo (Scalper 1 Minuto)**: 
  - Opera sobre velas de **1 Minuto**. 
  - Gasta y vende el 100% de los fondos basándose en cruces rápidos de Media Móvil (SMA20) y RSI. (Ideal para testing rápido de UI).

### 4. Mercados Globales Compatibles (`yfinance`)
- **Tradicionales**: SPY (S&P 500), QQQ (Nasdaq 100), Oro (GC=F), BTC-USD.
- **Transición y Emergentes**: MCHI (Mercado Chino), KWEB (Gigantes Web China).
- **IA y Futuro**: BOTZ (Robótica y AI), NVDA (Nvidia).

## Notas Técnicas para Desarrolladores
- **Lanzador**: Este proyecto se integra en un menú externo Tkinter en `/home/raul/.gemini/antigravity/scratch/ai_launcher/launcher.py`.
- **Ejecución Backend**: `cd backend && python main.py` (Se encarga de montar el servidor en el puerto 8766 y permite conexiones CORS del frontend).
- **CrewAI**: Se creó un prototipo de agentes en `backend/agentes_ia.py` listos para ser cableados como "Motor de Decisión" profundo en iteraciones futuras, si se conecta la API de Gemini Pro.
