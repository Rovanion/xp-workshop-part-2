from use_case import *
from domain import Direction, initial_input, Map, Material, Position

MAP = Map(materials=[Material.FLOOR, Material.FLOOR, Material.FLOOR,
                     Material.FLOOR, Material.FLOOR, Material.FLOOR,
                     Material.FLOOR, Material.FLOOR, Material.FLOOR],
          objects=[],
          width=3)
PLAYER = Player(name='test',
                position=Position(1.5, 1.5),
                forward=Direction(0.0, -1.0))

def test_freeze():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  state, _ = handle_event(state, 'tick', 0.070)
  assert state.player.position.x == 1.5
  assert state.player.position.y == 1.5
  assert state.player.forward.x == 0.0
  assert state.player.forward.y == -1.0


def test_move_forward():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  state, _ = handle_event(state, 'input', initial_input._replace(forward=True))
  state, _ = handle_event(state, 'tick', 0.070)
  assert state.player.position.x == 1.5
  assert state.player.position.y < 1.5
  assert state.player.forward.x == 0.0
  assert state.player.forward.y == -1.0

def test_turn_right():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  state, _ = handle_event(state, 'input', initial_input._replace(turn_right=True))
  state, _ = handle_event(state, 'tick', 0.070)
  assert state.player.position.x == 1.5
  assert state.player.position.y == 1.5
  assert state.player.forward.x > 0.0
  assert state.player.forward.y > -1.0


def test_move_backwards():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  state, _ = handle_event(state, 'input', initial_input._replace(backward=True))
  state, _ = handle_event(state, 'tick', 0.070)
  assert state.player.position.x == 1.5
  assert state.player.position.y > 1.5
  assert state.player.forward.x == 0.0
  assert state.player.forward.y == -1.0

def test_turn_left():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  state, _ = handle_event(state, 'input', initial_input._replace(turn_left=True))
  state, _ = handle_event(state, 'tick', 0.070)
  assert state.player.position.x == 1.5
  assert state.player.position.y == 1.5
  assert state.player.forward.x < 0.0
  assert state.player.forward.y > -1.0

def test_other_players():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  bengt = Player(
    name='bengt',
    position=Position(1.5, 1.5),
    forward=Direction(0.0, -1.0))
  state, _ = handle_event(state, 'player', bengt)
  state, _ = handle_event(state, 'tick', 0.070)
  assert state.other_players['bengt'] == bengt

def test_exit_server():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  state, commands = handle_event(state, 'exit', None)
  state, _ = handle_event(state, 'tick', 0.070)
  assert len(list(filter((lambda c: c[0] == 'leave'), commands))) == 1

def test_leave():
  state = initial_state(initial_input, PLAYER, MAP, 3, 5)
  bengt = Player(
    name='bengt',
    position=Position(1.5, 1.5),
    forward=Direction(0.0, -1.0))
  state, _ = handle_event(state, 'player', bengt)
  state, _ = handle_event(state, 'player_left', 'bengt')
  state, _ = handle_event(state, 'tick', 0.070)
  assert 'bengt' not in state.other_players.keys()
