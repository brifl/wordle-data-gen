import argparse
from wordset import WordSet
from wordlegame import WordleGame
import files
from typing import List
import logging
from gamerunner import GameRunner
from guessers import MisterRando, GoodGuesser
import json


def run(game_count, top, infile, outfile, logging_level):
    logging.basicConfig(level=logging_level)
    logging.info(
        f"Generating {game_count} games and outputting best of of {top} games to {outfile} using {infile} as input."
    )
    words = get_word_set(infile)
    runner = GameRunner(words)
    games = runner.generate_games(game_count)
    result_sets = []
    guesser = GoodGuesser(words)

    for _ in range(top):
        running_games = runner.clone_games_fresh(games)
        result = runner.run_games(running_games, guesser.guess)
        result_sets.append(result)

    best_result = result_sets[0]
    if top > 1:
        for i in range(game_count):
            for j in range(1, top):
                if len(result_sets[j][i].guessed_words) < len(
                    best_result[i].guessed_words
                ):
                    best_result[i] = result_sets[j][i]

    write_stats(game_count, outfile, best_result)
    write_training(outfile, best_result)


def write_training(outfile, best_result):
    #result_str = "\n".join([get_replay_text(game) for game in best_result])

    all_alpacas = []
    for game in best_result:
        all_alpacas.extend(get_replay_alpaca(game))
    result_str = json.dumps(all_alpacas, indent=4)

    files.to_output(outfile, result_str)


def get_replay_text(game: WordleGame) -> str:
    text = "User: Wordle start\n"
    replay = WordleGame(game.word)
    for i, guess in enumerate(game.guessed_words):
        text += f"Assistant: Guess {i+1}: {guess}\n"
        won = replay.guess(guess)
        if won:
            break
        text += f"User: Feedback: {mask_word(replay.word, replay.remaining_word)} Wrong spot: {sorted(list(replay.wrong_spot))} Eliminated: {sorted(list(replay.letters_not_remaining))}\n"
    text = text + f"User: The word was '{replay.word}'. Outcome: {replay.state}! Game end.\n"
    return text

def get_replay_alpaca(game: WordleGame) -> str:

    alpacas = []   
    replay = WordleGame(game.word)
    for i, guess in enumerate(game.guessed_words):
        alpaca = {}        
        alpaca["instruction"] = "Guess the next Wordle word." 
        alpaca["input"] = f"Guesses: {replay.guessed_words}, Matches: {mask_word(replay.word, replay.remaining_word)}, Wrong spot: {sorted(list(replay.wrong_spot))}, Eliminated: {sorted(list(replay.letters_not_remaining))}"
        alpaca["output"] = guess
        won = replay.guess(guess)
        alpacas.append(alpaca)
        if won:
            break

    return alpacas

    


def mask_word(word, mask):
    masked = ""
    for i in range(len(word)):
        if mask[i] == "*":
            masked += word[i]
        else:
            masked += "*"
    return masked


def write_stats(game_count, outfile, best_result):
    game_stats = {
        "total": game_count,
        "wins": 0,
        "losses": 0,
        "failed": 0,
        "win1": 0,
        "win2": 0,
        "win3": 0,
        "win4": 0,
        "win5": 0,
        "win6": 0,
    }
    for game in best_result:
        logging.debug(game.state)
        if game.state == "won":
            game_stats["wins"] += 1
            game_stats[f"win{len(game.guessed_words)}"] += 1
        elif game.state == "lost":
            game_stats["losses"] += 1
        else:
            game_stats["failed"] += 1

    result_str = json.dumps(game_stats)

    # result_str = "\n\n".join([game.summary_string() for game in result[:game_count]])
    files.to_output(outfile + "_stats", result_str)


def get_word_set(infile):
    file_text = files.from_input(infile)
    words = WordSet(file_text)
    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate syntetic data for Wordle game."
    )
    parser.add_argument(
        "--games", type=int, help="Number of games to generate.", default=10
    )
    parser.add_argument(
        "--top",
        type=int,
        help="Top of x number of games for a given word. Will take the best score of this many attempts.",
        default=1,
    )
    parser.add_argument(
        "--outfile",
        type=str,
        help='Output file name. Default is "training.txt"',
        default="training.txt",
    )
    parser.add_argument(
        "--infile",
        type=str,
        help="Input file with valid words.",
        default="valid_words.txt",
    )
    parser.add_argument(
        "--loglevel",
        type=str,
        help="Log level options are DEBUG, INFO, WARNING, ERROR, CRITICAL",
        default="INFO",
    )
    args = parser.parse_args()

    run(args.games, args.top, args.infile, args.outfile, args.loglevel.upper())
