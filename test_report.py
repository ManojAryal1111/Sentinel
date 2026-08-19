from src.report import generate_report

findings = generate_report()
for f in findings:
    print(f)