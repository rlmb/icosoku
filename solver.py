
class Vertex:
    def __init__(self, value):
        self.triangle_cnt = 0
        self.value = value
        self.current_value = 0
        self.current_cnt = 0
        self.is_not_ok = False

    def add_brick_point(self, value):
        self.current_cnt += 1
        self.current_value += value
        self._update_not_ok()

        if self.current_cnt > 5:
            print('Error - for Vertex %d, added too many point', self.value)

    def remove_brick_point(self, value):
        self.current_cnt -= 1
        self.current_value -= value
        self._update_not_ok()

        if self.current_cnt < 0:
            print('Error - for Vertex %d, removed too many point', self.value)

    def _update_not_ok(self):
        self.is_not_ok = self.current_value > self.value or (self.current_cnt == 5 and self.current_value != self.value) or ((self.value - self.current_value) > 3*(5-self.current_cnt))


class Brick:
    def __init__(self, point_a, point_b, point_c):
        self.point_a_orig = point_a
        self.point_b_orig = point_b
        self.point_c_orig = point_c
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        self.rotation = 0
        self.can_rotate = (point_a != point_b) or (point_a != point_c) or (point_b != point_c)

    def reset(self):
        self.point_a = self.point_a_orig
        self.point_b = self.point_b_orig
        self.point_c = self.point_c_orig
        self.rotation = 0

    def rotate(self):
        if self.rotation >= 2:
            print('Warning - rotate a brick more than twice. This is unnecessary.')
        self.rotation += 1

        if self.can_rotate:
            old_point_c = self.point_c
            self.point_c = self.point_b
            self.point_b = self.point_a
            self.point_a = old_point_c
        else:
            print('Warning - rotate a brick which does not need to be ' + repr(self))

    def __repr__(self):
        return 'Brick ' + str(self.point_a) + '|' + str(self.point_b) + '|' + str(self.point_c) + ' (' + str(self.point_a_orig) + '|' + str(self.point_b_orig) + '|' + str(self.point_c_orig) + ', rotation ' + str(self.rotation) + ')'


class Triangle:

    def __init__(self, vertex_a, vertex_b, vertex_c):
        self.brick = None
        self.vertexes = [vertex_a, vertex_b, vertex_c]
        vertex_a.triangle_cnt += 1
        vertex_b.triangle_cnt += 1
        vertex_c.triangle_cnt += 1

    def add_brick(self, brick):
        self.vertexes[0].add_brick_point(brick.point_a)
        self.vertexes[1].add_brick_point(brick.point_b)
        self.vertexes[2].add_brick_point(brick.point_c)
        self.brick = brick

    def remove_brick(self, brick):
        self.vertexes[0].remove_brick_point(brick.point_a)
        self.vertexes[1].remove_brick_point(brick.point_b)
        self.vertexes[2].remove_brick_point(brick.point_c)
        self.brick = None

    def __repr__(self):
        output = 'Triangle ' + str(self.vertexes[0].value) + '|' + str(self.vertexes[1].value) + '|' + str(self.vertexes[2].value)
        if self.brick is not None:
            output += ' - ' + repr(self.brick)
        return output


class Cube:
    def __init__(self):
        self.vertexes = {}
        for val in range(1, 13):
            self.vertexes[val] = Vertex(value=val)
        self.triangles = []
        self.next_triangle = 0

    def define_triangle(self, val_a, val_b, val_c):
        if len(self.triangles) >= 20:
            print('Error - only 20 Triangles can be defined')
        self.triangles.append(Triangle(self.vertexes[val_a], self.vertexes[val_b], self.vertexes[val_c]))

    def add_brick(self, brick):
        if self.next_triangle > len(self.triangles):
            print('Error - try to add a brick on triangle %d, but only %d triangles are defined.' % (self.next_triangle, len(self.triangles)))
            return
        self.triangles[self.next_triangle].add_brick(brick)
        self.next_triangle += 1

    def remove_brick(self, brick):
        if self.next_triangle <= 0:
            print('Error - try to remove a brick but none are set.')
            return
        self.next_triangle -= 1
        self.triangles[self.next_triangle].remove_brick(brick)

    def check_setup(self):
        res_status = True
        for vertex in self.vertexes.values():
            if vertex.triangle_cnt != 5:
                print('Vertex ' + vertex.value + ' is not correctly configured (' + str(vertex.triangle_cnt) + ' triangles)')
                res_status = False
        return res_status

    def check(self):
        for vertex in self.vertexes.values():
            if vertex.is_not_ok:
                return False
        return True

    def __repr__(self):
        output = 'Cube'
        for triangle in self.triangles:
            output += '\n' + repr(triangle)
        return output


