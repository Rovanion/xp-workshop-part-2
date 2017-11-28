from domain import Angle, find_first_collision, LineSegment, Player, Position

def rotate_player(player, input, frame_time, speed):
  rotation_sign = (1 if input.turn_right else 0) - (1 if input.turn_left else 0)

  if rotation_sign == 0:
    return player

  rotation_delta = Angle.from_radians(rotation_sign * speed * frame_time)
  new_forward = player.forward.rotate(rotation_delta)
  return player._replace(forward=new_forward)

def _try_to_move(map, from_, to):
  return to if find_first_collision(map, LineSegment(from_, to)) is None else from_

def move_player(player, map, input, frame_time, speed):
  movement_sign = (1 if input.forward else 0) - (1 if input.backward else 0)

  if movement_sign == 0:
    return player

  movement_delta = player.forward*(movement_sign * speed * frame_time)
  new_position = Position(player.position.x, player.position.y)

  x_target = Position(new_position.x + movement_delta.x, new_position.y)
  new_position = _try_to_move(map, from_=new_position, to=x_target)

  y_target = Position(new_position.x, new_position.y + movement_delta.y)
  new_position = _try_to_move(map, from_=new_position, to=y_target)

  return player._replace(position=new_position)
