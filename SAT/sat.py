from math import sqrt


def normalize(vector):
    """
    Вектор масштабируется до длины 1
    """
    norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector[0] / norm, vector[1] / norm


def dot(vector1, vector2):
    """
    Точка (или скалярное) произведение двух векторов
    """
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]


def edge_direction(point0, point1):
    """
    Вектор, идущий из point0 в point1
    """
    return point1[0] - point0[0], point1[1] - point0[1]


def orthogonal(vector):
    """
    Новый вектор, ортогональный данному вектору
    """
    return vector[1], -vector[0]

def project(vertices, axis):
    """
    Вектор, показывающий, сколько вершин лежит вдоль оси
    """
    if len(vertices) == 2:
        return project_circle(vertices, axis)
    dots = [dot(vertex, axis) for vertex in vertices]
    return [min(dots), max(dots)]

def project_circle(vertices, axis):
    dot_circle = dot(vertices[0], axis)
    return [dot_circle - vertices[1], dot_circle + vertices[1]]


def overlap(projection1, projection2):
    """
    Логическое значение, указывающее, перекрываются ли две проекции.
    """
    return min(projection1) <= max(projection2) and \
           min(projection2) <= max(projection1)


def vertices_to_edges(vertices):
    """
    Список ребер вершин как векторов
    """
    if len(vertices) == 2:
        return []
    return [edge_direction(vertices[i], vertices[(i + 1) % len(vertices)])
            for i in range(len(vertices))]

def separating_axis_theorem(vertices_a, vertices_b):
    edges = vertices_to_edges(vertices_a) + vertices_to_edges(vertices_b)
    axes = [normalize(orthogonal(edge)) for edge in edges]

    for axis in axes:
        projection_a = project(vertices_a, axis)
        projection_b = project(vertices_b, axis)

        overlapping = overlap(projection_a, projection_b)

        if not overlapping:
            return False
    return True