if __name__ == '__main__':

    # Create bricks
    bricks = []
    bricks.append([Brick(3, 3, 3)])
    bricks.append([Brick(0, 3, 3)])
    bricks.append([Brick(1, 3, 2), Brick(1, 3, 2)])
    bricks.append([Brick(1, 2, 3), Brick(1, 2, 3)])
    bricks.append([Brick(2, 0, 0)])
    bricks.append([Brick(2, 2, 2)])
    bricks.append([Brick(2, 2, 0)])
    bricks.append([Brick(3, 0, 0)])
    bricks.append([Brick(1, 0, 2), Brick(1, 0, 2), Brick(1, 0, 2)])
    bricks.append([Brick(1, 2, 0), Brick(1, 2, 0), Brick(1, 2, 0)])
    bricks.append([Brick(1, 1, 1)])
    bricks.append([Brick(0, 1, 1)])
    bricks.append([Brick(1, 0, 0)])
    bricks.append([Brick(0, 0, 0)])

    # Create the Cube
    cube = Cube()
    cube.define_triangle(1, 4, 5)    # 1
    cube.define_triangle(4, 12, 5)   # 2
    cube.define_triangle(5, 12, 6)   # 3
    cube.define_triangle(5, 6, 2)    # 4
    cube.define_triangle(5, 2, 1)    # 5
    cube.define_triangle(1, 2, 3)    # 6
    cube.define_triangle(1, 3, 9)    # 7
    cube.define_triangle(1, 9, 4)    # 8
    cube.define_triangle(4, 9, 10)   # 9
    cube.define_triangle(4, 10, 12)  # 10
    cube.define_triangle(12, 10, 11) # 11
    cube.define_triangle(12, 11, 6)  # 12
    cube.define_triangle(6, 11, 7)   # 13
    cube.define_triangle(2, 6, 7)    # 14
    cube.define_triangle(2, 7, 3)    # 15
    cube.define_triangle(3, 7, 8)    # 16
    cube.define_triangle(3, 8, 9)    # 17
    cube.define_triangle(9, 8, 10)   # 18
    cube.define_triangle(11, 8, 7)   # 19
    cube.define_triangle(11, 10, 8)  # 20

    debug_level = 5
    # Brute Force Search
    def solve(a_cube, bricks_orig, level=0, percent=0, gran=1):
        # check if there is remaining bricks to assign
        remaining_brick = False
        for br in bricks:
            if len(br):
                remaining_brick = True
                break
        if not remaining_brick:        
            print('There is no bricks anymore')
            return True
        
        for i in range(0, len(bricks)):
            if len(bricks[i]) == 0:
                continue

            b = bricks[i].pop(0)

            # assign a brick with rotation 0
            percent_current = percent + gran*3*i/(3*len(bricks))
            if level <= debug_level:
                print('%2.2f%% - Level %s, on %s, try %s' % (100*percent_current, str(level), repr(a_cube.triangles[level]), repr(b)))
            a_cube.add_brick(b)
            if a_cube.check():
                if solve(a_cube, bricks, level+1, percent_current, gran/(3*len(bricks))):
                    return True
            a_cube.remove_brick(b)

            if b.can_rotate:
                # assign a brick with rotation 1
                b.rotate()
                percent_current = percent + gran*(3*i+1)/(3*len(bricks))
                if level <= debug_level:
                    print('%2.2f%% - Level %s, on %s, try %s' % (100*percent_current, str(level), repr(a_cube.triangles[level]), repr(b)))
                a_cube.add_brick(b)
                if a_cube.check():
                    if solve(a_cube, bricks, level+1, percent_current, gran/(3*len(bricks))):
                        return True
                a_cube.remove_brick(b)

                # assign a brick with rotation 2
                b.rotate()
                percent_current = percent + gran*(3*i+2)/(3*len(bricks))
                if level <= debug_level:
                    print('%2.2f%% - Level %s, on %s, try %s' % (100*percent_current, str(level), repr(a_cube.triangles[level]), repr(b)))
                a_cube.add_brick(b)
                if a_cube.check():
                    if solve(a_cube, bricks, level+1, percent_current, gran/(3*len(bricks))):
                        return True
                a_cube.remove_brick(b)

            # Reset the brick (rotation)
            b.reset()
            bricks[i].insert(0, b)

    if cube.check_setup():
        if solve(cube, bricks):
            print(repr(cube))
        else:
            print('No result found')
