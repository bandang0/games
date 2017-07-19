def pong():
   '''
      PONG game developped for the Theia Project
      to see curses documentation:
      https://docs.python.org/2/howto/curses.html
      https://docs.python.org/2/library/curses.html
      version: pong-1.1
   '''

    HEIGHT = 20
    WIDTH = 60
    TIMEOUT = 50

    class player(object):
        def __init__(self, name, body, keyup, keydown, side):
            self.name = name # name of player
            self.hit_score = 0
            self.keyup = keyup
            self.keydown = keydown
            self.body = body
            self.side = side
            if side == 'left':
                self.bounce = [[coord[0], coord[1]+1] for coord in self.body]
            if side == 'right':
                self.bounce = [[coord[0], coord[1]-1] for coord in self.body]
            for part in self.body:
                win.addch(part[0], part[1], '|')

        @property
        def score(self):
            return ' {}: {} '.format(self.name, self.hit_score)

        def make_a_point(self):
            self.hit_score += 1

        def update_bounce(self):
            if self.side == 'left':
                self.bounce = [[coord[0], coord[1]+1] for coord in self.body]
            if self.side == 'right':
                self.bounce = [[coord[0], coord[1]-1] for coord in self.body]
            for part in self.body:
                win.addch(part[0], part[1], '|')

        def go_up(self):
            win.addch(self.body[-1][0], self.body[-1][1], ' ')
            del self.body[-1]
            self.body.insert(0, [self.body[0][0]-1, self.body[-1][1]])
            self.update_bounce()
            win.addch(self.body[0][0], self.body[0][1], '|')

        def go_down(self):
            win.addch(self.body[0][0], self.body[0][1], ' ')
            del self.body[0]
            self.body.insert(len(self.body), [self.body[-1][0]+1, self.body[-1][1]])
            self.update_bounce()
            win.addch(self.body[-1][0], self.body[-1][1], '|')

    class ball(object):
        def __init__(self, dir=-1, coef=0):
            self.position = [HEIGHT/2, WIDTH/2]
            self.dir = dir
            self.coef = coef
            win.addch(self.position[0], self.position[1], 'o')

        def bounce(self, where):
            #control if len(player)%2 = 0 or 1
            if where == 0:
                self.coef -= 1
            elif where == 2:
                self.coef += 1
            self.dir *= -1

        def bounce_segment(self):
            self.coef *= -1

        def reset(self, position=[HEIGHT/2, WIDTH/2], dir=-1, coef=0):
            self.position = position
            self.dir = dir
            self.coef = coef

    print('---------------------------')
    print('Welcome to PONG multiplayer')
    print('---------------------------')
    name1 = raw_input('player left name: ')
    print('Do not use the following key(s): ESC, SPACE, p, n')
    keyup1 = ord('{}'.format(raw_input('{} key up: '.format(name1))))
    keydown1 = ord('{}'.format(raw_input('{} key down: '.format(name1))))

    name2 = raw_input('player right name: ')
    print('Do not use the following key(s): ESC, SPACE, p, n')
    keyup2 = ord('{}'.format(raw_input('{} key up: '.format(name2))))
    keydown2 = ord('{}'.format(raw_input('{} key down: '.format(name2))))

    curses.initscr()
    win = curses.newwin(HEIGHT, WIDTH, 0, 0) #y,x coordiates
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)
    win.timeout(TIMEOUT)

    #name1 = 'player1'
    score1 = 0
    body1 = [[HEIGHT/2-1, 1], [HEIGHT/2, 1], [HEIGHT/2+1, 1]]
    player1 = player(name1, body1, keyup1, keydown1, 'left')

    score2 = 0
    body2 = [[HEIGHT/2-1,WIDTH-2], [HEIGHT/2,WIDTH-2], [HEIGHT/2+1,WIDTH-2]]
    player2 = player(name2, body2, keyup2, keydown2, 'right')

    ball = ball()

    score_max = 3
    new_round_message = 'press SPACE bar for another round'
    new_round_message_erase = '                                 '
    end_message = '  THE END\n  - ESC to quit\n  - n bar for another game'
    key = 0
    point = False

    while key != 27: # While Esc key is not pressed
        win.border(0)
        win.addstr(0, 3, ' {}'.format(player1.score))
        win.addstr(0, WIDTH/2 - 4, ' PONG ')
        win.addstr(0, WIDTH-15, '{}'.format(player2.score))
        win.addstr(HEIGHT-1, WIDTH/2-12, ' ESC (quit), p (pause) ')

        event = win.getch()
        key = event

        if player1.hit_score == score_max-1:
            winer = player1
            looser = player2
            winer_message = '{} has defeated {} {}-{}'.format(winer.name, looser.name,
                                                    winer.hit_score+1, looser.hit_score)
        elif player2.hit_score == score_max-1:
            winer = player2
            looser = player1
            winer_message = '{} has defeated {} {}-{}'.format(winer.name, looser.name,
                                                    winer.hit_score+1, looser.hit_score)

    # pause mode
        prevKey = key
        event = win.getch()
        key = key if event == -1 else event

        if key == ord('p'):
            key = -1
            while key != ord('p'):
                key = win.getch()
            key = prevKey
            continue

    # move the players
        if key == player1.keyup:
            if player1.body[0][0] == 1 :
                continue
            else:
                player1.go_up()
        if key == player1.keydown:
            if player1.body[2][0] == HEIGHT-2 :
                continue
            else:
                player1.go_down()
        if key == player2.keyup:
            if player2.body[0][0] == 1 :
                continue
            else:
                player2.go_up()
        if key == player2.keydown:
            if player2.body[2][0] == HEIGHT-2 :
                continue
            else:
                player2.go_down()

    # move the ball
        if ball.position in player1.bounce:
            ball.bounce(player1.bounce.index(ball.position))
        elif ball.position in player2.bounce:
            ball.bounce(player2.bounce.index(ball.position))
        elif ball.position[0] == 1 or ball.position[0] == HEIGHT-2:
            ball.bounce_segment()

        if ball.position[1] == WIDTH-2 and ball.position not in player2.body:
            if player1.hit_score < score_max -1:
                win.addstr(3, 10, new_round_message)
            else:
                win.addstr(3, 10, end_message)
                win.addstr(7, 3, winer_message)

            player1.make_a_point()
            old = [ball.position[0], ball.position[1]]
            ball.reset(dir=1)
            point = True

        elif ball.position[1] == 1 and ball.position not in player1.body:
            if player2.hit_score < score_max -1:
                win.addstr(3, 10, new_round_message)
            else:
                win.addstr(3, 10, end_message)
                win.addstr(7, 3, winer_message)

            player2.make_a_point()
            old = [ball.position[0], ball.position[1]]
            ball.reset(dir=-1)
            point = True

        if point:
            if key == ord(' '):
                win.addch(old[0], old[1], ' ')
                win.addstr(3,10, new_round_message_erase)
                point = False
            elif key == ord('n'):
                win.addch(old[0], old[1], ' ')
                win.addstr(3, 2, '                       ')
                win.addstr(4, 2, '                       ')
                win.addstr(5, 2, '                         ')
                win.addstr(7, 2, '                                         ')
                player1.hit_score = 0
                player2.hit_score = 0
                point = False
            else:
                continue
        else:
            win.addch(ball.position[0], ball.position[1], ' ')
            ball.position = [ball.position[0]+ball.coef, ball.position[1]+ball.dir]
            if ball.position[0] < 1:
                ball.position[0] = 1
            elif ball.position[0] > HEIGHT-2:
                ball.position[0] = HEIGHT-2
            elif ball.position[1] < 1:
                ball.position[1] = 1
            elif ball.position[1] > WIDTH-2:
                ball.position[1] = WIDTH-2
            win.addch(ball.position[0], ball.position[1], 'o')

    curses.endwin()
    print('---------------------------')
    print('End game')
    try:
        print(winer_message)
    except UnboundLocalError:
        print('No one won the match')
    sys.exit(0)
