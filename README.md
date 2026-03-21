# Proyecto final de Computacion
Grupo 7 conformado por:
- Douglas Barreto
- Laura Montes
- Alejandro Huérfano

Dataset: Amazon Sales

# Planteamiento del Problema
En el ámbito del comercio electrónico o incluso en redes sociales, los criterios superficiales como el promedio de calificaciones en un producto, se asume convencionalmente como un indicador de éxito y satisfacción del usuario, sin embargo, el hecho de una calificación considerablemente “buena” ignora el sesgo intrínseco en las personas a la hora de puntuar.  

El análisis crítico de un consumidor a través de reseñas es deteriorado por un sesgo de selección, es decir, se ven altamente motivados a la interacción sincera únicamente cuando su experiencia con el producto fue muy gratificante, o por el contrario, muy deficiente, así ocultando el rendimiento real del producto. En este campo también se incluye el operamiento de estrategias de descuento, se asocia con cambios en la percepción del consumidor para su compra inmediata; se dice que a mayor descuento del producto genera mayor satisfacción en el usuario y un mayor umbral de interacción.  
	
El objetivo investigativo se centrará en un análisis comparativo a distintas distribuciones del rating bajo distintos niveles de descuentos, con el fin de hallar patrones de comportamiento, siendo así, la identificación de anomalías con procedimientos estadísticos descriptivos; como dispersión en las calificaciones y frecuencia de términos críticos o interacciones como lo son las reseñas, permitiendo observar si el porcentaje del descuento y en el precio existe algún tipo de correlación, las cuáles en base a lo demostrado podría sugerir una discrepancia entre el rating y la crítica descriptiva.

# Objetivo General
Evaluar cómo la estrategia de descuentos influyen en la percepción de calidad y en la polarización del discurso del consumidor en el dataset de Amazon Sales.
## Objetivos Especificos
* Describir la distribución de las calificaciones para identificar la presencia de polarización en las opiniones de los usuarios.
* Comparar el promedio de rating en función de los rangos del porcentaje de descuento para determinar si a mayor descuento existe una tendencia a calificar con menor rigurosidad.
* Establecer agrupaciones de satisfacción basadas en el rating para determinar cómo estas categorías influyen en la variabilidad del precio actual y en el posicionamiento de las ventas.

# Marco Teórico
El riesgo de que un usuario de Amazon reciba un producto de mala calidad o defectuoso está presente. La asimetría de la información aborda situaciones en las que una de las dos partes (emisor y receptor) posee información que el otro desconoce; debido a este factor, el comprador se ve obligado a depender de reseñas que sirven como señalizadores que la misma empresa hace visibles para reducir la incertidumbre. Para superar esta asimetría, las señales deben garantizar que solo se envíe información que refleje atributos o capacidades reales del producto. En sintonía con las reseñas de Amazon, la «prueba social» es el fenómeno por el cual, si el comprador observa que muchos usuarios adquirieron el producto y otorgaron una buena puntuación, percibe que el riesgo de error es menor.  
	
No obstante, la fiabilidad de estas señales no opera por sí sola, sino que se ve apoyada en la percepción económica del usuario aplicada durante el proceso de compra. En este contexto, el efecto anclaje (anchoring) toma un papel fundamental, ya que es un sesgo cognitivo en el que la primera información que percibe una persona condiciona la toma de sus decisiones. Al mostrar un precio inicial tachado y hacer énfasis en el costo posterior al descuento, el producto se vuelve más llamativo, e impulsa la compra por una percepción de ahorro más que por el valor intrínseco del bien. La utilidad de la transacción puede llegar a dominar la percepción general, provocando que el usuario otorgue calificaciones elevadas no necesariamente por la excelencia del producto, sino como un reflejo del bienestar derivado del ahorro percibido.  
	
Cuando desplazamos el análisis hacia el precio actual, sin sesgos por ofertas, entra en juego el criterio de exigencia del usuario. Bajo este contexto, los productos con un mayor costo generan en el consumidor un rol más estricto; cualquier mínima discrepancia entre la calidad esperada y la obtenida se traduce en una penalización más severa en el rating, lo que conduce a una heterogeneidad de opiniones. De igual forma ocurre con los productos más económicos: el beneficio monetario hace que el usuario reduzca sus niveles de exigencia. En ambos casos, el juicio del consumidor se rige según la Teoría de la desconfirmación de expectativas.

