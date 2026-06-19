# Asteroids Refactorizado
- Juan Diego Céspedes Uribe - 20232020148
- Juan David Bejarano Cristancho - 20232020056
- Juan Camilo Rueda Leon - 20232020110
## Descripcion
Este repositorio contiene una version refactorizada del juego "Asteroids" en Python y Pygame. El codigo se reorganizo para ser mas modular, legible y facil de extender.

## Cambios principales realizados
- Se reemplazo la logica monolitica de `asteroids.py` por un motor de juego basado en clases.
- Se señaro la creacion de objetos en una fabrica con `ObjectFactory`.
- Se añidio un `GameManager` singleton para controlar el estado global del juego.
- Se implemento un `GameState` con `PlayingState` y `GameOverState` para manejar fases del juego.
- Se añadio un `EventManager` y un `ScoreObserver` para notificar eventos de colision.
- Se añadio invulnerabilidad temporal al chocar con un asteroide.
- Se hizo que el asteroide desaparezca cuando choca con la nave.
- Se mejoraron los controles para aceptar `A`, `W`, `D`, `SPACE` y tambien las flechas `LEFT`, `UP`, `RIGHT`.
- Se cambio el color del texto de vida a rojo cuando la vida es baja.
- Se refactorizaron componentes en archivos separados para mejorar el mantenimiento.

## Patrones de diseno aplicados
- **Singleton**: `GameManager` garantiza una unica instancia que controla el ciclo principal del juego.
- **Factory**: `ObjectFactory` crea asteroides y balas, desacoplando la construccion de objetos de su uso.
- **State**: `GameState` con `PlayingState` y `GameOverState` separa la logica de cada fase del juego.
- **Observer**: `EventManager` notifica eventos de colision a observadores, como `ScoreObserver`.
- **Strategy**: `MovementStrategy` permite definir comportamientos de movimiento intercambiables para los asteroides.

## Ejemplos de implementacion
### Singleton (`GameManager`)
```python
class GameManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance
```
Este patron asegura que solo exista una instancia de `GameManager` que controla la inicializacion y el ciclo principal.

### Factory (`ObjectFactory`)
```python
class ObjectFactory:
    def __init__(self, size):
        self.size = size

    def create_asteroid(self):
        return Asteroid(self.size)

    def create_bullet(self, pos, angle, vel):
        return Bullet(pos, angle, vel, self.size)
```
La fabrica desacopla la creacion de asteroides y balas de su uso en la logica del juego.

### State (`GameState`)
```python
class PlayingState(GameState):
    def update(self):
        self.game_manager.ship.update()
        ...
        if self.game_manager.ship.vida <= 0:
            self.game_manager.change_state(GameOverState(self.game_manager))
```
El patron state permite cambiar facilmente entre el estado de juego activo y el estado de game over.

### Observer (`EventManager`)
```python
class EventManager:
    def subscribe(self, event_type, listener):
        ...

    def notify(self, event_type, data=None):
        ...
```
```python
class ScoreObserver:
    def update(self, event_type, data):
        if event_type == "collision":
            print(f"Collision detected: {data}")
```
Este patron notifica eventos de colision a los observadores registrados.

### Strategy (`MovementStrategy`)
```python
class MovementStrategy:
    def move(self, obj):
        pass

class RandomMovement(MovementStrategy):
    def move(self, obj):
        pass
```
El patron strategy permite definir diferentes formas de mover a los asteroides sin cambiar su clase principal.


## Antipatrones Identificados (Código Original)
Durante la fase de análisis del código original, se identificaron los siguientes 15 antipatrones, los cuales justificaron la necesidad de esta refactorización:

### 1. Importaciones de comodín (Star Imports)
Importar con * contamina el espacio de nombres y hace difícil saber de dónde viene cada función, lo que puede causar colisiones de nombres.

```Python
from pygame.locals import *
from ship import *
```
### 2. Cargar recursos repetidamente desde el disco (I/O Bottleneck)
El código leía el disco duro cada vez que se creaba una bala o un asteroide.
```
Python
# En Bullet.__init__ y Asteroid.__init__
self.image=pygame.image.load("imagenes/bala.png")
```
### 3. Modificar una lista mientras se itera sobre ella
Eliminar elementos dentro de un bucle for que itera sobre la misma lista altera los índices y hace que el bucle se salte elementos.
```
Python
for bullet in ship.bullets:
    # ...
    if bullet.alcance ==0:
        ship.bullets.remove(bullet) # ¡Peligro!
```

### 4. Instanciar objetos pesados en el bucle principal
Crear la fuente de texto cada fotograma dentro del bucle de juego consumía muchísima memoria y CPU innecesariamente.
```
Python
while 1:
    # ...
    fuente=pygame.font.Font(None, 45)
    fuente_go=pygame.font.Font(None,100)
```
### 5. Uso de while 1: en lugar de while True:
Aunque funciona por compatibilidad, while True: es el estándar moderno por ser más explícito y legible.
```
Python
while 1:
    for event in pygame.event.get():
```
### 6. Inicialización de la clase padre a la antigua
En Python moderno, se debe usar super().__init__() en lugar de llamar a la clase padre directamente para evitar problemas en herencias complejas.
```
Python
class Asteroid(Sprite):
    def __init__(self, cont):
        Sprite.__init__(self) # Antipatrón
```
### 7. Concatenación de cadenas anticuada
Usar + str(variable) es menos legible y ligeramente más lento que usar F-Strings.
```
Python
texto_puntos=fuente.render("Puntos: "+str(ship.puntos),1,(250,250,250))
```
### 8. Control de FPS mediante retrasos (Delay)
Usar pygame.time.delay() pausa todo el programa, haciendo que la velocidad del juego dependa directamente de la velocidad del procesador en lugar de usar un reloj.
```
Python
pygame.display.update()
pygame.time.delay(10)
```
### 9. Comprobaciones redundantes en listas
Comprobar si un elemento está en la lista mientras se itera sobre ella es una redundancia lógica.
```
Python
for asteroid in asteroids:
    # ...
    if asteroid in asteroids: # Redundante
        asteroid.explotar()
 ```
