

def orbit():


    n = int(raw_input('How many?'))
    planets = list()
    for i in range(n):
        planets.append(planet())

    while key != 27:
        for obj in planets:
            addch(obj.X, obj.Y, ' ')
            obj.move(planets)
            addch(obj.X, obj.Y, 'o')




if __name__ == '__main__':
    orbit()
