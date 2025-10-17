import argparse
from core.whistleblower import whistleblower
from core.report_data import ReportData
from reports import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Generate output using OpenAI's API and optionally create structured audit reports")
    parser.add_argument('--json_file', type=str, required=True,
                        help="Path to the JSON file with input data")
    parser.add_argument('--api_key', type=str, default=None,
                        help="OpenAI API key (overrides the one in JSON file)")
    parser.add_argument('--model', type=str, default=None,
                        help="OpenAI model to use (overrides the one in JSON file)")
    parser.add_argument('--report-format', type=str, choices=['markdown', 'pdf'], default=None,
                        help="Generate a structured report in the specified format (markdown or pdf)")
    parser.add_argument('--output-file', type=str, default=None,
                        help="Path for the output report file (without extension)")

    args = parser.parse_args()

    # Create ReportData object if report generation is requested
    report_data = None
    if args.report_format:
        report_data = ReportData()
    
    # Run whistleblower detection
    output = whistleblower(args, report_data)
    print(output)
    
    # Generate report if requested
    if args.report_format and report_data:
        generator = ReportGenerator()
        try:
            report_path = generator.generate(report_data, args.report_format, args.output_file)
            print(f"\n✓ Report generated successfully: {report_path}")
        except Exception as e:
            print(f"\n✗ Error generating report: {e}")
    
    return output


if __name__ == "__main__":
    main()