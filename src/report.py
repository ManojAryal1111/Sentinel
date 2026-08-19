from jinja2 import Environment, FileSystemLoader
from src.probe_loader import load_probes
from src.baseline import load_baseline

def generate_report():
    probes = load_probes()
    baseline = load_baseline()

    findings = []
    for probe in probes:
        status = baseline.get(probe.id, "UNKNOWN")
        findings.append({
            "id": probe.id,
            "category": probe.category,
            "severity": probe.severity,
            "description": probe.description,
            "status": status,
        })

    return findings


def render_html_report(target: str, output_path: str = "reports/report.html"):
    findings = generate_report()

    vuln_count = 0
    for f in findings:
        if "FAIL" in f["status"]:
            vuln_count += 1

    env = Environment(loader=FileSystemLoader("src"))
    template = env.get_template("report_template.html")
    html = template.render(findings=findings, vuln_count=vuln_count, total_count=len(findings), target=target)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)