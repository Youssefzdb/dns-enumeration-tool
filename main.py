import sys
from utils.cli_parser import parse_arguments
from core.orchestrator import DNSEnumOrchestrator

def main():
    try:
        args = parse_arguments()
        orchestrator = DNSEnumOrchestrator(
            target=args.target,
            nameserver=args.nameserver,
            port=args.port,
            wordlist=args.wordlist,
            threads=args.threads,
            output=args.output,
            format=args.format
        )
        orchestrator.run()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()