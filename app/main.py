import argparse
from pathlib import Path
from app.service import build_report, normalize_input, simulate_delivery
from app.utility import load_json, save_json


def process_file(input_path: Path, output_path: Path):

    raw_data = load_json(input_path)

    validated_data = normalize_input(raw_data)

    stats = simulate_delivery(validated_data)

    report = build_report(stats)

    save_json(report.model_dump(), output_path,)


def process_directory(input_directory: Path, output_directory: Path):
   
    json_files = sorted(input_directory.glob("*.json"))

    if not json_files:
        raise ValueError(f"No JSON files found in {input_directory}")

    output_directory.mkdir(parents=True, exist_ok=True)

    for input_file in json_files:

        output_file = (
            output_directory
            / f"{input_file.stem}_report.json"
        )

        process_file(input_file, output_file )
        print(f"Processed: {input_file.name}, {output_file}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=("FastBox Delivery System Simulator")
    )

    parser.add_argument("input", type=Path,
        help=(
            "JSON file or directory "
            "containing JSON files"
        ),
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("reports"),
        help="Output file or directory.",
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    if not args.input.exists():
        raise SystemExit(f"Input path does not exist: {args.input}")

    try:
        if args.input.is_file():
            output_path = args.output

            if args.output.is_dir():
                output_path = (
                    args.output
                    / f"{args.input.stem}_report.json"
                )

            process_file(args.input, output_path)
            print(f"Report generated: {output_path}")

        elif args.input.is_dir():

            process_directory(args.input, args.output)

    except (ValueError, FileNotFoundError) as e:

        raise SystemExit(f"Error: {e}") from e


if __name__ == "__main__":
    main()