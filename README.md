# Medidor de CO2  

Este repositorio público documenta los detalles técnicos de la construcción de un medidor económico *no comercial* de concentración de CO2 en el aire usando un sensor específico de tipo NDIR (infrarojo no dispersivo), una placa Arduino y otros accesorios comunes. Incluye los detalles del hardware, con sus componentes y circuitos asi como del software usado para controlar, mediante una placa Arduino, la adquisición de datos del sensor y la actuación sobre dispositivos de salida como pantallas, bocinas, y puerto serial. Software adicional permite leer el puerto serial para un análisis más detallado de las series temporales, en forma local o remota. 

Este proyecto puede ser perfectamente realizado por no especialistas, idealmente por aficionados de cualquier nivel de la gran comunidad de Arduino. No requiere conocimientos profundos de electrónica, ni de programación, ni de matemática, ni de física. Solo fue necesario realizar un par de soldaduras muy sencillas.
La comunidad del software y hardware libre es tan grande y generosa que basta saber googlear perseverantemente ante cualquier duda. Lo más dificil de este proyecto es comprar los sensores de CO2 ya que por ahora, en Argentina, hay que importarlos. El proyecto consistió en el armado de 5 medidores idénticos para medir la calidad del aire en la ciudad de San Carlos de Bariloche. Las mediciones y experimentos serán recopilados en un blog.  

