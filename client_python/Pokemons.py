class Pokemon:
    def __init__(self, value: float, direction: int, pos: tuple[float, float, float]):
        self._value = value
        self._direction = direction
        self._pos = pos

    def value(self):
        return self._value

    def direction(self):
        return self._direction

    def pos(self):
        return self._pos

    def set_value(self, value: float):
        self._value = value

    def set_direction(self, direction: int):
        self._direction = direction

    def set_pos(self, pos: tuple[float, float, float]):
        self._pos = pos


class Pokemons:
    def __init__(self):
        self._size = 0
        self._pokemons: {tuple[float, float, float], Pokemon} = {}

    def add(self, pokemon: Pokemon):
        if self._pokemons.get(pokemon.pos()) is None:
            self._pokemons[pokemon.pos()] = pokemon
            self._size += 1
            return True
        return False

    def pokemons(self):
        return self._pokemons

    def size(self):
        return self._size


