import collections
import enum
import math
import sys

smallest_number = sys.float_info.epsilon

class Angle:
  def __init__(self, radians):
    self.__radians = radians

  @classmethod
  def from_radians(class_, radians):
    return class_(radians)

  @classmethod
  def from_degrees(class_, degrees):
    return class_((math.pi * degrees) / 180)

  def to_radians(self):
    return self.__radians

  def to_degrees(self):
    return (180 * self.__radians) / math.pi

class _Vector(collections.namedtuple('_Vector', 'x, y')):
  def __add__(self, v):
    return _Vector(self.x + v.x, self.y + v.y)

  def __sub__(self, v):
    return _Vector(self.x - v.x, self.y - v.y)

  def __mul__(self, s):
    return _Vector(self.x * s, self.y * s)

  def __div__(self, s):
    return _Vector(self.x / s, self.y / s)

  def length(self):
    return math.sqrt(self.x*self.x + self.y*self.y)

  def normalize(self):
    return self * (1 / (self.length() + smallest_number))

  def abs(self):
    return _Vector(abs(self.x), abs(self.y))

  def to_grid(self):
    return _Vector(int(math.floor(self.x)), int(math.floor(self.y)))

  def dot(self, v):
    return self.x*v.x + self.y*v.y

  def rotate(self, angle):
    radians = angle.to_radians()
    x = self.x * math.cos(radians) - self.y * math.sin(radians)
    y = self.x * math.sin(radians) + self.y * math.cos(radians)
    return _Vector(x, y)

Direction = _Vector
Position = _Vector

LineSegment = collections.namedtuple('LineSegment', [ 'start', 'end', ])
Input = collections.namedtuple('Input', [ 'forward', 'backward', 'turn_left', 'turn_right', 'activate', ])
Player = collections.namedtuple('Player', [ 'name', 'position', 'forward', ])

initial_input = Input(
  forward=False,
  backward=False,
  turn_left=False,
  turn_right=False,
  activate=False
)

@enum.unique
class Material(enum.Enum):
  VOID = 0
  FLOOR = 1
  ATTENTEC = 2
  WALL = 3
  DOOR = 4
  WINDOW = 5
  DART = 6
  PAINTING1 = 7
  PAINTING2 = 8

@enum.unique
class Object(enum.Enum):
  KEY = 0
  APPLE = 1
  DESK = 2
  CHAIR = 3
  COMPUTER = 4
  PLANT = 5

class Map(collections.namedtuple('Map', 'materials, objects, width')):
  def __to_index(self, position):
    grid_position = position.to_grid()
    return grid_position.y*self.width + grid_position.x

  def material(self, position):
    index = self.__to_index(position)
    return self.materials[index] if index >= 0 and index < len(self.materials) else Material.VOID

  def replace_material(self, position, replacement):
    index = self.__to_index(position)
    new_materials = list(self.materials)
    new_materials[index] = replacement
    return self._replace(materials=new_materials)

class SquareSide(enum.Enum):
  HORIZONTAL = 0
  VERTICAL = 1

Collision = collections.namedtuple('Collision', [ 'position', 'distance', 'wall', 'side', ])

def find_first_collision(map, line_segment, debug=False):
  start, end = line_segment.start, line_segment.end
  grid_start, grid_end = start.to_grid(), end.to_grid()
  delta = end - start

  if abs(delta.x) < smallest_number and abs(delta.y) < smallest_number:
    return None

  direction = delta.normalize()
  dy_dx = math.inf if abs(direction.x) < smallest_number else direction.y / direction.x
  dx_dy = math.inf if abs(direction.y) < smallest_number else direction.x / direction.y

  horizontal_crossing_distance = math.sqrt(1 + dy_dx*dy_dx)
  vertical_crossing_distance = math.sqrt(1 + dx_dy*dx_dy)

  if abs(direction.x) < smallest_number:
    step_x = 0
    next_horizontal_crossing = math.inf
  elif direction.x < 0:
    step_x = -1
    next_horizontal_crossing = horizontal_crossing_distance * (start.x - grid_start.x)
  else:
    step_x = 1
    next_horizontal_crossing = horizontal_crossing_distance * (grid_start.x + 1 - start.x)

  if abs(direction.y) < smallest_number:
    step_y = 0
    next_vertical_crossing = math.inf
  elif direction.y < 0:
    step_y = -1
    next_vertical_crossing = vertical_crossing_distance * (start.y - grid_start.y)
  else:
    step_y = 1
    next_vertical_crossing = vertical_crossing_distance * (grid_start.y + 1 - start.y)

  steps = abs(grid_end.x - grid_start.x) + abs(grid_end.y - grid_start.y)
  x, y = grid_start.x, grid_start.y

  for _ in range(steps):
    if next_horizontal_crossing < next_vertical_crossing:
      side = SquareSide.HORIZONTAL
      next_horizontal_crossing += horizontal_crossing_distance
      x += step_x
    else:
      side = SquareSide.VERTICAL
      next_vertical_crossing += vertical_crossing_distance
      y += step_y

    position = Position(x, y)

    if map.material(position) != Material.FLOOR:
      if side == SquareSide.HORIZONTAL:
        distance = abs((x - start.x + (1 - step_x) / 2) / direction.x)
        wall = start.y + distance * direction.y
      else:
        distance = abs((y - start.y + (1 - step_y) / 2) / direction.y)
        wall = start.x + distance * direction.x

      return Collision(position, distance, wall, side)

  return None
