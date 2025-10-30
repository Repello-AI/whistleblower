import argparse
from core.whistleblower import whistleblower

def main():
    parser = argparse.ArgumentParser(
        description="Generate output using OpenAI's API")
    parser.add_argument('--json_file', type=str, required=True,
                        help="Path to the JSON file with input data")
    parser.add_argument('--transport', type=str, choices=['rest', 'websocket'], 
                        default='rest', help="Transport type: 'rest' or 'websocket' (default: rest)")

    args = parser.parse_args()

    output = whistleblower(args)
    print(output)
    return output


if __name__ == "__main__":
    main()