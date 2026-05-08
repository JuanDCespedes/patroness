# Asteroids Refactorizado

## Descripcion
Este repositorio contiene una version refactorizada del juego "Asteroids" en Python y Pygame. El codigo se reorganizo para ser mas modular, legible y facil de extender.

## Cambios principales realizados
- Reemplace la logica monolitica de `asteroids.py` por un motor de juego basado en clases.
- Separe la creacion de objetos en una fabrica con `ObjectFactory`.
- Anade un `GameManager` singleton para controlar el estado global del juego.
- Implemente un `GameState` con `PlayingState` y `GameOverState` para manejar fases del juego.
- Anade un `EventManager` y un `ScoreObserver` para notificar eventos de colision.
- Anade invulnerabilidad temporal al chocar con un asteroide.
- Hice que el asteroide desaparezca cuando choca con la nave.
- Mejore los controles para aceptar `A`, `W`, `D`, `SPACE` y tambien las flechas `LEFT`, `UP`, `RIGHT`.
- Cambie el color del texto de vida a rojo cuando la vida es baja.
- Refactorice componentes en archivos separados para mejorar el mantenimiento.

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

## Como ejecutar
1. Activa el entorno virtual:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. Ejecuta el juego:
   ```powershell
   python asteroids.py
   ```

## Notas
- Si la ventana no responde a los controles, asegurate de que este activa y con foco.
- El texto de vida cambia a rojo cuando la vida baja de 30.
- Si deseas ajustar el nivel de dificultad, puedes cambiar el numero maximo de asteroides y la frecuencia de aparicion en `game_state.py`.
