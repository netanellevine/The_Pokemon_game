class Pokemon:
    def __init__(self, value: float, direction: int, pos: tuple[float, float, float]):
        self._value = value
        self._direction = direction
        self._killed = True
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

    def killed(self):
        return self._killed

    def set_killed(self, kill):
        self._killed = kill

    def set_pos(self, pos: tuple[float, float, float]):
        self._pos = pos


class Pokemons:
    def __init__(self):
        self._size = 0
        self._pokemons: {str, Pokemon} = {}

    def add(self, pokemon: Pokemon):
        key = f'{pokemon.pos()}'
        if self._pokemons.get(key) is None:
            self._pokemons[key] = pokemon
            pokemon.set_killed(False)
            self._size += 1
            return True
        self._pokemons.get(key).set_killed(False)
        return False

    def pokemons(self):
        return self._pokemons

    def size(self):
        return self._size


