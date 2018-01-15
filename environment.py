from board import BoardState


def play_game(agent1, agent2):
    board = BoardState()
    while True:
        x_move = agent1.act(board)

        if not board.is_legal_move(x_move):
            agent1.reward(-10)
            agent2.reward(1)
            return -10, 1

        if board.put_x(x_move):
            agent1.reward(1)
            agent2.reward(-1)
            return 1, -1

        if board.is_over():
            agent1.reward(0)
            agent2.reward(0)
            return 0, 0

        o_move = agent2.act(board)

        if not board.is_legal_move(o_move):
            agent1.reward(1)
            agent2.reward(-10)
            return 1, -10

        if board.put_o(o_move):
            agent1.reward(-1)
            agent2.reward(1)
            return -1, 1

        if board.is_over():
            agent1.reward(0)
            agent2.reward(0)
            return 0, 0


def play_half_set(agent1, agent2, length=49):
    total_result_1 = 0
    total_result_2 = 0
    fatal_wins = 0
    wins = 0
    draws = 0
    losses = 0
    fatal_losses = 0
    for i in range(0, length):
        result_1, result_2 = play_game(agent1, agent2)
        if result_1 == -10:
            fatal_losses += 1
            result_1 = -1
        elif result_1 == -1:
            losses += 1
        elif result_1 == 0:
            draws += 1
        elif result_2 == -1:
            wins += 1
        else:
            fatal_wins += 1
            result_2 = -1
        total_result_1 += result_1
        total_result_2 += result_2
    agent1.flush()
    agent2.flush()
    return total_result_1, total_result_2, fatal_wins, wins, draws, losses, fatal_losses


def play_set(agent1, agent2):
    first_total_result_1, first_total_result_2, first_fatal_wins, first_wins, first_draws, first_losses, first_fatal_losses = play_half_set(agent1, agent2)
    second_total_result_1, second_total_result_2, second_fatal_wins, second_wins, second_draws, second_losses, second_fatal_losses = play_half_set(agent2, agent1)
    total_result = first_total_result_1 + second_total_result_2

    print('Versus {}: ++{} +{} ={} -{} --{}    {}  {}{}'.format(
        str(agent2.__class__.__name__).rjust(25),
        str(first_fatal_wins + second_fatal_losses).rjust(2),
        str(first_wins + second_losses).rjust(2),
        str(first_draws + second_draws).rjust(2),
        str(first_losses + second_wins).rjust(2),
        str(first_fatal_losses + second_fatal_wins).rjust(2),
        '.' * 3,
        '+' if total_result > 0 else '-',
        abs(total_result)
    ))
    return total_result
