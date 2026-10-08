# 🏛️ Tutor Financiero IA (Robo-Advisor & Simulador DCA)

Un sistema integral de **Paper Trading** y asesoría financiera impulsado por algoritmos técnicos. A diferencia de los bots tradicionales de especulación rápida (Scalping), esta plataforma está diseñada específicamente para estrategias de **Ahorro a Largo Plazo**, **Dollar-Cost Averaging (DCA)** y **Value Investing** sobre mercados tradicionales y emergentes.

---

## 🚀 Funcionalidades Principales

* **Billetera Virtual Persistente:** Simulador con un saldo inicial de $100 USD. El progreso de la cartera se guarda permanentemente en la memoria del navegador (`localStorage`), permitiendo retomar la inversión al día siguiente.
* **Gráficos en Tiempo Real:** Visualización fluida de velas (OHLCV) e indicadores técnicos (SMA20, RSI) utilizando la tecnología de TradingView.
* **Perfiles de Inversión Adaptativos:**
  * **🏛️ Inversor Institucional (Largo Plazo):** Ejecuta estrategias de DCA programado y "Fondos de Oportunidad" automáticos en gráficas diarias.
  * **⚡ Simulador Educativo (Corto Plazo):** Entorno de alta velocidad en gráficas de 1 minuto para testear UI y algoritmos de Scalping.
* **Inteligencia de Mercado Dinámica:** Un panel educativo que cambia automáticamente según el activo seleccionado, enseñando al usuario los horarios operativos (Hora de Buenos Aires), ventanas de liquidez institucional y advertencias de peligro (ej. "Ruido lateral" de fin de semana).
* **Historial de Operaciones:** Registro inmutable en el backend (`trades_history.json`) de cada compra o venta, guardando métricas de rendimiento y precio promedio de entrada.

---

## 🛡️ Conceptos de Protección de Inversión y Gestión de Riesgo

El sistema implementa doctrinas financieras del mundo real para proteger el capital del usuario:

1. **DCA (Dollar-Cost Averaging):** En lugar de invertir todo el capital de golpe en un posible pico de mercado, el "Inversor Institucional" promedia su costo comprando pequeñas fracciones ($10) en intervalos regulares, anulando el riesgo de la volatilidad a corto plazo.
2. **Caza de Pánicos (Oportunidades):** El algoritmo vigila el mercado. Si detecta un "Crash" o miedo extremo (RSI < 30), activa un fondo de reserva ($50) para comprar activos a precios de descuento.
3. **Señales de Venta (Stop Loss Técnico):** El backend no solo compra; tiene la capacidad de detectar tendencias bajistas prolongadas o zonas de sobrecompra masiva (RSI > 70) para liquidar posiciones y proteger las ganancias.

---

## 🔒 Sistemas de Protección de Fallos Implementados

Para asegurar que el simulador sea a prueba de balas tanto en código como en interacción humana:

* **Modo Copiloto (Seguro contra IAs):** Un escudo de confirmación interactiva. Si la IA detecta una oportunidad, pausa la ejecución y despliega una ventana detallando su razonamiento técnico. Nada se compra con el dinero del usuario sin su click en "Aceptar Operación".
* **Botón de Cierre de Emergencia (Panic Button):** Un botón rojo en la tabla de Posiciones Activas que permite al usuario puentear a la IA, liquidar el 100% de la posición al instante al precio actual de mercado, y recuperar sus dólares en efectivo.
* **Auto-Recuperación de Datos (Sanity Checks):** Mecanismos de seguridad en JavaScript que interceptan archivos de guardado corruptos o de versiones anteriores. Si detecta valores matemáticos rotos (`NaN` o `Undefined`), los repara automáticamente en segundo plano para evitar que la interfaz colapse.

---

## 🛠️ Stack Tecnológico y Librerías

El proyecto mantiene una arquitectura desacoplada y ligera:

### Frontend (UI / Cliente)
* **HTML5 / Vanilla JavaScript:** Lógica de estado sin frameworks pesados.
* **Tailwind CSS (CDN):** Estilizado rápido y diseño responsivo "Dark Mode".
* **Lightweight Charts (TradingView):** Motor de renderizado en canvas para gráficas financieras profesionales de altísimo rendimiento.

### Backend (Servidor API)
* **Python 3.x:** Lenguaje principal del motor analítico.
* **FastAPI + Uvicorn:** Creación de una API REST ultrarrápida y asíncrona (Puerto 8766).
* **yfinance:** Conexión en tiempo real con Yahoo Finance para obtener la data de todos los mercados bursátiles del mundo gratis.
* **ta (Technical Analysis Library):** Librería matemática para calcular indicadores clave (RSI, Medias Móviles, Bollinger) directamente sobre DataFrames.
* **pandas:** Manipulación masiva de datos y cálculo de series de tiempo.

---

## 🌍 Mercados Disponibles

El proyecto soporta el análisis técnico y la simulación de compras de los siguientes activos internacionales:

* **Tradicionales EE.UU.:** S&P 500 (`SPY`), Nasdaq 100 (`QQQ`).
* **Inteligencia Artificial y Robótica:** Nvidia (`NVDA`), ETF Robótica (`BOTZ`).
* **Asia y Emergentes:** ETF Mercado Chino (`MCHI`), Gigantes Web China (`KWEB`).
* **Materias Primas & Macro:** Oro Físico (`GC=F`), Bitcoin (`BTC-USD`).

---

> *Desarrollado como una suite educativa y de asistencia financiera local. No constituye consejo financiero real.*
