import argparse
from wordset import WordSet
from wordlegame import WordleGame
import files
import logging
from gamerunner import GameRunner
from guessers import MisterRando, GoodGuesser
import json



def run(game_count, top, infile, outfile, logging_level):
    logging.basicConfig(level=logging_level)
    logging.info(
        f"Generating {game_count} games and outputting top {top} games to {outfile} using {infile} as input."
    )
    words = get_word_set(infile)
    runner = GameRunner(words)
    games = runner.generate_games(game_count)
    result = runner.run_games(games, GoodGuesser(words).guess)
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
    for game in result:
        game_stats["total"] += 1
        if game.state == "win":
            game_stats["wins"] += 1
            game_stats[f"win{len(game.guesses)}"] += 1
        elif game.state == "loss":
            game_stats["losses"] += 1
        else:
            game_stats["failed"] += 1

    result_str = json.dumps(game_stats)

    #result_str = "\n\n".join([game.summary_string() for game in result[:game_count]])
    files.to_output(outfile, result_str)


def get_word_set(infile):
    file_text = files.from_input(infile)
    words = WordSet(file_text)
    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate syntetic data for Wordle game."
    )
    parser.add_argument(
        "--games", type=int, help="Number of games to generate.", default=100
    )
    parser.add_argument(
        "--top",
        type=int,
        help="Top number of games of best scoring games to output to the training file",
        default=50,
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
