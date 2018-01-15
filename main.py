from formatting import *
from model import agent_exists, load_user_agent, load_vendor_agent
from human import play_against


print('Welcome to {}Tic{}-{}Tac{}-{}Toe{}!'.format(FONT_BOLD + COLOR_GREEN, COLOR_END, FONT_BOLD + COLOR_YELLOW, COLOR_END, FONT_BOLD + COLOR_RED, COLOR_END))
print_line()
while True:
    print('What do you want?')
    print(' 1. Watch neural network training by playing vs hard-coded agents')
    print(' 2. Watch neural network training by self-playing')
    print(' 3. To play vs neural network provided by package')
    print(' 4. To play vs neural network trained locally by (1) or (2)')
    choice = input('Your choice: ')
    if choice == '1':
        import hardcoded
        break
    elif choice == '2':
        import selfplay
        break
    elif choice == '3':
        play_against(load_vendor_agent())
        break
    elif choice == '4':
        if not agent_exists():
            print('{}You have to train agent first - select 1 or 2 and let it play a bit{}'
                  .format(COLOR_RED + FONT_BOLD, COLOR_END))
        else:
            play_against(load_user_agent())
            break
    else:
        print('{}Please enter number 1, 2, 3 or 4{}'.format(COLOR_RED + FONT_BOLD, COLOR_END))
    print_separator()