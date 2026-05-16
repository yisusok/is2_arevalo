# Caso de Uso del Patrón Flyweight

### Situación de utilidad: **Sistema de Renderizado de Partículas para un Videojuego (Ej: Lluvia o Tormenta de Nieve)**

Imagina que estás desarrollando un videojuego donde ocurre una tormenta y necesitas renderizar **100,000 gotas de agua simultáneamente** en pantalla en tiempo real. 

Cada gota de agua individual tiene propiedades que se dividen en dos categorías:
1. **Estado Intrínseco (Compartido/Invariable):** La textura en alta definición, la malla de polígonos (modelo 3D), el color base y el comportamiento físico ante la luz. Estos datos consumen mucha memoria RAM (por ejemplo, 5 MB por cada modelo).
2. **Estado Extrínseco (Variable/Contextual):** Las coordenadas de posición actual $(X, Y, Z)$, la velocidad de caída actual y el ángulo de inclinación afectado por el viento. Estos datos cambian en cada fotograma y ocupan muy poco espacio (apenas unos bytes).

---

### El Problema sin Flyweight
Si el motor del juego creara 100,000 objetos independientes de la clase `Gota`, donde cada instancia duplica internamente los datos pesados de la textura y la geometría:

$$\text{Memoria requerida} = 100,000 \times 5 \text{ MB} = 500,000 \text{ MB} \approx 500 \text{ GB de RAM}$$

El sistema colapsaría (*crash*) instantáneamente por falta de memoria al intentar instanciar la tormenta.

---

### La Solución con Flyweight
Aplicando el patrón, se separa el estado pesado (intrínseco) del liviano (extrínseco):

1. **Objeto Flyweight (`TipoParticulaGota`):** Se crea una **única instancia** en memoria que almacena la textura de 5 MB y el modelo 3D.
2. **Contexto (`GotaIndividual`):** Se crean 100,000 objetos extremadamente ligeros que solo contienen sus coordenadas $(X, Y, Z)$ y una referencia/puntero al único objeto `TipoParticulaGota` compartido.

Al momento de dibujar la pantalla (*renderizar*), el bucle del juego recorre las 100,000 posiciones y le pasa las coordenadas dinámicas como argumentos al método de dibujo de la única textura compartida. 

### Beneficio
El consumo de memoria se reduce drásticamente de **500 GB a escasos Megabytes** (5 MB fijos de la textura + la estructura liviana de las posiciones), permitiendo que el juego funcione fluidamente a altas tasas de refresco (FPS).