Con este sencillo proyecto nos sumamos a la [campaña ventilar](https://www.argentina.gob.ar/ciencia/unidad-coronavirus/ventilar) desde San Carlos de Bariloche.

___

## Motivación

### COVID19

El covid19 se contagia principalmente por [vía aérea](https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(21)00869-2/fulltext#.YILw1d1ShYA.twitter), a través de la exhalación de aerosoles por personas infectadas (¡típicamente asíntomáticas o presintomáticas!), y la consiguiente inhalación de estos aerosoles contaminados por personas susceptibles. Cuando inhalamos aerosoles, algunas de estas gotitas se puede [adherir a nuestros tractos respiratorios](https://www.nature.com/articles/s42254-021-00307-4). Existe luego una probabilidad finita de que el virus, aún activo, se libere del interior de una de esas gotitas y alcance los [receptores](https://www.sciencedirect.com/science/article/abs/pii/S0092867420306759) que propician su multiplicación, con las conocidas consecuencias en la salud de las personas.  

Los aerosoles que pueden potencialmente transportar carga viral están constituídos por un [espectro de partículas micrométricas](https://www.sciencedirect.com/science/article/pii/S0021850208002036#fig4) que pueden permanecer en el aire desde decenas de segundos hasta muchas horas (análogo al polen por ejemplo). En exteriores, los aerosoles exhalados por un infectado sólo pueden ser inhalados por personas a pequeña distancia, ya que a gran distancia se diluyen rápidamente. En interiores, sin embargo, existen ambas, las rutas denominadas de [corto y de largo alcance](https://www.ajicjournal.org/article/S0196-6553(16)30531-4/pdf). Mientras que [la ruta de corto alcance](https://www.sciencedirect.com/science/article/pii/S0360132320302183) se puede controlar manteniendo una prudencial distancia, la ruta de largo alcance depende crucialmente de los [sistemas de ventilación](https://www.rehva.eu/fileadmin/user_upload/REHVA_COVID-19_guidance_document_V4.1_15042021.pdf). [Compartiendo una sala con una o más personas infectadas](https://english.elpais.com/society/2020-10-28/a-room-a-bar-and-a-class-how-the-coronavirus-is-spread-through-the-air.html?rel=mas), la dosis total de exposición al virus es igual al producto de su concentración por el tiempo. Para reducir el riesgo de contagio en interiores, además de usar de barbijos capaces de filtrar aerosoles en los dos sentidos (exhalados e inhalados), la ventilación debe aumentarse y el tiempo y densidad de ocupación debe ser reducido, tanto más cuanto más fuerte sea la actividad desarrollada en el lugar, ya que esta determina la tasa volumetrica de respiración de los ocupantes.


### ¿Porqué medir CO2?
No sabemos cuanto virus hay en el aire, pero está claro que el riesgo está en [respirar aire ya respirado por otro](https://youtu.be/ZMRyWUjleB0). Cuando respiramos, llevamos aire rico en oxígeno a los pulmones, el oxígento va de ahí a la sangre, que lo lleva a las células a través del sistema circulatorio. El CO2 que liberan las celulás es transportado en camino inverso hacia los pulmones y cuando exhalamos liberamos aire con una concentración de CO2 del orden de 40000 ppm (partes por millón), muchisímo más alta que la concentración media de CO2 en cualquier interior. Si no existen otras fuentes de CO2 en el ambiente, una forma fácil de saber que fracción del aire que estamos respirando ya fue respirado por otra persona es entonces medir la concentración de CO2 que está en exceso con respecto de su valor en el exterior. Este exceso depende fuertemente de las características de ventilación de la sala.

### ¿Qué concentración de CO2?
La concentración de CO2 es un [proxy](https://pubs.acs.org/doi/10.1021/acs.estlett.1c00183) a la concentración potencial de virus activo en el aire. Una concentración alta de CO2 implica una concentración potencialmente alta de virus, pero esta última también depende del número de personas infectadas en el lugar, de la calidad y buen uso de los [tapabocas](https://science.sciencemag.org/content/early/2021/05/19/science.abg6296) por los ocupantes, y de la existencia de filtros de aire y de otras condiciones físicas. En cualquier caso, la concentración de CO2 es un indicador de riesgo útil.   

Aunque existen [modelos teóricos](https://www.edx.org/es/course/physics-of-covid-19-transmission), es muy difícil hacer estimaciones precisas de la probabilidad de contagio, debido a la incertidumbre de algunos paramétros necesarios para hacer las [predicciones](https://www.medrxiv.org/content/10.1101/2020.08.26.20182824v2.full). Una recomendación simplista pero muy práctica es mantener la concentración  de CO2 en un interior a valores < 800 ppm, que implica que el 0.96% del aire que respiramos ya fue respirado. Se asume, en esta recomendación, que la ocupación es compartida por una duración estandard de algunas horas, la típica de clases o de trabajo de oficina, ya que la dosis total bajo exposición al virus es igual al producto de su concentración por el tiempo. Así, *cualquier* exceso de CO2 con respecto del exterior es peligroso si la exposición es muy prolongada. Si se puede medir en la sala desocupada, uno puede determinar el número de cambios de aire por hora o ACH cargando el ambiente con CO2 de forma controlada y monitoreando su descarga hacia el valor del equilibrio. [Ambas mediciones, la de las ppm de CO2 y el ACH pueden relacionarse fácilmente](https://schools.forhealth.org/wp-content/uploads/sites/19/2020/08/Harvard-Healthy-Buildings-program-How-to-assess-classroom-ventilation-08-28-2020.pdf), permitiendo realizar predicciones para el mismo interior, pero diferente número de personas por ejemplo. Ofrecemos [una calculadora online](https://droyktton.github.io/loscoihues/ventilacion/CO2ACHProbInfeccionV3.html) para facilitar los cálculos.

### ¿Estoy ventilando bien?
La recomendación general es mantener una ventilación cruzada, continua, y distribuída. Sin embargo cada interior tiene sus características, sus aberturas, su volumen, sus conexiones con otros espacios, un exterior de ciertas características, y un número de ocupantes realizando determinadas actividades. Esta entonces claro que la ventilación que funciona en un lugar puede no ser adecuada en otro lugar. En particular, si la temperatura exterior es muy baja por ejemplo, no podremos aplicar una ventilación natural exagerada. Por todo esto es que la ventilación tiene que ser también **medida**. Medir en el lugar y momento concretos nos permite responder a las preguntas: ¿Está en este momento bien ventilado mi ambiente?, ¿Qué puedo hacer para mejorar la ventilación de mi sala compartida?. La medición de CO2 nos permite experimentar distintas condiciones de ventilación hasta encontrar la adecuada, sin necesidad de complicados modelos matemáticos que dependen de todas las características del interior arriba mencionadas.

La recomendación más práctica y más segura es entonces que la ventilación sea [continua, cruzada, distribuída y medida](https://www.argentina.gob.ar/sites/default/files/covid-19-prevencion-de-transmision-por-aerosoles-2021_0.pdf). Es en este último punto que los medidores de CO2 son herramientas importantes (de hecho, la experimentación con estos medidores en estos interiores es la que nos lleva a concluir que la ventilación debe ser continua, cruzada y distribuída).

### Preguntas frecuentes
No se si todo, pero casi todo lo que uno querría saber y no se atreve a preguntar sobre la transmisión de covid19 por aerosoles, lo puede encontrar en éstas extensas [FAQ](https://docs.google.com/document/d/1fB5pysccOHvxphpTmCG_TGdytavMmc1cUumn8m0pwzo/edit#), con numerosos enlaces a las publicaciones relevantes.

### Argentina
Para reducir los riesgos de contagio en interiores, que es donde suelen ocurrir la mayoría de los contagios incluídos los peligrosos eventos de superpropagación de la enfermedad, es muy importante que aprendamos a ventilar, y que compartamos rápida y abiertamente los conocimientos y la experiencia, y que generemos más conciencia. Para más información, particularmente referida a Argentina, recomendamos visitar la [campaña ventilar](https://www.argentina.gob.ar/ciencia/unidad-coronavirus/ventilar).


___

# Medidor
 
## Funcionalidad
El medidor muestra la concentración de CO2, la temperatura y la humedad relativa, en una pantalla. Los mismos datos son impresos en el puerto serial para otros posibles usos, como monitoreo externo o remoto. Usando un pulsador podemos iniciar una rutina de calibración forzada, opcional, que se realiza esperando unos minutos en el exterior con el medidor encendido. El medidor se alimenta con 5V o 9V, para lo cual se puede usar un cargador enchufado, o una batería. Es importante colocar el medidor lejos de las personas y no obstruir sus conductos de ventilación traseros que permiten que el aire circule libremente a través del sensor. También es importante asegurarse de que no hayan fuentes de CO2 que no provengan de la respiración.

## Lista de Componentes
1. Sensor especifico para CO2:
2. Placa Arduino:
3. Salidas:
 1. Pantalla: LCD 16x2.
 2. Audio: Buzzer pasivo.
 3. Puerto Serial.
6. Alimentación: Batería Gadnic 10000 mAh.
7. Gabinete: Cajas de Luz.
8. Otros accesorios: 
   1. mini protoboard adhesiva. 
   2. cablecitos macho-macho, hembra-macho.
   3. Peines. 
   4. Resistencia.

## Circuito

## Software

___

# Proyectos Parecidos

+ [El de Jorge Aliaga](https://github.com/jlaliaga/Medidor-de-CO2)
+ https://www.instructables.com/CO2-Sensor-for-Schools/ 
+ https://emariete.com/medidor-casero-co2/
+ https://github.com/danielbernalb/LibreCO2/blob/main/INSTRUCCIONES%20en%20Espa%C3%B1ol.md
+ https://github.com/Sensirion/arduino-ble-gadget/blob/master/documents/SCD30_Monitor_Tutorial.md
+ https://github.com/anaireorg/anaire-devices
+ https://fablab.ruc.dk/co2/
+ https://github.com/Alitux/solarco2

# Agradecimientos

+ A Pierre Arneodo por diseñar y armar los gabinetes.
+ A Eduardo Jagla por la motivación, la experimentación, y la discusión.
+ A Luciano Lamaite y Jorge Aliaga por los tips técnicos y prácticos.
+ Al Instituto Balseiro por apoyar la iniciativa. 




