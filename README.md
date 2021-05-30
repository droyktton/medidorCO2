# Medidor de CO2  

Este repositorio público documenta los detalles técnicos de un medidor de concentracion de CO2 en el aire usando un sensor NDIR, una placa Arduino y otros accesorios. Incluye los detalles del hardware, con sus componentes y circuitos, y del software usado para controlar, mediante una placa Arduino, la adquisición de datos del sensor y la actuación sobre dispositivos de salida como pantallas, bocinas, y puerto serial. 

___

## Motivación
El covid19 se contagia principalmente por vía aérea, a través de la exhalación de aerosoles por personas infectadas (típicamente asíntomáticas o presintomáticas!), y la consiguiente inhalación de estos aerosoles contaminados por personas susceptibles. Cuando inhalamos aerosoles, estos se puede adherir a nuestros tractos respiratorios. Existe luego una probabilidad finita de que el virus, aún activo, se libere del interior de la gotita y alcance los receptores que propician su multiplicación en el cuerpo.  

Los aerosoles que pueden potencialmente transportar carga viral están constituídos por un espectro de partículas micrométricas que pueden permanecer en el aire desde decenas de segundos hasta muchas horas (análogo al polen por ejemplo). En exteriores, los aerosoles exhalados por un infectado solo pueden ser inhalados por personas a pequeña distancia, ya que a gran distancia se diluyen rápidamente. En interiores, sin embargo, existen ambas, las rutas denominadas de corto y de largo alcance. La importancia de la última ruta depende crucialmente de los sistemas de ventilación. Compartiendo una sala con una o más personas infectadas, la dosis total de exposición al virus es igual al producto de su concentración por el tiempo. Para reducir el riesgo de contagio en interiores, además de usar de barbijos capaces de retener una fracción de los aerosoles exhalados e inhalados, la ventilación debe aumentarse y el tiempo y densidad de ocupación debe ser reducido, tanto más cuanto más fuerte sea la actividad desarrollada en el lugar, ya que esta determina la tasa volumetrica de respiración de los ocupantes.

### ¿Porqué medir CO2?
No sabemos cuanto virus hay en el aire, pero está claro que el riesgo está en respirar aire ya respirado por otro. Cuando respiramos, llevamos el oxígeno del aire a los pulmones y de ahí a la sangre, que lo lleva a las células. El CO2 que liberan las celulás es transportado en camino inverso hacia los pulmones y cuando exhalamos liberamos aire con una concentración de CO2 del orden de 40000 ppm (partes por millón), muchisímo más alta que la concentración media de CO2 en cualquier interior. Si no existen otras fuentes de CO2 en el ambiente, una forma fácil de saber que fracción del aire que estamos respirando ya fue respirado por otra persona es entonces medir la concentración de CO2 que está en exceso con respecto de su valor en el exterior. Este exceso depende fuertemente de las características de ventilación de la sala.

### ¿Qué concentración de CO2?
La concentración de CO2 es sólo un proxy a la concentración potencial de virus activo en el aire. Una concentración alta de CO2 implica una concentración potencialmente alta de virus, pero esta última también depende del número de personas infectadas en el lugar, de la calidad y buen uso de los tapabocas por los ocupantes, y de la existencia de filtros de aire y de otras condiciones físicas. En cualquier caso, la concentración de CO2 es un indicador de riesgo útil.   

Aunque existen modelos, es muy dificil estimar una probabilidad de contagio cuantitativamente. Una recomendación simple pero práctica es mantener la concentración  de CO2 en un interior a valores < 800 ppm. Esto es recomendado cuando la ocupación es compartida por una duración estandard, la típica de clases o de trabajo de oficina, ya que la dosis total bajo exposición al virus es igual al producto de su concentración por el tiempo (así, cualquier exceso de CO2 con respecto del exterior es peligroso si la exposición es muy prolongada). Si se puede medir en la sala desocupada, uno puede determinar el número de cambios de aire por hora o ACH cargando el ambiente con CO2 de forma controlada y monitoreando su descarga hacia el valor del equilibrio. Ambas mediciones pueden relacionarse, y [aquí](https://droyktton.github.io/loscoihues/ventilacion/CO2ACHProbInfeccionV3.html) proveemos una calculadora para hacerlo cuantitativamente.  

### ¿Estoy ventilando bien?
La recomendación general es mantener una ventilación cruzada, continua, y distribuída. Sin embargo cada interior tiene sus características, sus aberturas, su volumen, sus conexiones con otros espacios, un exterior de ciertas características, y un número de ocupantes realizando determinadas actividades. Esta entonces claro que la ventilación que funciona en un lugar puede no ser adecuada en otro lugar. En particular, si la temperatura exterior es muy baja por ejemplo, no podremos aplicar una ventilación natural exagerada. Por todo esto es que la ventilación tiene que ser también medida. Medir en el lugar y momento concretos nos permite responder a las preguntas: ¿Esta en este momento bien ventilando mi ambiente?, ¿Qué puedo hacer para mejorar la ventilación de mi sala?. La medición de CO2 nos permite experimentar distintas condiciones de ventilación hasta encontrar la adecuada, sin necesidad de complicados modelos matemáticos que dependen de todas las características del interior arriba mencionadas.

___

# Medidor
 
## Funcionalidad
El medidor muestra la concentración de CO2, la temperatura y la humedad relativa, en una pantalla. Los mismos datos son impresos en el puerto serial para otros usos. Usando un pulsador podemos iniciar una rutina de calibración forzada, opcional. El medidor se alimenta con 5V o 9V, para lo cual se puede usar un cargador enchufado, o una batería. Es importante colocar el medidor lejos de las personas y no obstruir sus conductos de ventilación traseros que permiten que el aire circule libremente a través del sensor. 

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

# Agradecimientos

+ A Eduardo Jagla por la motivación y discusión.
+ A Pierre Arneodo por diseñar y armar los gabinetes.
+ A Luciano Lamaite y Jorge Aliaga por los tips técnicos y comerciales.
+ Al Instituto Balseiro por apoyar la iniciativa. 



