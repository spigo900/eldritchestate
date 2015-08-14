* Keep a list of rooms.
* Each room is defined as a set of shapes.
* No room can intersect with any other room; this may be determined by checking
  each shape of the room against each shape of the other room... but that would
  get computationally intensive *very* fast, so I'm not sure I want to do it
  that way.

  Perhaps I'll just have a "bounding box" algorithm that takes a
  list/tuple/iterable of shapes and returns a new rectangle representing the
  bounding box. That way, I only have to check either one or N shapes, depending
  on whether I check each shape of the room currently being generated against
  the bounding box, or if I check only the room's own bounding box. I'm not sure
  which would give nicer results or if it would even make a significant
  difference; I guess I could always try it and find out.
* Pick a random spot and try to put a room there. (Actually, I may use a better
  algorithm for room placement than that. Probably will, in fact. How can I
  check, for example, that the room is connected to another room? How can I
  ensure that certain rooms are always placed together, or that they're
  connected somehow, in some specific way, perhaps?

  Maybe I should have a field in my map description dictionary for
  room-clusters... I'm not sure how I'd describe them in data, though, exactly.
  I suppose I'll have to think about that... or, no. I don't think it'll work.
  It's a bit too explicit, for one, and for another thing, how do I specify how
  abuilding should be laid out without making the whole thing a cluster? It
  can't work that way. I think what I'll want instead is this: I'll have some
  kind of field in the room for rooms it prefers to connect to/be adjacent to.
  I'll also have a max\_connections attribute on rooms, and a connection\_sides
  attribute... probably. I'm not completely sure how I want that to work. I
  suppose I'll have to experiment with it a bit, but I think that should be fine
  for a first-pass, anyway. I should certainly be able to describe most rooms
  that way.

  It'll have to be more complicated once I start adding z-levels, of course, but
  that won't be until after I'm through with the prototype, and that won't be
  for a while.

Rooms... rooms... what should the room type data structure look like? I'm
thinking they should be able to specify frequency, min and max rooms of type,
max connections, preferred connections, possibly preferred/mandatory adjacencies
(so you can specify that certain room types must be adjacent to the outside
world, for example, so you can have windows in a way that makes sense), fixed
tiles (in a map data structure, I think, so you can specify all tiles or none),
and... yeah, I'm not sure what all.

It's gonna be kind of interesting to figure that out; I want to be able to
support maps for industrial buildings, (legal) offices, and homes, especially
big, creaky mansions and the like -- think The Haunting, The Frighteners, et
cetera, except more eldritch and creepy. Like The Mansion 3: Freeman's
Residence, but creakier and older. Old, 1700's and 1800's style buildings; hell,
really, buildings that were old even then, I think.

Room shape, I think I'll specify as a list of shapes (technically, a set, as
they're converted to one internally, but JSON has no such thing and I don't
think Python has an EDN parser... not that it would really make sense to use one
with it). As for generating things like walkways and split-level rooms (things
like stages and grand stair rooms)... that's actually going to be a problem. I'm
not sure how to do that, exactly. I think one thing I'll want to do is have a Z
dimension for the shapes, too... maybe you can specify a cube as a
six-tuple/list, and a cylinder as a... wait, a cylinder would have four
dimensions. Damn. That makes it harder. Maybe I'll have to specify them as
dictionaries instead of lists. That'd probably make it simpler. And shapes with
no Z dimension are considered flat.



Rectangles are a tuple of four elements (x, y, width, height).

Circles are a tuple of three elements (x, y, radius).

Ellipses are... what? I'm not sure, because I have no idea how ellipses are
defined except that it involves quadratic equations somehow. I doubt I'll need
them, though.
