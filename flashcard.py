from io import StringIO
import argparse

parser = argparse.ArgumentParser()
for arg in {'--import_from', '--export_to'}:
    parser.add_argument(arg)
args = parser.parse_args()
log = StringIO()
flashcard = {}


def printl(obj: 'Any Type'):
    print(obj, file=log, flush=True)
    print(obj)


def inputl():
    content = input()
    print('>' + content, file=log, flush=True)
    return content


def add():
    printl('The card:')
    while 1:
        card = inputl()
        if card not in flashcard:
            break
        printl(f'The card "{card}" already exists. Try again:')
    printl('The definition of the card:')
    while 1:
        definition = inputl()
        if definition not in [flashcard[x][0] for x in flashcard]:
            break
        printl(f'The definition "{definition}" already exists. Try again:')
    flashcard[card] = [definition, 0]
    printl(f'The pair ("{card}":"{definition}") has been added.')


def remove():
    printl('Which card?')
    card = inputl()
    if card in flashcard:
        flashcard.pop(card)
        printl('The card has been removed.')
        return
    printl(f'Can\'t remove "{card}": there is no such card.')


def import_(file_name):
    try:
        with open(file_name) as file:
            n = 0
            for x in file:
                flash = x.split(':', maxsplit=1)
                meaning = flash[1].strip().split('@')
                flashcard[flash[0]] = [meaning[0], int(meaning[1])]
                n += 1
            printl(f'{n} cards have been loaded.')
    except FileNotFoundError:
        printl('File not found.')


def export_(file_name):
    printl('File name:')
    with open(file_name, 'a') as file:
        n = 0
        for x in flashcard:
            file.writelines(f'{x}: {flashcard[x][0]}@{flashcard[x][1]}\n')
            n += 1
        printl(f'{n} cards have been saved.')


def ask():
    printl('How many times to ask?')
    n = int(inputl())
    i, k = 0, 0
    while k < n:
        i = list(flashcard.keys())[k % len(flashcard)]
        printl(f'print the definition of "{i}":')
        answer = inputl()
        if answer == flashcard[i][0]:
            printl('Correct')
        else:
            if answer in [flashcard[x][0] for x in flashcard]:
                answer = list(flashcard.keys())[[flashcard[x][0] for x in flashcard].index(answer)]
                printl(f'Wrong. The right answer is "{flashcard[i][0]}", but your definition is correct for "{answer}" '
                       f'card.')
            else:
                printl(f'Wrong. The right answer is "{flashcard[i][0]}".')
            flashcard[i][1] += 1
        k += 1


def logger():
    global log
    printl('File name:')
    with open(inputl(), 'w') as file:
        for x in log.getvalue().split('\n'):
            file.write(x + '\n')
    printl('The log has been saved.')


def hardest_card():
    # Compteur d'erreur non vide
    max_error = [flashcard[x][1] for x in flashcard if flashcard[x][1] != 0]
    if max_error:
        # Plus grand compteur d'erreur
        hardest_stat = max(max_error)
        # carte avec le plus grand compteur
        hardest = [x for x in flashcard if flashcard[x][1] == hardest_stat]
        if len(hardest) == 1:
            text = f'The hardest card is "{hardest[0]}". You have {hardest_stat} ' \
                   f'errors answering it.'
        else:
            tricky = ",".join('"' + x + '"' for x in hardest)
            text = f'The hardest cards are {tricky}. You have {hardest_stat} ' \
                   f'errors answering them.'
        printl(text)
    else:
        printl("There are no cards with errors.")


def reset_stats():
    for x in flashcard:
        flashcard[x][1] = 0
    printl('Card statistics have been reset.')


def menu():
    if args.import_from:
        import_(args.import_from)
    while 1:
        printl('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        choice = inputl()
        match choice:
            case 'add':
                add()
            case 'remove':
                remove()
            case 'import':
                printl('File name:')
                file_name = inputl()
                import_(file_name)
            case 'export':
                printl('File name:')
                file_name = inputl()
                export_(file_name)
            case 'ask':
                ask()
            case 'log':
                logger()
            case 'hardest card':
                hardest_card()
            case 'reset stats':
                reset_stats()
            case 'exit':
                if args.export_to:
                    export_(args.export_to)
                printl('Bye bye!')
                exit()


if __name__ == '__main__':
    menu()
    log.close()

