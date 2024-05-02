import argparse
import files

def run(games, top, infile, outfile):
    file_text = files.from_input(infile)
    
    words = files.read_words(infile)
    games = files.generate_games(words, games)
    games = files.sort_games(games)
    games = games[:top]
    files.write_games(games, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate syntetic data for Wordle game.')
    parser.add_argument('--games', type=int, help='Number of games to generate.', default=10000)
    parser.add_argument('--top', type=int, help='Top number of games of best scoring games to output to the training file', default=1000)
    parser.add_argument('--outfile', type=str, help='Output file name. Default is "training.txt"', default="training.txt")
    parser.add_argument('--infile', type=str, help='Input file with valid words.', default="valid_words.txt")
    args = parser.parse_args()

    run(args.games, args.top, args.infile, args.outfile)