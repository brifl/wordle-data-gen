import argparse
import files
from games import WordSet


def run(games, top, infile, outfile):
    print(
        f"Generating {games} games and outputting top {top} games to {outfile} using {infile} as input."
    )
    file_text = files.from_input(infile)
    words = WordSet(file_text)
    # words.apply_length_filter(5)
    # five_letter_word_data = '\n'.join(words.get_filtered_words())
    # files.to_output(outfile, five_letter_word_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate syntetic data for Wordle game."
    )
    parser.add_argument(
        "--games", type=int, help="Number of games to generate.", default=10000
    )
    parser.add_argument(
        "--top",
        type=int,
        help="Top number of games of best scoring games to output to the training file",
        default=1000,
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
    args = parser.parse_args()

    run(args.games, args.top, args.infile, args.outfile)