### 10. Lógica de renderizado mezclada con lógica de actualización
Hacer un screen.blit dentro de la lógica de colisiones rompe el principio de responsabilidad única.
```
Python
if asteroid.rect.colliderect(bullet.rect):
    asteroid.explotar()
    screen.blit(asteroid.image, asteroid.rect) # Lógica mezclada
```
### 11. Disparo sin tiempo de enfriamiento (Cooldown)
Se ejecutaba la acción de disparo en cada fotograma si se mantenía presionada la tecla, agotando la memoria.
```
Python
elif teclas[K_SPACE]:
    self.disparar() # Se ejecuta 60 veces por segundo
```
### 12. Números mágicos (Magic Numbers)
Uso de valores literales sin contexto ni variables descriptivas.
```
Python
if random.randint(0,100) % 25 == 0 and len(asteroids) < 10:
```
### 13. Ruptura del encapsulamiento
El archivo main.py accedía y modificaba directamente las propiedades internas de otras clases (ej. restando vida directamente).
```
Python
if ship.rect.colliderect(asteroid.rect):
    ship.vida -= 10
```
### 14. Efecto visual inútil (Condición de carrera visual)
El método explotar() cambiaba la imagen del asteroide, pero el objeto era eliminado de la lista inmediatamente, por lo que el usuario nunca veía la explosión.
```
Python
asteroid.explotar()
screen.blit(asteroid.image, asteroid.rect)
asteroids.remove(asteroid) # Borra la explosión al instante
```
### 15. Rutas de archivos fuertemente acopladas
Las rutas a recursos estaban quemadas en el código sin usar librerías como os.path.join, dificultando la compatibilidad entre sistemas operativos.
```
Python
self.imagen_base=pygame.image.load("imagenes/nave.png")
```
## Archivos relevantes
- `asteroids.py`: punto de entrada del juego.
- `game_manager.py`: controla la inicializacion, ciclo de juego y cambio de estado.
- `game_state.py`: contiene los estados del juego y la logica de renderizado.
- `ship.py`: logica de la nave, controles y disparo.
- `asteroid.py`: logica de los asteroides.
- `bullet.py`: logica de las balas.
- `object_factory.py`: fabrica de objetos del juego.
- `event_manager.py`: gestion de eventos y observadores.
- `movement_strategy.py`: estrategia de movimiento para asteroides.

## Antipatrones Identificados (Código Original)

*1. Importaciones de comodín (Star Imports)*
python
from pygame.locals import *
from ship import *


*2. Cargar recursos repetidamente desde el disco (I/O Bottleneck)*
python
En Bullet.__init__ y Asteroid.__init__
self.image=pygame.image.load("imagenes/bala.png")


*3. Modificar una lista mientras se itera sobre ella*
python
for bullet in ship.bullets:
    if bullet.alcance ==0:
        ship.bullets.remove(bullet) # ¡Peligro!


*4. Instanciar objetos pesados en el bucle principal*
python
while 1:
    fuente=pygame.font.Font(None, 45)
    fuente_go=pygame.font.Font(None,100)


*5. Uso de while 1: en lugar de while True:*
python
while 1:
    for event in pygame.event.get():


*6. Inicialización de la clase padre a la antigua*
python
class Asteroid(Sprite):
    def __init__(self, cont):
        Sprite.__init__(self) # Antipatrón


*7. Concatenación de cadenas anticuada*
python
texto_puntos=fuente.render("Puntos: "+str(ship.puntos),1,(250,250,250))


*8. Control de FPS mediante retrasos (Delay)*
python
pygame.display.update()
pygame.time.delay(10)


*9. Comprobaciones redundantes en listas*
python
for asteroid in asteroids:
    if asteroid in asteroids: # Redundante
        asteroid.explotar()


*10. Lógica de renderizado mezclada con lógica de actualización*
python
if asteroid.rect.colliderect(bullet.rect):
    asteroid.explotar()
    screen.blit(asteroid.image, asteroid.rect) # Lógica mezclada


*11. Disparo sin tiempo de enfriamiento (Cooldown)*
python
elif teclas[K_SPACE]:
    self.disparar() # Se ejecuta 60 veces por segundo


*12. Números mágicos (Magic Numbers)*
python
if random.randint(0,100) % 25 == 0 and len(asteroids) < 10:


*13. Ruptura del encapsulamiento*
python
if ship.rect.colliderect(asteroid.rect):
    ship.vida -= 10


*14. Efecto visual inútil (Condición de carrera visual)*
python
asteroid.explotar()
screen.blit(asteroid.image, asteroid.rect)
asteroids.remove(asteroid) # Borra la explosión al instante


*15. Rutas de archivos fuertemente acopladas*
python
self.imagen_base=pygame.image.load("imagenes/nave.png")
